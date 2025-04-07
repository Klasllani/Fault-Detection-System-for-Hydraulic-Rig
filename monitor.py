import numpy as np
import pandas as pd

def monitor_sensor_data(model, scaler, new_data):
    """
    Process new sensor data and make predictions
    
    Args:
        model: Trained machine learning model
        scaler: Fitted StandardScaler
        new_data: DataFrame with new sensor readings
        
    Returns:
        Tuple of (prediction, confidence)
    """
    try:
        # Transform the data using the scaler
        normalized_new_data = scaler.transform(new_data)
        
        # Make prediction
        prediction = model.predict(normalized_new_data)
        probabilities = model.predict_proba(normalized_new_data)
        
        # Get the confidence (probability of the predicted class)
        confidence = np.max(probabilities, axis=1)[0]
        
        return prediction[0], confidence
    except ValueError as e:
        print(f"Error in data structure: {str(e)}")
        raise ValueError(f"Data structure mismatch: {str(e)}")

def diagnose_fault(prediction):
    """
    Map numerical prediction to human-readable diagnosis
    
    Args:
        prediction: Model prediction (string)
        
    Returns:
        String with fault diagnosis
    """
    fault_mapping = {
        'cooler_3': "Cooler close to total failure",
        'cooler_20': "Cooler reduced efficiency",
        'cooler_100': "Cooler full efficiency",
        'valve_73': "Valve close to total failure",
        'valve_80': "Valve severe lag",
        'valve_90': "Valve small lag",
        'valve_100': "Valve optimal switching behavior",
        'pump_0': "Internal pump no leakage",
        'pump_1': "Internal pump weak leakage",
        'pump_2': "Internal pump severe leakage",
        'accumulator_90': "Hydraulic accumulator close to total failure",
        'accumulator_100': "Hydraulic accumulator severely reduced pressure",
        'accumulator_115': "Hydraulic accumulator slightly reduced pressure",
        'accumulator_130': "Hydraulic accumulator optimal pressure",
        'stable_0': "Conditions were stable",
        'stable_1': "Conditions might not be stable"
    }
    
    # Convert prediction to string if necessary
    pred_str = str(prediction)
    return fault_mapping.get(pred_str, "Unknown fault")