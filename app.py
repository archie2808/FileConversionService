from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from new1 import convert_txt_to_pdf
import io
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Index.html")

@app.route('/convert', methods=['POST'])
def convert_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # If user does not select file, browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and file.filename.endswith('.txt'):
        # Convert TXT to PDF in memory
        return_data = io.BytesIO()
        input_data = file.read().decode('utf-8')
        convert_txt_to_pdf(input_data, return_data)
        return_data.seek(0)

        return send_file(
            return_data,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted.pdf'
        )

    else:
        flash('Invalid file type. Please upload a .txt file')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)