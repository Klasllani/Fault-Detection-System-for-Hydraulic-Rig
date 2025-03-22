from flask import Flask, request, jsonify
import pandas as pd
from data_loader import load_data
from model import preprocess_data, train_model
from monitor import monitor_sensor_data, diagnose_fault
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

app = Flask(__name__)

sensor_files = [
    'PS1.txt', 'PS2.txt', 'PS3.txt', 'PS4.txt', 'PS5.txt', 'PS6.txt',
    'EPS1.txt', 'FS1.txt', 'FS2.txt', 'TS1.txt', 'TS2.txt', 'TS3.txt',
    'TS4.txt', 'VS1.txt', 'CE.txt', 'CP.txt', 'SE.txt'
]

# Load data
data = load_data(sensor_files, 'profile.txt')

# Handle NaN values by filling with the mean of each column
data = data.fillna(data.mean(numeric_only=True))

X = data.iloc[:, :-5]
y = data.iloc[:, -5:].idxmax(axis=1)

X_normalized, scaler = preprocess_data(data)
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)
model = train_model(X_train, y_train)

# Print classification report
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

@app.route('/monitor', methods=['POST'])
def monitor():
    try:
        incoming_data = request.json
        if not incoming_data:
            return jsonify({'error': 'No data provided'}), 400
            
        new_data = pd.DataFrame(incoming_data)
        if new_data.empty:
            return jsonify({'error': 'Invalid data format'}), 400
            
        # Handle NaN values in incoming data
        new_data = new_data.fillna(new_data.mean(numeric_only=True))
        
        prediction = monitor_sensor_data(model, scaler, new_data)
        diagnosis = diagnose_fault(prediction)
        return jsonify({'prediction': prediction.tolist(), 'diagnosis': diagnosis})
        
    except ValueError as ve:
        return jsonify({'error': f'Value error: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
