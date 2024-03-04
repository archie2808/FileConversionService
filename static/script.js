document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

fetch('/txt_to_docx', {
    method: 'POST',
    body: formData
})
.then(response => {
    // Extract filename from Content-Disposition header
    const contentDisp = response.headers.get('Content-Disposition');
    let filename = 'downloaded_file';
    if (contentDisp) {
        filename = contentDisp.split('filename=')[1];
        if (filename) {
            filename = filename.replace(/['"]/g, ''); // Remove any quotes from the filename
        }
    }
    return response.blob().then(blob => ({blob, filename}));
})
.then(({blob, filename}) => {
    // Create a URL for the blob
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
})
.catch(error => console.error('Error:', error));


document.getElementById('conversionType').addEventListener('change', function() {
    var form = document.getElementById('uploadForm');
    var conversionType = this.value;
    if(conversionType === 'pdf') {
        form.action = '/txt_to_pdf';
    } else if(conversionType === 'docx') {
        form.action = '/txt_to_docx';
    }
})}