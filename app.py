from flask import Flask, render_template, request, redirect, url_for, flash, send_file, make_response
from new1 import convert_txt_to_pdf, convert_txt_to_docx
from ErrorDecorator import file_Validation
import io


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Index.html")

@app.route('/txt_to_pdf', methods=['POST'])
@file_Validation
def convert_file():

    file = request.files['file']

    # Convert TXT to PDF in memory
    return_data = io.BytesIO()
    input_data = file.read().decode('utf-8')
    convert_txt_to_pdf(input_data, return_data)
    return_data.seek(0)
    original_filename = file.filename.rsplit(".", 1)[0]  # removes extension from the original file name
    download_name = f"{original_filename}.pdf"
    return send_file(
        return_data,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=download_name
        )



@app.route('/txt_to_docx', methods=['POST'])
@file_Validation
def txt_to_docx():
    file = request.files['file']
    input_data = file.read().decode('utf-8')
    doc = convert_txt_to_docx(input_data)
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)
    # Correctly call send_file and directly return its response
    return send_file(
        output_stream,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name=f"{file.filename}"
    )




if __name__ == '__main__':
    app.run(debug=True)