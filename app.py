from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import io
import os
from docx2pdf import convert

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

@app.route('/')
def index():
    return 'File conversion service'

@app.route('/convert', methods=['POST'])
def convert_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # File conversion logic
    if file and file.filename.endswith('.docx'):
        # Save DOCX file temporarily
        temp_docx = 'temp.docx'
        file.save(temp_docx)

        # Convert to PDF
        temp_pdf = 'temp.pdf'
        convert(temp_docx, temp_pdf)

        # Read the generated PDF file
        result = io.BytesIO()
        with open(temp_pdf, 'rb') as pdf_file:
            result.write(pdf_file.read())
        result.seek(0)  # Reset the position to the start of the stream

        # Remove the temporary files
        os.remove(temp_docx)
        os.remove(temp_pdf)

        # Return the converted file
        return send_file(result, attachment_filename = 'converted.pdf', as_attachment=True)

    else:
        flash('Invalid file type. Please upload a .docx file')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
