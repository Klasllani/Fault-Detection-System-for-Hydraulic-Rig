document.getElementById('monitor-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect input values for all sensors (single cycle of data)
    const ps1 = document.getElementById('ps1').value;
    const ps2 = document.getElementById('ps2').value;
    const ps3 = document.getElementById('ps3').value;
    const ps4 = document.getElementById('ps4').value;
    const ps5 = document.getElementById('ps5').value;
    const ps6 = document.getElementById('ps6').value;
    const eps1 = document.getElementById('eps1').value;
    const fs1 = document.getElementById('fs1').value;
    const fs2 = document.getElementById('fs2').value;
    const ts1 = document.getElementById('ts1').value;
    const ts2 = document.getElementById('ts2').value;
    const ts3 = document.getElementById('ts3').value;
    const ts4 = document.getElementById('ts4').value;
    const vs1 = document.getElementById('vs1').value;
    const ce = document.getElementById('ce').value;
    const cp = document.getElementById('cp').value;
    const se = document.getElementById('se').value;

    // Create a single row of data matching the training data structure
    const data = {
        PS1: parseFloat(ps1),
        PS2: parseFloat(ps2),
        PS3: parseFloat(ps3),
        PS4: parseFloat(ps4),
        PS5: parseFloat(ps5),
        PS6: parseFloat(ps6),
        EPS1: parseFloat(eps1),
        FS1: parseFloat(fs1),
        FS2: parseFloat(fs2),
        TS1: parseFloat(ts1),
        TS2: parseFloat(ts2),
        TS3: parseFloat(ts3),
        TS4: parseFloat(ts4),
        VS1: parseFloat(vs1),
        CE: parseFloat(ce),
        CP: parseFloat(cp),
        SE: parseFloat(se)
    };

    // Send the data as a single-row DataFrame (array with one object)
    fetch('/monitor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify([data]) // Wrap in array to match DataFrame expectation
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result').innerText = `Prediction: ${result.prediction}, Diagnosis: ${result.diagnosis}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
