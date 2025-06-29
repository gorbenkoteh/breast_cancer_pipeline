import pandas as pd
from config import DATA_PATH

def load_dataset():
    try:
        df = pd.read_csv(DATA_PATH, header=None)
        columns = [
            'id', 'diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 
            'area_mean', 'smoothness_mean', 'compactness_mean', 'concavity_mean',
            'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
            'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
            'compactness_se', 'concavity_se', 'concave_points_se', 'symmetry_se',
            'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst',
            'area_worst', 'smoothness_worst', 'compactness_worst', 'concavity_worst',
            'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
        ]
        df.columns = columns
        df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
        return df
    except Exception as e:
        raise Exception(f"Data loading failed: {str(e)}")