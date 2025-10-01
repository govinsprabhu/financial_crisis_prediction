document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    if (!fileInput.files.length) return;
    formData.append('image', fileInput.files[0]);

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<div style="text-align: center; color: #007bff;">Analyzing image for vehicles...</div>';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.error) {
            resultDiv.innerHTML = '<div style="color: #dc3545; text-align: center;">Error: ' + data.error + '</div>';
        } else if (data.labels && data.labels.length > 0) {
            let resultHTML = '<div style="text-align: left;">';
            resultHTML += '<h3 style="color: #28a745; margin-bottom: 15px;">Vehicle Detection Results</h3>';
            resultHTML += '<p><strong>Analysis Method:</strong> ' + data.method + '</p>';
            
            if (data.vehicle_count) {
                resultHTML += '<p><strong>Vehicles Detected:</strong> ' + data.vehicle_count + '</p>';
            }
            
            resultHTML += '<div style="margin-top: 15px;"><strong>Detected Items:</strong></div>';
            resultHTML += '<ul style="list-style-type: none; padding-left: 0;">';
            
            data.labels.forEach((label, index) => {
                const isVehicle = label.includes('Vehicle Type:');
                const isMilitary = label.includes('(Military)');
                let itemClass = 'list-item';
                let icon = '🚗';
                
                if (isVehicle) {
                    if (isMilitary) {
                        itemClass += ' military';
                        icon = '🛡️';
                    } else {
                        itemClass += ' civilian';
                        icon = '🚙';
                    }
                } else {
                    icon = '📷';
                }
                
                resultHTML += `<li class="${itemClass}" style="margin: 8px 0; padding: 8px; border-left: 3px solid #007bff; background: #f8f9fa;">
                    <span style="font-size: 1.2em; margin-right: 8px;">${icon}</span>
                    ${label}
                </li>`;
            });
            
            resultHTML += '</ul></div>';
            resultDiv.innerHTML = resultHTML;
        } else {
            resultDiv.innerHTML = '<div style="text-align: center; color: #6c757d;">No vehicles or objects detected in this image.</div>';
        }
    } catch (err) {
        resultDiv.innerHTML = '<div style="color: #dc3545; text-align: center;">Error analyzing image. Please try again.</div>';
        console.error('Error:', err);
    }
});
