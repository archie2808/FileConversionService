/**
 * Handles the file upload and conversion process within a web form.
 * This script intercepts the form submission, validates the file on the server, and manages the file conversion process.
 * It provides user feedback and handles errors throughout the process.
 */

// Add an event listener to the form submission
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    // Prepare the file data from the form for sending
    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    // Send the file data to the server for validation
    fetch('/validate_file', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Display an error message if the server finds an issue with the file
            displayError(data.error);
        } else {
            // Proceed to submit the file for conversion if validation is successful
            submitFileForConversion(formData);
        }
    })
    .catch(error => {
        // Log and display errors if the validation process fails
        console.error('Validation error:', error);
        displayError('Validation request failed');
    });
});

// Display an error message to the user
function displayError(message) {
   alert(message);
}

// Handle the file conversion process after successful validation
function submitFileForConversion(formData) {
    var conversionType = document.getElementById('conversionType').value;
    formData.append('target_format', conversionType);

    var form = document.getElementById('uploadForm');

    // Set the appropriate action URL based on the conversion type
    if (['jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'png'].includes(conversionType)) {
        form.action = '/convert_image';
    } else {
        form.action = '/convert';
    }

    // Display a loading symbol and disable UI components to prevent further user actions during conversion
    let loadingTimeout = setTimeout(() => {
        document.getElementById('loadingSymbol').style.display = 'block';
        document.getElementById('fileInput').disabled = true;
        document.getElementById('conversionType').disabled = true;
        document.querySelector('button[type="submit"]').disabled = true;
    }, 250);

    // Perform the file conversion request
    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            clearTimeout(loadingTimeout);
            if (!response.ok) {
                // Handle non-200 responses and pass any errors to the catch block
                return response.json().then(error => Promise.reject(error));
            }
            // Handle the response, assuming binary data unless it's JSON (error message)
            const contentType = response.headers.get('Content-Type') || '';
            if (contentType.includes('application/json')) {
                return response.json().then(error => Promise.reject(error));
            } else {
                // Process the binary data to create a downloadable file link
                return response.blob().then(blob => {
                    return {
                        blob: blob,
                        filename: response.headers.get('Content-Disposition').split('filename=')[1].replaceAll('"', '')
                    };
                });
            }
        })
        .then(({blob, filename}) => {
            // Create a temporary link and trigger the download
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename || 'downloaded_file';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        })
        .catch(error => {
            // Display conversion errors
            console.error('Error during conversion:', error);
            displayError(error.error || 'An error occurred during file conversion.');
        })
        .finally(() => {
            // Reset UI components regardless of success or failure
            document.getElementById('loadingSymbol').style.display = 'none';
            document.getElementById('fileInput').disabled = false;
            document.getElementById('conversionType').disabled = false;
            document.querySelector('button[type="submit"]').disabled = false;
        });
}


