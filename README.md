# Fault Detection System for a Hydraulic Rig Setup

## Overview
This project is designed to monitor and indentify faults in the circulation processes of an oil-based hydraulic rig. The parameters observed are temperature, pressure, flow rate, and pH. "Condition monitoring of hydraulic systems", a comprehensive public dataset from UCI, is used. Machine learning models like Scikit-learn and RandomForestClassifier are employed to diagnose the type and severity of faults, providing early warnings. Also included is a web-based interface for easy interaction and visualization.

## Running
After cloning the repo, download all required .txt files from the dataset linked below and ensure they are moved to the condition+monitoring+of+hydraulic+systems folder within the project. Ensure Python 3.6 or higher is installed on your system. Next, install the necessary libraries: Flask, pandas, numpy, and scikit-learn. Navigate to the project directory, ans start the Flask application by running app.py with Python. Follow the standard output to access the web browser visualizer. There, cick "Train Model" to train the model, input sensor values in the form, and click "Monitor System" to view the diagnosis. 

## Dataset Citation
Helwig, N., Pignanelli, E., & Schtze, A. (2015). Condition monitoring of hydraulic systems [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CW21.

## Acknowledgments
I would like to acknowledge the UCI Machine Learning Repository and the creators of the dataset, Nikolai Helwig, Eliseo Pignanelli, and Andreas Schütze, for providing the data used in this project. Proper credit should be given to them when using this dataset for any purpose.
