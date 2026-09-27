import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

class FraudDetectionModel:
    def __init__(self):
        self.model_path="fraud_anomaly_model.joblib"
        self.model=self._load_or_train()

    def _load_or_train(self)->IsolationForest:
        """
        Model Persistence: Loads pre-trained model from disk or trains a new one.
        Features trained on: [amount, ratio_to_avg, is_night, is_intl]
        """
        if os.path.exists(self.model_path):
            print(">> [Fraud Engine] Loaded calibrated IsolationForest from disk (joblib).")
            return joblib.load(self.model_path)

        print(">> [Fraud Engine] Training multi-dimensional IsolationForest...")
        np.random.seed(42)

        # 3,000 baseline Indian retail transactions
        # Feature 0: Amount (Normal: ₹50 to ₹4,000)
        amounts=np.random.exponential(scale=1000,size=(3000,1))
        amounts=np.clip(amounts,20.0,15000.0)

        # Feature 1: Ratio to customer average (Normal: 0.2x to 2.5x)
        ratios=np.random.normal(loc=1.0,scale=0.4,size=(3000,1))
        ratios=np.clip(ratios,0.1,3.0)

        # Feature 2: Is Night (96% day, 4% late night)
        nights=np.random.choice([0,1],size=(3000,1),p=[0.96,0.04])

        # Feature 3: Is International (99% domestic, 1% intl)
        intls=np.random.choice([0,1],size=(3000,1),p=[0.99,0.01])

        X_train=np.hstack([amounts,ratios,nights,intls])

        model=IsolationForest(contamination=0.02,random_state=42)
        model.fit(X_train)
        joblib.dump(model,self.model_path)
        print(">> [Fraud Engine] Calibrated & saved to 'fraud_anomaly_model.joblib'.")
        return model

    def evaluate_risk(self,
                            amount: float,
                            amount_to_mean_ratio:float, 
                            is_night:bool, 
                            is_international: bool
                            ) -> tuple[bool,float]:

        """
        Multi-Factor Institutional Fraud Scoring.
        Returns: (is_anomaly: bool, calibrated_risk_score: 0.0 to 99.9)
        """

        night_flag= 1 if is_night else 0
        intl_flag=1 if is_international else 0

        # 4-dimensional feature vector
        features=np.array([[amount,amount_to_mean_ratio,night_flag,intl_flag]])

        # 1. Structural Anomaly via Isolation Forest
        raw_prediction=self.model.predict(features)[0]
        is_anomaly=(raw_prediction==-1)
        raw_score=self.model.decision_function(features)[0]

        # Base tree risk (scaled 0 to 45)
        # Deep normal ~ 5-15; anomaly boundary ~ 35-45
        tree_risk=max(5.0,min(45.0,(0.25-raw_score)*100))

        # 2. Behavioral Velocity Factor (Logarithmic Ratio Multiplier)
        # If ratio is 1.0 (normal) -> log10(1) = 0 -> penalty = 0
        # If ratio is 10x -> log10(10) = 1.0 -> penalty = 18.0
        # If ratio is 120x -> log10(120) = 2.08 -> penalty = 37.4
        safe_ratio=max(1.0,amount_to_mean_ratio)
        behavioral_penalty=np.log10(safe_ratio)*18.0

        # 3. Circadian Penalty (Night-time 1 AM - 5 AM)
        circadian_penalty=12.0 if is_night else 0

        # 4. Cross-Border International Penalty
        intl_penalty=22.0 if is_international else 0

        # 5. Composite Score Calculation
        composite_score=tree_risk+behavioral_penalty+circadian_penalty+intl_penalty

        # # If it's a verified structural anomaly with > 10x ratio, enforce critical floor
        # if is_anomaly and safe_ratio>10.0:
        #     composite_score=max(composite_score,85.0)

        final_score=round(max(0.0,min(99.0,composite_score)),1)
        final_anomaly=is_anomaly or (final_score>=70.0)

        return final_anomaly,final_score

fraud_model=FraudDetectionModel()
