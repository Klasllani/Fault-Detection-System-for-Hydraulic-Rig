# Fault Detection System for a Hydraulic Rig Setup

## Overview
This project is designed to monitor and indentify faults in the circulation processes of an oil-based hydraulic rig. The parameters observed are temperature, pressure, flow rate, and pH. "Condition monitoring of hydraulic systems", a comprehensive public dataset from UCI, is used. Machine learning models like Scikit-learn and RandomForestClassifier are employed to diagnose the type and severity of faults, providing early warnings and subsequent action. Also included is a web-based interface for easy interaction and visualization.

## Running
Ensure Python 3.6 or higher is on your system and install the necessary libraries: Flask, pandas, numpy, and scikit-learn. Clone the repo, navigate to the project directory, and start the Flask application with app.py. Follow the terminal output to access the web browser visualizer. There: click "Train Model" to train the model, input sensor values in the form, and click "Monitor System" to view the diagnosis. 

## Dataset Citation
Helwig, N., Pignanelli, E., & Schtze, A. (2015). Condition monitoring of hydraulic systems [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CW21.
