document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    fetch('/txt_to_docx', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        // Create a URL for the blob
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'converted.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('conversionType').addEventListener('change', function() {
    var form = document.getElementById('uploadForm');
    var conversionType = this.value;
    if(conversionType === 'pdf') {
        form.action = '/convert_to_pdf';
    } else if(conversionType === 'docx') {
        form.action = '/convert_to_docx';
    }
});