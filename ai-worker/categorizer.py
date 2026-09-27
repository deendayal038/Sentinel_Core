import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class TransactionCategorizeer:
    def __init__(self):
        self.model_path="categorizer_model.joblib"
        self.categories=[
            "FOOD DINING","UTILITIES_BILLS","INVESTMENT_WEALTH","TRAVEL_FUEL","ENTERTAINMENT","TRANSFER"
        ]
        self.model=self._load_or_train_model()

    def _load_or_train_model(self)-> RandomForestClassifier:
        """
        Model Persistence (joblib):
        If trained model exists on disk, load it in 5ms. 
        Otherwise, train and save it.
        """
        if os.path.exists(self.model_path):
            print(">>[Categorizer] loaded pre-trained model from disk (joblib)")
            return joblib.load(self.model_path)

        print(">>[Categorize] training new random forest classifier")
        np.random.seed(42)

        # Features: [amount, hour_of_day, is_weekend]
        # 1. FOOD: small amounts (₹100 - ₹1,200), lunch (12-15) and dinner (19-23)
        food_amounts=np.random.uniform(100,1200,(300,1))
        food_hours=np.random.choice([12,13,14,19,20,21,22],(300,1))
        food_weekend=np.random.choice([0,1],(300,1),p=[0.7,0.3])
        X_food=np.hstack([food_amounts,food_hours,food_weekend])
        Y_food=np.zeros(300) #Label 0

        # 2. UTILITIES: medium amounts (₹800 - ₹4,500), daytime (9-17), weekdays
        util_amounts=np.random.uniform(800,4500,(300,1))
        util_hours=np.random.randint(9,18,(300,1))
        util_weekend=np.zeros((300,1))
        X_util=np.hstack([util_amounts,util_hours,util_weekend])
        Y_util=np.ones(300) #Label 1

        # 3. INVESTMENT: large amounts (₹5,000 - ₹50,000), market hours (9-15), weekdays only
        inv_amounts=np.random.uniform(5000,50000,(300,1))
        inv_hours=np.random.randint(9,16,(300,1))
        inv_weekend=np.zeros((300,1))
        X_inv=np.hstack([inv_amounts,inv_hours,inv_weekend])
        Y_inv=np.full(300,2) #Label 2

        # 4. TRAVEL / FUEL: (₹300 - ₹3,500), commute hours (7-10, 17-21)
        tf_amounts=np.random.uniform(300,3500,(300,1))
        tf_hours=np.random.choice([7,8,9,17,18,19,20],(300,1))
        tf_weekend=np.random.choice([0,1],(300,1),p=[0.7,0.3])
        X_tf=np.hstack([tf_amounts,tf_hours,tf_weekend])
        Y_tf=np.full(300,3) #Label 3

        # 5. ENTERTAINMENT: (₹250 - ₹2,000), late evening & weekends (20-24)
        ent_amounts=np.random.uniform(250,2000,(300,1))
        ent_hours=np.random.choice([20,21,22,23],(300,1))
        ent_weekend=np.ones((300,1))
        X_ent=np.hstack([ent_amounts,ent_hours,ent_weekend])
        Y_ent=np.full(300,4) #Label 4

        # 6. TRANSFER (P2P Transfers, UPI/NEFT: ₹500 to ₹1,00,000, all hours, any day)
        tr_amounts=np.random.uniform(1,100000,(300,1))
        tr_hours=np.random.randint(0,24,(300,1))
        tr_weekend=np.random.choice([0,1],(300,1))
        X_tr=np.hstack([tr_amounts,tr_hours,tr_weekend])
        Y_tr=np.full(300,5) #Label 5

        #Combining datasets
        X=np.vstack([X_food,X_util,X_inv,X_tf,X_ent,X_tr])
        y=np.concatenate([Y_food,Y_util,Y_inv,Y_tf,Y_ent,Y_tr])

        # Train Random Forest (100 Decision Trees voting together)
        clf=RandomForestClassifier(n_estimators=100,random_state=42)
        clf.fit(X,y)

        # Save to disk using joblib (Model Persistence)
        joblib.dump(clf,self.model_path)
        print(">>[Categorizer] model trained and saved to disk as 'categorizer_model.joblib")
        return clf

    def predict_category(self,amount:float,hour:int,is_weekend:bool=False)->tuple[str,float]:

        features=np.array([[amount,hour,1 if is_weekend else 0]])

        class_idx=self.model.predict(features)[0]
        category_name=self.categories[int(class_idx)]

        probabilities=self.model.predict_proba(features)[0]
        confidence=round(float(np.max(probabilities))*100,1)
        if confidence<45.0:
            return "UNCATEGORIZED",confidence

        return category_name,confidence


categorizer=TransactionCategorizeer()