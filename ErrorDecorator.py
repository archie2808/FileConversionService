
from functools import wraps
from flask import request, redirect, flash

def file_Validation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not file.filename.endswith(('.txt', '.pdf', '.docx')):
            flash('Invalid file type. Allowed types are: .txt, .pdf, .docx')
            return redirect(request.url)
        return f(*args, **kwargs)
    return decorated_function
