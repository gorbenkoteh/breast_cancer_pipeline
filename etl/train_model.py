from sklearn.linear_model import LogisticRegression
from config import RANDOM_STATE

def train_model(X_train, y_train):
    try:
        model = LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
            class_weight='balanced'
        )
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        raise Exception(f"Model training failed: {str(e)}")