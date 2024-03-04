from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, send_file

import io

def file_Validation(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        file = request.files['file']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not file or not file.filename.endswith(('.txt', '.pdf', '.docx')):
            flash('Invalid file type.')
            return redirect(request.url)
        return f(*args, **kwargs)
    return decorated_function