import joblib
import json
import os
from config import RESULTS_DIR

def save_artifacts(model, metrics):
    try:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        
        # Save model
        model_path = os.path.join(RESULTS_DIR, 'model.pkl')
        joblib.dump(model, model_path)
        
        # Save metrics
        metrics_path = os.path.join(RESULTS_DIR, 'metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        
        return model_path, metrics_path
    except Exception as e:
        raise Exception(f"Saving artifacts failed: {str(e)}")