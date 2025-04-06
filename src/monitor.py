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
        Prediction result
    """
    # Handle missing columns by filling with zeros
    try:
        # Transform the data using the scaler
        normalized_new_data = scaler.transform(new_data)
        
        # Make prediction
        prediction = model.predict(normalized_new_data)
        return prediction
    except ValueError as e:
        # If there's a mismatch in the number of features
        print(f"Error in data structure: {str(e)}")
        raise ValueError(f"Data structure mismatch: {str(e)}")

def diagnose_fault(prediction):
    """
    Map numerical prediction to human-readable diagnosis
    
    Args:
        prediction: Model prediction (array-like)
        
    Returns:
        String with fault diagnosis
    """
    fault_mapping = {
        0: "Cooler close to total failure",
        1: "Cooler reduced efficiency",
        2: "Cooler full efficiency",
        3: "Valve optimal switching behavior",
        4: "Valve small lag",
        5: "Valve severe lag",
        6: "Valve close to total failure",
        7: "Internal pump no leakage",
        8: "Internal pump weak leakage",
        9: "Internal pump severe leakage",
        10: "Hydraulic accumulator optimal pressure",
        11: "Hydraulic accumulator slightly reduced pressure",
        12: "Hydraulic accumulator severely reduced pressure",
        13: "Hydraulic accumulator close to total failure",
        14: "Conditions were stable"
    }
    
    # Handle case where prediction is an array
    if hasattr(prediction, '__iter__'):
        pred_value = prediction[0]
    else:
        pred_value = prediction
        
    return fault_mapping.get(pred_value, "Unknown fault")
