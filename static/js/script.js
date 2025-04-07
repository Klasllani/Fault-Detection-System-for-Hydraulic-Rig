// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const trainButton = document.getElementById('train-button');
    const trainStatus = document.getElementById('train-status');
    const monitorButton = document.getElementById('monitor-button');
    const resultDiv = document.getElementById('result');
    const sensorForm = document.getElementById('sensor-form');
    
    // Check if model is already trained
    fetch('/get_features')
        .then(response => {
            if (response.ok) {
                trainStatus.innerHTML = '<p class="success">Model is trained and ready to use</p>';
                return response.json();
            } else {
                trainStatus.innerHTML = '<p class="error">Model not trained yet. Please train the model first.</p>';
                throw new Error('Model not trained');
            }
        })
        .catch(error => {
            console.error('Error checking model status:', error);
            trainStatus.innerHTML = '<p class="error">Error checking model status: ' + error.message + '</p>';
        });
    
    // Train button click event
    trainButton.addEventListener('click', function() {
        trainStatus.innerHTML = '<p>Training model... This may take a moment.</p>';
        
        fetch('/train')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    trainStatus.innerHTML = `<p class="success">Model trained successfully!<br>
                                           Accuracy metrics:</p>
                                           <pre>${data.report}</pre>`;
                } else {
                    trainStatus.innerHTML = `<p class="error">Error: ${data.message}</p>`;
                }
            })
            .catch(error => {
                trainStatus.innerHTML = `<p class="error">Training failed: ${error.message}</p>`;
                console.error('Error:', error);
            });
    });
    
    // Monitor button click event
    monitorButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent any default form submission behavior
        
        // Validate form
        if (!sensorForm.checkValidity()) {
            sensorForm.reportValidity();
            resultDiv.innerHTML = '<p class="error">Please fill in all required fields with valid numbers.</p>';
            return;
        }
        
        // Collect form data
        const formData = new FormData(sensorForm);
        const sensorData = {};
        let hasInvalidInput = false;
        
        formData.forEach((value, key) => {
            const numValue = parseFloat(value);
            if (isNaN(numValue)) {
                hasInvalidInput = true;
                return;
            }
            sensorData[key] = numValue;
        });
        
        if (hasInvalidInput) {
            resultDiv.innerHTML = '<p class="error">Invalid input: All sensor values must be valid numbers.</p>';
            return;
        }
        
        // Send the sensor data to the /monitor endpoint
        fetch('/monitor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sensorData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'Failed to process sensor data');
                });
            }
            return response.json();
        })
        .then(result => {
            if (result.error) {
                resultDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
            } else {
                resultDiv.innerHTML = `
                    <p><strong>Fault Type:</strong> ${result.diagnosis}</p>
                    <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(2)}%</p>
                    <p><strong>Severity:</strong> ${getSeverityLevel(result.diagnosis)}</p>
                    <p><strong>Recommended Action:</strong> ${getRecommendedAction(result.diagnosis)}</p>
                `;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p class="error">Error processing sensor data: ${error.message}</p>`;
            console.error('Error:', error);
        });
    });
    
    // Helper function to get severity level
    function getSeverityLevel(diagnosis) {
        // Critical conditions
        if (diagnosis.includes("Critical system failure")) {
            return "Critical";
        } else if (diagnosis.includes("close to total failure")) {
            return "Critical";
        }
        // High severity conditions
        else if (diagnosis.includes("severe") || diagnosis.includes("severely")) {
            return "High";
        } else if (diagnosis.includes("might not be stable")) {
            return "High";
        }
        // Medium severity conditions
        else if (diagnosis.includes("reduced") || diagnosis.includes("small lag") || diagnosis.includes("weak")) {
            return "Medium";
        } else if (diagnosis.includes("Mismatch")) {
            return "Medium";
        }
        // Low severity conditions
        else if (diagnosis.includes("optimal") || diagnosis.includes("full efficiency") || diagnosis.includes("no leakage") || diagnosis.includes("stable")) {
            return "Low";
        }
        // Unknown severity
        else {
            return "Unknown";
        }
    }
    
    // Helper function to provide recommended actions
    function getRecommendedAction(diagnosis) {
        // Critical conditions
        if (diagnosis.includes("Critical system failure")) {
            return "Shut down the system immediately, inspect all components, and check for overpressure or overheating issues.";
        } else if (diagnosis.includes("Cooler close to total failure")) {
            return "Shut down the system and replace the cooling system immediately to prevent overheating.";
        } else if (diagnosis.includes("Valve close to total failure")) {
            return "Shut down the system and replace the valve immediately to restore proper flow and pressure.";
        } else if (diagnosis.includes("Hydraulic accumulator close to total failure")) {
            return "Shut down the system and replace the hydraulic accumulator immediately to prevent pressure loss.";
        }
        // High severity conditions
        else if (diagnosis.includes("Valve severe lag")) {
            return "Schedule an urgent valve service to prevent potential failure; monitor pressure and flow closely.";
        } else if (diagnosis.includes("Internal pump severe leakage")) {
            return "Schedule an urgent pump repair to replace seals and prevent further leakage; monitor pressure and motor power.";
        } else if (diagnosis.includes("Hydraulic accumulator severely reduced pressure")) {
            return "Schedule an urgent accumulator recharge or replacement; monitor pressure and vibration levels.";
        } else if (diagnosis.includes("Conditions might not be stable")) {
            return "Investigate potential instability causes, such as high vibration or low efficiency, and schedule a system inspection.";
        }
        // Medium severity conditions
        else if (diagnosis.includes("Cooler reduced efficiency")) {
            return "Schedule maintenance for the cooling system to improve efficiency; monitor temperatures closely.";
        } else if (diagnosis.includes("Valve small lag")) {
            return "Schedule a valve inspection to address the lag; monitor pressure and flow for any changes.";
        } else if (diagnosis.includes("Internal pump weak leakage")) {
            return "Schedule pump maintenance to address the leakage; monitor pressure and motor power for worsening conditions.";
        } else if (diagnosis.includes("Hydraulic accumulator slightly reduced pressure")) {
            return "Schedule an accumulator service to restore pressure; monitor pressure and vibration levels.";
        } else if (diagnosis.includes("Mismatch: Sensor values do not indicate a total failure")) {
            return "Review sensor data for inconsistencies and verify the system's actual condition; schedule a diagnostic check.";
        }
        // Low severity conditions
        else if (diagnosis.includes("Cooler full efficiency")) {
            return "Continue regular monitoring; cooling system is operating normally.";
        } else if (diagnosis.includes("Valve optimal switching behavior")) {
            return "Continue regular monitoring; valve is operating normally.";
        } else if (diagnosis.includes("Internal pump no leakage")) {
            return "Continue regular monitoring; pump is operating normally.";
        } else if (diagnosis.includes("Hydraulic accumulator optimal pressure")) {
            return "Continue regular monitoring; accumulator is operating normally.";
        } else if (diagnosis.includes("Conditions were stable")) {
            return "Continue regular monitoring; system is stable and operating normally.";
        }
        // Unknown fault
        else {
            return "Consult the maintenance manual for further diagnosis and troubleshooting steps.";
        }
    }
});