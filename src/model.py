from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def preprocess_data(data):
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data.iloc[:, :-5])
    return normalized_data, scaler

def train_model(X, y):
    model = RandomForestClassifier()
    model.fit(X, y)
    return model
