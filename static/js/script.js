// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    const trainButton = document.getElementById('train-button');
    const trainStatus = document.getElementById('train-status');
    const monitorForm = document.getElementById('monitor-form');
    const resultDiv = document.getElementById('result');
    
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
                trainStatus.innerHTML = `<p class="error">Training failed: ${error}</p>`;
                console.error('Error:', error);
            });
    });
    
    // Monitor form submission
    monitorForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Collect form data
        const formData = new FormData(monitorForm);
        const data = {};
        
        // Convert form data to JavaScript object
        for (const [key, value] of formData.entries()) {
            if (value) {
                data[key] = parseFloat(value);
            } else {
                data[key] = 0;
            }
        }
        
        // Send the data to the server
        fetch('/monitor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'Network response was not ok');
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
            resultDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
            console.error('Error:', error);
        });
    });
    
    // Helper function to get severity level
    function getSeverityLevel(diagnosis) {
        if (diagnosis.includes("close to total failure")) {
            return "Critical";
        } else if (diagnosis.includes("severe") || diagnosis.includes("severely")) {
            return "High";
        } else if (diagnosis.includes("reduced") || diagnosis.includes("small lag") || diagnosis.includes("weak")) {
            return "Medium";
        } else if (diagnosis.includes("optimal") || diagnosis.includes("full efficiency") || diagnosis.includes("no leakage") || diagnosis.includes("stable")) {
            return "Low";
        } else {
            return "Unknown";
        }
    }
    
    // Helper function to provide recommended actions
    function getRecommendedAction(diagnosis) {
        if (diagnosis.includes("Cooler")) {
            if (diagnosis.includes("close to total failure")) {
                return "Replace cooling system immediately.";
            } else if (diagnosis.includes("reduced efficiency")) {
                return "Schedule maintenance for cooling system.";
            } else {
                return "Continue regular monitoring.";
            }
        } else if (diagnosis.includes("Valve")) {
            if (diagnosis.includes("close to total failure")) {
                return "Replace valve immediately.";
            } else if (diagnosis.includes("severe lag")) {
                return "Service valve urgently.";
            } else if (diagnosis.includes("small lag")) {
                return "Schedule valve inspection.";
            } else {
                return "Continue regular monitoring.";
            }
        } else if (diagnosis.includes("pump")) {
            if (diagnosis.includes("severe leakage")) {
                return "Replace pump seals immediately.";
            } else if (diagnosis.includes("weak leakage")) {
                return "Schedule pump maintenance.";
            } else {
                return "Continue regular monitoring.";
            }
        } else if (diagnosis.includes("accumulator")) {
            if (diagnosis.includes("close to total failure")) {
                return "Replace hydraulic accumulator immediately.";
            } else if (diagnosis.includes("severely reduced")) {
                return "Recharge or service accumulator urgently.";
            } else if (diagnosis.includes("slightly reduced")) {
                return "Schedule accumulator service.";
            } else {
                return "Continue regular monitoring.";
            }
        } else if (diagnosis.includes("stable")) {
            return "All systems operating normally.";
        } else {
            return "Consult maintenance manual.";
        }
    }
});
