function displayResponse(data) {
    // Get the main response text
    const text = data.response;
    
    // Format the response with markdown-like parsing
    let formattedText = text
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
        
    // Create tool info display if a tool was used
    if (data.tool_used) {
        let toolInfoHTML = `<div class="tool-info">
            <h4>🔍 Agent used tool: ${data.tool_used}</h4>`;
            
        // Add tool-specific details if available
        if (data.tool_used === 'poi_search' && data.tool_details) {
            // Add city information
            if (data.tool_details.city_name) {
                toolInfoHTML += `<p><strong>Location:</strong> ${data.tool_details.city_name}`;
                
                // Add coordinates if available
                if (data.tool_details.city_coordinates) {
                    const [lat, lon] = data.tool_details.city_coordinates;
                    toolInfoHTML += ` (${lat.toFixed(4)}, ${lon.toFixed(4)})`;
                }
                
                toolInfoHTML += `</p>`;
            }
            
            // Add points of interest list
            if (data.tool_details.nearby_pois && data.tool_details.nearby_pois.length > 0) {
                toolInfoHTML += `<p><strong>Found ${data.tool_details.nearby_pois.length} points of interest within 2km:</strong></p>`;
                toolInfoHTML += `<ul class="poi-list">`;
                
                data.tool_details.nearby_pois.forEach(poi => {
                    toolInfoHTML += `<li>${poi.name} (${poi.distance_km} km)</li>`;
                });
                
                toolInfoHTML += `</ul>`;
            } else {
                toolInfoHTML += `<p>No points of interest found in this location.</p>`;
            }
        }
        
        toolInfoHTML += `</div>`;
        
        // Add tool info before the main response
        formattedText = toolInfoHTML + formattedText;
    }
    
    responseContainer.innerHTML = formattedText;
}document.addEventListener('DOMContentLoaded', function() {
// Elements
const promptInput = document.getElementById('prompt-input');
const generateBtn = document.getElementById('generate-btn');
const responseContainer = document.getElementById('response-container');
const loadingSpinner = document.getElementById('loading-spinner');
const modelInfo = document.getElementById('model-info');

// Fetch available models
fetchModels();

// Event listener for generate button
generateBtn.addEventListener('click', generateResponse);

// Event listener for Enter key in textarea
promptInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && event.ctrlKey) {
        event.preventDefault();
        generateResponse();
    }
});

function generateResponse() {
    const prompt = promptInput.value.trim();
    
    if (!prompt) {
        alert('Please enter a prompt first.');
        return;
    }
    
    // Show loading spinner
    loadingSpinner.style.display = 'block';
    generateBtn.disabled = true;
    
    // Clear previous response
    responseContainer.innerHTML = '';
    
    // Make API request
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            displayError(data.error);
        } else {
            displayResponse(data);
        }
    })
    .catch(error => {
        displayError('Error: ' + error.message);
    })
    .finally(() => {
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        generateBtn.disabled = false;
    });
}

function displayResponse(data) {
    // Get the main response text
    const text = data.response;
    
    // Format the response with markdown-like parsing
    let formattedText = text
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
        
    // Create tool info display if a tool was used
    if (data.tool_used) {
        let toolInfoHTML = `<div class="tool-info">
            <h4>💡 Agent used tool: ${data.tool_used}</h4>`;
            
        // Add tool-specific details if available
        if (data.tool_used === 'city_search' && data.tool_details) {
            if (data.tool_details.found) {
                toolInfoHTML += `<p>City found: <strong>${data.tool_details.exact_match}</strong></p>`;
            } else if (data.tool_details.similar_matches && data.tool_details.similar_matches.length > 0) {
                toolInfoHTML += `<p>Similar cities found: <strong>${data.tool_details.similar_matches.join(', ')}</strong></p>`;
            } else {
                toolInfoHTML += `<p>No matching city found.</p>`;
            }
        }
        
        toolInfoHTML += `</div>`;
        
        // Add tool info before the main response
        formattedText = toolInfoHTML + formattedText;
    }
    
    responseContainer.innerHTML = formattedText;
}

function displayError(errorMessage) {
    responseContainer.innerHTML = `<p class="error">${errorMessage}</p>`;
}

function fetchModels() {
    fetch('/models')
        .then(response => response.json())
        .then(data => {
            if (data.models) {
                modelInfo.innerHTML = 'Available models: ' + data.models.join(', ');
            } else {
                modelInfo.innerHTML = 'No model information available';
            }
        })
        .catch(error => {
            modelInfo.innerHTML = 'Error fetching model information';
            console.error('Error:', error);
        });
}
});