/**
 * Submits the file upload form and handles validation and conversion.
 *
 * This script captures the form submission event, prevents the default form submission action,
 * and uses fetch to send the file to a server-side validation endpoint. If the server identifies
 * an error with the file, it displays an alert with the error message. Otherwise, it proceeds
 * to submit the file for conversion.
 */
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from submitting immediately

    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    // Validate the file by sending it to the validation endpoint
    fetch('/validate_file', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Display error message if validation fails
            displayError(data.error);
        } else {
            // Proceed with file conversion if validation succeeds
            submitFileForConversion(formData);
        }
    })
    .catch(error => {
        console.error('Validation error:', error);
        displayError('Validation request failed');
    });
});

/**
 * Displays an error message using an alert.
 *
 * @param {string} message - The error message to be displayed.
 */
function displayError(message) {
   alert(message);
}

/**
 * Submits the file for conversion based on the selected conversion type.
 *
 * After successful validation, this function submits the file to the appropriate
 * conversion endpoint using fetch. It handles the server's response, including
 * displaying errors if the conversion fails.
 *
 * @param {FormData} formData - The FormData object containing the file to be converted.
 */
function submitFileForConversion(formData) {
    // Append the selected conversion type to the FormData object
    var conversionType = document.getElementById('conversionType').value;
    formData.append('target_format', conversionType);

    // Perform the fetch request to the single /convert endpoint
    fetch('/convert', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        // Check if the response is OK (status 200-299)
        if (!response.ok) {
            // If not OK, attempt to parse it as JSON for the error message
            return response.json().then(error => Promise.reject(error));
        }
        // Check the content type of the response
        const contentType = response.headers.get('Content-Type') || '';
        if (contentType.includes('application/json')) {
            // If the response is JSON, there might be an error message
            return response.json().then(error => Promise.reject(error));
        } else {
            // If the response is not JSON, assume it's a file to be downloaded
            return response.blob().then(blob => {
                return {
                    blob: blob,
                    filename: response.headers.get('Content-Disposition').split('filename=')[1].replaceAll('"', '')
                };
            });
        }
    })
    .then(({ blob, filename }) => {

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'downloaded_file';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })
    .catch(error => {
        // Handle JSON errors or network issues
        console.error('Error during conversion:', error);
        displayError(error.error || 'An error occurred during file conversion.');
    });
}


/**
 * Event listener for change in conversion type selection.
 *
 * This part of the script is reserved for handling changes in the conversion
 * type selection by the user, which could be extended for additional functionality.
 */
document.getElementById('conversionType').addEventListener('change', function() {
    // This part remains unchanged
});