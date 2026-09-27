import pandas as pd
import numpy as np

def extract_behavioral_features(current_amount:float,past_amounts:list[float],is_night:bool)->dict:

    if past_amounts and len(past_amounts)>0:
        avg_spending=float(np.mean(past_amounts))
        amount_to_mean_ratio=round(current_amount/max(avg_spending,1.0),2)

    else:
        avg_spending=current_amount
        amount_to_mean_ratio=1.0

    # Log magnitude factor (Smooth scaling for large numbers)
    log_magnitude=round(float(np.log10(max(current_amount,10.0))),2)

    return {
        "customer_avg_spending":round(avg_spending,2),
        "amount_to_mean_ratio":amount_to_mean_ratio,
        "log_magnitude":log_magnitude
    }