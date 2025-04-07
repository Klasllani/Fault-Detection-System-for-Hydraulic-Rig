import pandas as pd
import os
import numpy as np

def load_data(sensor_files, profile_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'condition+monitoring+of+hydraulic+systems')
    
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found at {data_dir}")
    
    sensor_data_list = []
    column_names = []
    
    for sensor_file in sensor_files:
        file_path = os.path.join(data_dir, sensor_file)
        try:
            if not os.path.exists(file_path):
                print(f"Warning: File {sensor_file} not found at {file_path}")
                continue
                
            # Read the file
            sensor_df = pd.read_csv(file_path, delimiter='\t', header=None, dtype='float32')
            
            # Reduce each cycle to a single value (mean)
            base_name = os.path.splitext(sensor_file)[0]
            sensor_mean = sensor_df.mean(axis=1)  # Mean across all data points in a cycle
            sensor_df = pd.DataFrame(sensor_mean, columns=[base_name])
            column_names.append(base_name)
            
            sensor_data_list.append(sensor_df.reset_index(drop=True))
            
        except Exception as e:
            print(f"Error loading {sensor_file}: {str(e)}")
            continue
    
    if not sensor_data_list:
        raise FileNotFoundError("No sensor data files were successfully loaded")
    
    # Ensure all dataframes have the same length
    min_length = min(df.shape[0] for df in sensor_data_list)
    sensor_data_list = [df.iloc[:min_length] for df in sensor_data_list]
    
    # Concatenate sensor data horizontally
    sensor_data = pd.concat(sensor_data_list, axis=1)
    
    # Load profile data
    profile_file_path = os.path.join(data_dir, profile_file)
    if not os.path.exists(profile_file_path):
        raise FileNotFoundError(f"Profile file not found at {profile_file_path}")
        
    profile_data = pd.read_csv(profile_file_path, delimiter='\t', header=None, dtype='int32')
    profile_data = profile_data.iloc[:min_length, :]  # Match the length of sensor data
    
    # Add column names for profile data
    profile_cols = ['cooler', 'valve', 'pump', 'accumulator', 'stable']
    profile_data.columns = profile_cols
    
    # Combine sensor and profile data
    data = pd.concat([sensor_data, profile_data], axis=1)
    
    return data