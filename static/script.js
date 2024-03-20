// Event listener for form submission
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    // Determine the selected conversion type and set the appropriate URL
    var conversionType = document.getElementById('conversionType').value;
    var actionUrl = conversionType === 'pdf' ? '/txt_to_pdf' : '/txt_to_docx';

    fetch(actionUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Extract filename from Content-Disposition header
        const contentDisp = response.headers.get('Content-Disposition');
        let filename = 'downloaded_file';
        if (contentDisp) {
            const matches = contentDisp.match(/filename="?([^"]+)"?/);
            if (matches && matches.length > 1) {
                filename = matches[1];
            }
        }
        return response.blob().then(blob => ({blob, filename}));
    })
    .then(({blob, filename}) => {
        // Create a URL for the blob and initiate download
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => console.error('Error:', error));
});

// Event listener for change in conversion type selection
document.getElementById('conversionType').addEventListener('change', function() {
    // No need to change the form action here; it's handled during the form submission
});
