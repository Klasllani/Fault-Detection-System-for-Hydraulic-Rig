import numpy as np
import pandas as pd

def monitor_sensor_data(model, scaler, new_data):
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

def diagnose_fault(prediction, sensor_data=None):
    # Define the fault mapping
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
    
    # If sensor data is provided, check for extreme values
    if sensor_data is not None:
        # Extract sensor values
        ps_values = [sensor_data.get(f'PS{i}', 0) for i in range(1, 7)]
        ts_values = [sensor_data.get(f'TS{i}', 0) for i in range(1, 5)]
        vs1 = sensor_data.get('VS1', 0)
        ce = sensor_data.get('CE', 0)
        cp = sensor_data.get('CP', 0)
        se = sensor_data.get('SE', 0)
        fs_values = [sensor_data.get(f'FS{i}', 0) for i in range(1, 3)]
        eps1 = sensor_data.get('EPS1', 0)

        # Check for critical conditions
        if (any(ps > 300 or ps < 10 for ps in ps_values) or  # Extreme pressure
            any(ts > 60 for ts in ts_values) or             # Extreme temperature
            vs1 > 2.0 or                                    # Extreme vibration
            ce < 50 or                                      # Very low cooling efficiency
            cp < 0.5 or                                     # Very low cooling power
            se < 80):                                       # Very low efficiency factor
            return "Critical system failure"

        # Validate the prediction against expected ranges
        predicted_diagnosis = fault_mapping.get(prediction, "Unknown fault")
        
        if "optimal" in predicted_diagnosis.lower() or "full efficiency" in predicted_diagnosis.lower():
            # For "optimal" conditions, ensure values are within normal ranges
            if (any(ps < 100 or ps > 200 for ps in ps_values) or
                any(ts < 30 or ts > 50 for ts in ts_values) or
                vs1 < 0.3 or vs1 > 0.7 or
                ce < 90 or
                cp < 1.5 or cp > 2.5 or
                se < 95):
                return "Critical system failure due to extreme sensor values"
        elif "close to total failure" in predicted_diagnosis.lower():
            # For "close to total failure," ensure values are indeed extreme
            if (all(50 <= ps <= 300 for ps in ps_values) and
                all(30 <= ts <= 60 for ts in ts_values)):
                return "Mismatch: Sensor values do not indicate a total failure"
    
    # If no overrides, return the mapped diagnosis
    return fault_mapping.get(prediction, "Unknown fault")