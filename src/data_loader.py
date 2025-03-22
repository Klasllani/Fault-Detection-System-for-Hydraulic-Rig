import pandas as pd
import os

def load_data(sensor_files, profile_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    data_dir = os.path.join(project_root, 'condition+monitoring+of+hydraulic+systems')
    
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found at {data_dir}")
    
    sensor_data = []
    for sensor_file in sensor_files:
        file_path = os.path.join(data_dir, sensor_file)
        try:
            if not os.path.exists(file_path):
                print(f"Warning: File {sensor_file} not found at {file_path}")
                continue
            # Load data in chunks and downsample by taking every 10th row
            chunks = pd.read_csv(file_path, delimiter='\t', chunksize=10000, dtype='float32')
            sensor_df = pd.concat([chunk.iloc[::10, :] for chunk in chunks], ignore_index=True)
            sensor_data.append(sensor_df)
        except Exception as e:
            print(f"Error loading {sensor_file}: {str(e)}")
            continue
    
    if not sensor_data:
        raise FileNotFoundError("No sensor data files were successfully loaded")
    
    # Concatenate sensor data
    sensor_data = pd.concat(sensor_data, axis=1)
    
    # Load profile data (also downsample to match)
    profile_file_path = os.path.join(data_dir, profile_file)
    if not os.path.exists(profile_file_path):
        raise FileNotFoundError(f"Profile file not found at {profile_file_path}")
    profile_data = pd.read_csv(profile_file_path, delimiter='\t', dtype='int32').iloc[::10, :]
    
    # Combine sensor and profile data
    data = pd.concat([sensor_data, profile_data], axis=1)
    return data
