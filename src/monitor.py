def monitor_sensor_data(model, scaler, new_data):
    normalized_new_data = scaler.transform(new_data.iloc[:, :-5])
    prediction = model.predict(normalized_new_data)
    return prediction

def diagnose_fault(prediction):
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
    return fault_mapping.get(prediction[0], "Unknown fault")
