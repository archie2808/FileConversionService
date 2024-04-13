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
            submitFileForConversion(formData);
        }
    })
    .catch(error => {
        console.error('Validation error:', error);
        displayError('Validation request failed');
    });
});

function displayError(message) {
   alert(message);
}

function submitFileForConversion(formData) {
    var conversionType = document.getElementById('conversionType').value;
    formData.append('target_format', conversionType);

    var form = document.getElementById('uploadForm');

    if ([ 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'png'].includes(conversionType)) {
        form.action = '/convert_image';
    } else {
        form.action = '/convert';
    }

    let loadingTimeout = setTimeout(() => {
        document.getElementById('loadingSymbol').style.display = 'block';
        // Disable UI components to prevent further interactions
        document.getElementById('fileInput').disabled = true;
        document.getElementById('conversionType').disabled = true;
        document.querySelector('button[type="submit"]').disabled = true;
    }, 250);

    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        clearTimeout(loadingTimeout);
        if (!response.ok) {
            return response.json().then(error => Promise.reject(error));
        }
        const contentType = response.headers.get('Content-Type') || '';
        if (contentType.includes('application/json')) {
            return response.json().then(error => Promise.reject(error));
        } else {
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
        console.error('Error during conversion:', error);
        displayError(error.error || 'An error occurred during file conversion.');
    })
    .finally(() => {
        clearTimeout(loadingTimeout);
        document.getElementById('loadingSymbol').style.display = 'none';
        document.getElementById('fileInput').disabled = false;
        document.getElementById('conversionType').disabled = false;
        document.querySelector('button[type="submit"]').disabled = false;
    });
}


