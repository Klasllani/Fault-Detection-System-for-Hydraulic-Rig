import pandas as pd
import os
import numpy as np

def load_data(sensor_files, profile_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(project_root, 'condition+monitoring+of+hydraulic+systems')
    
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
                
            # Read the file and create column names based on file name
            sensor_df = pd.read_csv(file_path, delimiter='\t', header=None, dtype='float32')
            
            # Create meaningful column names
            base_name = os.path.splitext(sensor_file)[0]
            if sensor_df.shape[1] == 1:
                # If there's only one column, use the filename as column name
                sensor_df.columns = [base_name]
                column_names.append(base_name)
            else:
                # For multiple columns, append index
                cols = [f"{base_name}_{i}" for i in range(sensor_df.shape[1])]
                sensor_df.columns = cols
                column_names.extend(cols)
            
            # Downsample by taking every 10th row
            sensor_df = sensor_df.iloc[::10, :]
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
    profile_data = profile_data.iloc[::10, :min_length].T  # Transpose and take same number of rows
    
    # Add column names for profile data
    profile_cols = ['cooler', 'valve', 'pump', 'accumulator', 'stable']
    profile_data.columns = profile_cols
    
    # Combine sensor and profile data
    data = pd.concat([sensor_data, profile_data], axis=1)
    
    return data
