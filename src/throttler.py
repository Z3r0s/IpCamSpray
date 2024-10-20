from sklearn.linear_model import LogisticRegression
import numpy as np

def train_anomaly_detector(response_times, statuses):
    X = np.array(response_times).reshape(-1, 1)
    y = [1 if status == 429 or status >= 500 else 0 for status in statuses]
    model = LogisticRegression()
    model.fit(X, y)
    return model

def should_throttle(model, response_time, status):
    return model.predict([[response_time]])[0] == 1