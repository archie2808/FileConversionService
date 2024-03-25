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
    var conversionType = document.getElementById('conversionType').value;
    var actionUrl = conversionType === 'pdf' ? '/txt_to_pdf' : '/txt_to_docx';

    fetch(actionUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            // Parse and reject the promise if there are errors
            return response.json().then(data => Promise.reject(data));
        }
        // Handle successful conversion here (not implemented in the provided code)
    })
    .catch(error => {
        // Log and display errors from the conversion process
        console.error('Conversion error:', error);
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
