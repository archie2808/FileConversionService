import os

from flask import Flask, render_template, request, jsonify, send_file
from conversionLogic import txt_to_pdf, txt_to_docx, docx_to_txt, pdf_to_docx, pdf_to_txt, docx_to_txt, pdf_to_txt, \
    docx_to_txt, docx_to_pdf
import io
import logging
import os


app = Flask(__name__)
app.secret_key = 'secret_key'

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    """
    Renders the main page of the file conversion service.

    Returns:
        A rendered template of Index.html which contains the user interface
        for uploading files and selecting the conversion type.
    """
    return render_template("Index.html")


def get_file_extension(filename):
    """Extract the file extension from a filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else None


@app.route('/convert_to_docx', methods=['POST'])
def convert_to_docx():
    """
          Converts uploaded files to DOCX.

          The function checks the file extension and calls the appropriate conversion function.
          Unsupported file types for conversion will result in an error message.

          Returns:
              - A DOCX file for download if conversion is successful.
              - JSON response with an error message if conversion fails or is not supported.
          """
    logging.info('Processing file conversion to DOCX')

    file = request.files['file']

    file_extension = get_file_extension(file.filename)
    logging.debug(f'File extension identified: {file_extension}')
    input_stream = io.BytesIO(file.read())
    output_stream = io.BytesIO()

    try:
        if file_extension == 'pdf':
            pdf_to_docx(input_stream, output_stream)
            logging.debug('PDF to DOCX conversion successful')

        elif file_extension == 'txt':
            input_data = file.read().decode('utf-8')
            doc = txt_to_docx(input_data)
            output_stream = io.BytesIO()
            doc.save(output_stream)
            output_stream.seek(0)
            logging.debug('TXT to DOCX conversion successful')

        elif file_extension == 'docx':
            return jsonify({'error': 'The file is already in DOCX format'}), 400

        if output_stream:
            output_stream.seek(0)
            download_name = f"{file.filename.rsplit('.', 1)[0]}"
            return send_file(output_stream,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=download_name)

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/convert_to_pdf', methods=['POST'])
def convert_to_pdf():
    """
        Converts uploaded files to PDF format.

        The function checks the file extension and calls the appropriate conversion function.
        If the uploaded file is already in PDF format, it returns an error message.
        Any other file types not supported for conversion will also result in an error message.

        Returns:
            - A PDF file for download if conversion is successful.
            - JSON response with an error message if conversion fails or is not supported.
        """
    try:
        file = request.files['file']
        file_extension = get_file_extension(file.filename)

        input_stream = io.BytesIO(file.read())
        output_stream = io.BytesIO()

        if file_extension == 'txt':
            input_data = input_stream.getvalue().decode('utf-8')
            txt_to_pdf(input_data, output_stream)

        elif file_extension == 'docx':
            docx_to_pdf(input_stream, output_stream)

        elif file_extension == 'pdf':
            return jsonify({'error': 'The attached file is of the same type as target type'}), 400

        output_stream.seek(0)
        download_name = f"{file.filename.rsplit('.', 1)[0]}.pdf"
        return send_file(
            output_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        return jsonify({'error': 'Internal server error during PDF conversion'}), 500


@app.route('/convert_to_txt', methods=['POST'])
def convert_to_txt():
    """
       Converts uploaded files to plain text format (TXT).

       The function checks the file extension and calls the appropriate conversion function.
       Unsupported file types for conversion will result in an error message.

       Returns:
           - A TXT file for download if conversion is successful.
           - JSON response with an error message if conversion fails or is not supported.
       """
    try:
        file = request.files['file']
        file_extension = get_file_extension(file.filename)
        text_content = ' '
        input_stream = io.BytesIO(file.read())

        if file_extension == 'pdf':
            text_content = pdf_to_txt(input_stream)
        elif file_extension == 'docx':
            text_content = docx_to_txt(input_stream)
        elif file_extension == 'txt':
            return jsonify({'error': 'The attached file is of the same type as target type'})


        output_stream = io.BytesIO()
        output_stream.write(text_content.encode('utf-8'))
        output_stream.seek(0)
        download_name = f"{file.filename.rsplit('.', 1)[0]}.txt"

        return send_file(
            output_stream,
            as_attachment=True,
            mimetype='text/plain',
            download_name=download_name
        )
    except Exception as e:
        return jsonify({'error': 'Internal server error during TXT conversion'}), 500
@app.route('/validate_file', methods=['POST'])
def validate_file():
    """Validates the uploaded file to ensure it meets the requirements for conversion.

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
        return jsonify({'error': 'Unsupported File Type'}), 400
    else:
        return jsonify({'message': 'File is valid'}), 200


if __name__ == '__main__':
    app.run(debug=True)
