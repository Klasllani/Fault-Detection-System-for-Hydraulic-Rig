from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import numpy as np
from data_loader import load_data
from model import preprocess_data, train_model
from monitor import monitor_sensor_data, diagnose_fault
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
import json

app = Flask(__name__)

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/train', methods=['GET'])
def train():
    global model, scaler, feature_names
    
    sensor_files = [
        'PS1.txt', 'PS2.txt', 'PS3.txt', 'PS4.txt', 'PS5.txt', 'PS6.txt',
        'EPS1.txt', 'FS1.txt', 'FS2.txt', 'TS1.txt', 'TS2.txt', 'TS3.txt',
        'TS4.txt', 'VS1.txt', 'CE.txt', 'CP.txt', 'SE.txt'
    ]

    try:
        # Load data
        data = load_data(sensor_files, 'profile.txt')

        # Handle NaN values by filling with the mean of each column
        data = data.fillna(data.mean(numeric_only=True))

        # Features are the sensor data (excluding the last 5 columns which are targets)
        X = data.iloc[:, :-5]
        feature_names = X.columns.tolist()  # Save feature names for later use
        
        # Ensure the static directory exists
        os.makedirs('static', exist_ok=True)
        
        # Save feature names to a JSON file in the static folder
        with open('static/feature_names.json', 'w') as f:
            json.dump(feature_names, f)
            
        # Target: Create labels by combining component name and condition value
        profile_cols = ['cooler', 'valve', 'pump', 'accumulator', 'stable']
        # Find the column with the maximum value and create the label
        y = data[profile_cols].apply(lambda row: f"{row.idxmax()}_{row[row.idxmax()]}", axis=1)

        # Preprocess data
        X_normalized, scaler = preprocess_data(X)
        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)
        
        # Train model
        model = train_model(X_train, y_train)

        # Generate classification report
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)
        print(report)
        
        # Save some sample data for the frontend
        sample_data = {
            'features': feature_names,
            'sample_values': X.iloc[0].tolist(),
            'fault_types': list(set(y.tolist()))
        }
        
        with open('static/sample_data.json', 'w') as f:
            json.dump(sample_data, f)
        
        return jsonify({
            'status': 'success', 
            'message': 'Model trained successfully',
            'report': report,
            'features': feature_names
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/monitor', methods=['POST'])
def monitor():
    try:
        # Check if model and scaler are initialized
        if model is None or scaler is None:
            return jsonify({'error': 'Model not trained. Please train the model first.'}), 400
        
        incoming_data = request.json
        if not incoming_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Expected feature names (one per sensor)
        expected_features = ['PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'EPS1', 'FS1', 'FS2', 
                             'TS1', 'TS2', 'TS3', 'TS4', 'VS1', 'CE', 'CP', 'SE']
        
        # Create input data dictionary
        input_data = {}
        for feature in expected_features:
            if feature in incoming_data:
                input_data[feature] = float(incoming_data[feature])
            else:
                input_data[feature] = 0.0  # Default value if missing
        
        # Convert to DataFrame
        new_data = pd.DataFrame([input_data])
        
        # Handle NaN values
        new_data = new_data.fillna(0.0)
        
        # Make prediction
        prediction, confidence = monitor_sensor_data(model, scaler, new_data)
        diagnosis = diagnose_fault(prediction)
        
        return jsonify({
            'prediction': prediction,  # Already a string like 'accumulator_90'
            'confidence': float(confidence),
            'diagnosis': diagnosis
        })
        
    except ValueError as ve:
        return jsonify({'error': f'Value error: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/get_features', methods=['GET'])
def get_features():
    if feature_names:
        return jsonify({'features': feature_names})
    else:
        return jsonify({'error': 'Features not available. Please train the model first.'}), 400

if __name__ == '__main__':
    # Initialize model, scaler, and feature_names as None initially
    model = None
    scaler = None
    feature_names = None
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True)