from flask import Flask, render_template, request, jsonify, send_file
from conversionLogic import convert_txt_to_pdf, convert_txt_to_docx, convert_docx_to_txt
import io

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    """
    Renders the main page of the file conversion service.

    Returns:
        A rendered template of Index.html which contains the user interface
        for uploading files and selecting the conversion type.
    """
    return render_template("Index.html")

@app.route('/convert_to_pdf', methods=['POST'])
def txt_to_PDF():
    """
    Converts a text file to PDF format and sends the converted file back to the client.

    The function retrieves a file from the request, converts it to PDF using
    the convert_txt_to_pdf function from the conversionLogic module, and returns
    the PDF file as a response to the client.

    Returns:
        A Flask response object containing the converted PDF file, or a JSON
        object with an error message if an exception occurs.
    """
    try:
        file = request.files['file']
        return_data = io.BytesIO()
        input_data = file.read().decode('utf-8')
        convert_txt_to_pdf(input_data, return_data)
        return_data.seek(0)
        original_filename = file.filename.rsplit(".", 1)[0]  # Removes extension from the original file name
        download_name = f"{original_filename}.pdf"
        return send_file(
            return_data,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/validate_file', methods=['POST'])
def validate_file():
    """
    Validates the uploaded file to ensure it meets the requirements for conversion.

    The function checks if the file exists in the request, if a file is selected,
    and if the file type is one of the allowed types (.txt, .pdf, .docx). It returns
    a JSON message indicating success or describing the validation error.

    Returns:
        A JSON response indicating the result of the validation process.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not file.filename.endswith(('.txt', '.pdf', '.docx')):
        return jsonify({'error': 'Invalid file type. Allowed types are: .txt, .pdf, .docx'}), 400
    else:
        return jsonify({'message': 'File is valid'}), 200

@app.route('/convert_to_docx', methods=['POST'])
def txt_to_docx():
    """
    Converts a text file to DOCX format and sends the converted file back to the client.

    Similar to txt_to_PDF, but for DOCX conversion using convert_txt_to_docx from the
    conversionLogic module.

    Returns:
        A Flask response object containing the converted DOCX file, or a JSON
        object with an error message if an exception occurs.
    """
    try:
        file = request.files['file']
        input_data = file.read().decode('utf-8')
        doc = convert_txt_to_docx(input_data)
        output_stream = io.BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)
        download_name = f"{file.filename.rsplit('.', 1)[0]}.docx"
        return send_file(
            output_stream,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/convert_to_txt', methods=['POST'])
def docx_to_txt():
    """
    Converts a DOCX file to plain text format and sends the text back to the client.

    Uses the convert_docx_to_txt function from the conversionLogic module to perform
    the conversion.

    Returns:
        A JSON response containing the converted text, or an error message if
        the conversion fails.
    """
    try:
        file = request.files['file']
        text = convert_docx_to_txt(file)
        return jsonify({'text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
