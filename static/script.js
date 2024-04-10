/**
 * Submits the file upload form and handles validation and conversion.
 *
 * This script captures the form submission event, prevents the default form submission action,
 * and uses fetch to send the file to a server-side validation endpoint. If the server identifies
 * an error with the file, it displays an alert with the error message. Otherwise, it proceeds
 * to submit the file for conversion.
 */
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission behavior.

    // Prepare the form data for submission.
    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    // Send the file to the server for validation.
    fetch('/validate_file', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json()) // Parse the JSON response from the server.
    .then(data => {
        if (data.error) {
            // If there's an error (e.g., validation error), display it.
            displayError(data.error);
        } else {
            // If validation succeeds, proceed to file conversion.
            submitFileForConversion(formData);
        }
    })
    .catch(error => {
        // Handle any errors that occur during the fetch operation.
        console.error('Validation error:', error);
        displayError('Validation request failed');
    });
});

/**
 * Displays an error message to the user.
 * @param {string} message - The error message to be displayed.
 */
function displayError(message) {
    alert(message); // Use an alert to display the error message.
}

/**
 * Submits the file for conversion.
 * Determines the conversion endpoint based on the selected file type.
 * @param {FormData} formData - The FormData object containing the file to be converted.
 */
function submitFileForConversion(formData) {
    var conversionType = document.getElementById('conversionType').value;
    formData.append('target_format', conversionType);

    // Determine the correct action based on the selected conversion type.
    var form = document.getElementById('uploadForm');
    if ([ 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'png'].includes(conversionType)) {
        form.action = '/convert_image';
    } else {
        form.action = '/convert';
    }

    // Display a loading indicator and disable UI components.
    let loadingTimeout = setTimeout(() => {
        document.getElementById('loadingSymbol').style.display = 'flex';
        document.getElementById('fileInput').disabled = true;
        document.getElementById('conversionType').disabled = true;
        document.querySelector('button[type="submit"]').disabled = true;
    }, 100); // Delay to ensure UI updates if conversion is quick.

    // Perform the conversion request to the server.
    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        clearTimeout(loadingTimeout); // Clear the loading timeout upon response.
        if (!response.ok) {
            // If response is not OK, parse and reject the error.
            return response.json().then(error => Promise.reject(error));
        }
        // Handle the response
        return response.blob().then(blob => {
            return {
                blob: blob,
                filename: response.headers.get('Content-Disposition').split('filename=')[1].replaceAll('"', '')
            };
        });
    })
    .then(({ blob, filename }) => {
        // Create a URL for the blob and initiate a download.
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'downloaded_file';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })
    .catch(error => {
        // Log and display any errors during conversion.
        console.error('Error during conversion:', error);
        displayError(error.error || 'An error occurred during file conversion.');
    })
    .finally(() => {
        // Re-enable UI components and hide the loading indicator.
        document.getElementById('loadingSymbol').style.display = 'none';
        document.getElementById('fileInput').disabled = false;
        document.getElementById('conversionType').disabled = false;
        document.querySelector('button[type="submit"]').disabled = false;
    });
}


