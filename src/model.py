from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

def preprocess_data(data):
    # Create a scaler
    scaler = StandardScaler()
    
    # Handle potential NaN values
    data_clean = data.copy()
    data_clean = data_clean.fillna(data_clean.mean())
    
    # Normalize the data
    normalized_data = scaler.fit_transform(data_clean)
    
    return normalized_data, scaler

def train_model(X, y):
    # Create and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model
