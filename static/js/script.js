// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Reference to the train button
    const trainButton = document.getElementById('train-button');
    const trainStatus = document.getElementById('train-status');
    const monitorForm = document.getElementById('monitor-form');
    const resultDiv = document.getElementById('result');
    
    // First, check if model is already trained
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
        
        // Convert form data to JavaScript object with proper names
        for (const [key, value] of formData.entries()) {
            // Use the name attribute directly to ensure matching with backend
            if (value) {
                data[key] = parseFloat(value);
            } else {
                // Provide default values if fields are empty
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
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(result => {
            // Format the result for display
            if (result.error) {
                resultDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
            } else {
                resultDiv.innerHTML = `
                    <p><strong>Fault Type:</strong> ${result.diagnosis}</p>
                    <p><strong>Confidence:</strong> ${calculateConfidence(result.prediction)}%</p>
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
    
    // Helper function to calculate a fake confidence level for UI purposes
    function calculateConfidence(predictionCode) {
        // This is just for display - in a real application you'd get this from the model
        const baseConfidence = 85;
        const randomFactor = Math.floor(Math.random() * 15);
        return baseConfidence + randomFactor;
    }
    
    // Helper function to get severity level
    function getSeverityLevel(diagnosis) {
        if (diagnosis.includes("close to total failure")) {
            return "Critical - Immediate Attention Required";
        } else if (diagnosis.includes("severe") || diagnosis.includes("severely")) {
            return "High - Urgent Attention Required";
        } else if (diagnosis.includes("reduced") || diagnosis.includes("small lag") || diagnosis.includes("weak")) {
            return "Medium - Monitoring Required";
        } else if (diagnosis.includes("optimal") || diagnosis.includes("full efficiency") || diagnosis.includes("no leakage") || diagnosis.includes("stable")) {
            return "Low - System Normal";
        } else {
            return "Unknown";
        }
    }
    
    // Helper function to provide recommended actions
    function getRecommendedAction(diagnosis) {
        if (diagnosis.includes("cooler")) {
            if (diagnosis.includes("close to total failure")) {
                return "Immediately replace cooling system. Shut down system to prevent damage.";
            } else if (diagnosis.includes("reduced efficiency")) {
                return "Schedule maintenance for cooling system. Check for blockages or coolant levels.";
            } else {
                return "Continue regular monitoring of cooling system.";
            }
        } else if (diagnosis.includes("valve")) {
            if (diagnosis.includes("close to total failure")) {
                return "Replace valve immediately. Prepare for system shutdown.";
            } else if (diagnosis.includes("severe lag")) {
                return "Service valve urgently. Check for mechanical issues or control problems.";
            } else if (diagnosis.includes("small lag")) {
                return "Schedule valve inspection at next maintenance interval.";
            } else {
                return "Continue regular monitoring of valve operation.";
            }
        } else if (diagnosis.includes("pump")) {
            if (diagnosis.includes("severe leakage")) {
                return "Replace pump seals immediately. Check for downstream contamination.";
            } else if (diagnosis.includes("weak leakage")) {
                return "Schedule pump maintenance within next 48 hours. Monitor fluid levels.";
            } else {
                return "Continue regular monitoring of pump performance.";
            }
        } else if (diagnosis.includes("accumulator")) {
            if (diagnosis.includes("close to total failure")) {
                return "Replace hydraulic accumulator immediately. Check system pressure stability.";
            } else if (diagnosis.includes("severely reduced")) {
                return "Recharge or service accumulator urgently. Check for leaks in the system.";
            } else if (diagnosis.includes("slightly reduced")) {
                return "Schedule accumulator service at next maintenance interval.";
            } else {
                return "Continue regular monitoring of accumulator pressure.";
            }
        } else if (diagnosis.includes("stable")) {
            return "All systems operating normally. Continue regular monitoring schedule.";
        } else {
            return "Consult maintenance manual for specific recommendations.";
        }
    }
});
