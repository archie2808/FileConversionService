from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO, FileIO
import traceback
from logger_config import configure_logger
from converter_factory import ConverterFactory
import Config

app = Flask(__name__)
app.secret_key = 'secret_key'

logger = configure_logger(__name__)


@app.route('/')
def index():
    """
    Renders the main page of the file conversion service.

    Returns:
        A rendered template of Index.html which contains the user interface
        for uploading files and selecting the conversion type.
    """
    return render_template("Index.html")




@app.route('/convert', methods=['POST'])
def convert_file():
    if 'target_format' not in request.form:
        return jsonify({'error': 'Cannot convert same files'}), 400
    file = request.files['file']
    target_format = request.form['target_format'].lower()
    source_format = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''

    if source_format == target_format:
        return jsonify({'error': 'Source and target formats cannot be the same'}), 400

    input_stream = BytesIO(file.read())

    try:
        converter = ConverterFactory.get_converter(input_stream, source_format, target_format)
        output_stream = BytesIO()
        converter.convert(output_stream)

        mimetype = Config.mime_types.get(target_format, 'application/octet-stream')

        output_stream.seek(0)

        return send_file(output_stream, mimetype=mimetype, as_attachment=True, download_name= f"{file.filename.rsplit('.', 1)[0]}")
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Conversion failed: {traceback.format_exc()}")
        return jsonify({'error': 'Conversion failed'}), 500


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
    if not file.filename.endswith(('.txt', '.pdf', '.docx', '.rtf', 'csv', 'xlsx')):
        return jsonify({'error': 'Unsupported File Type'}), 400
    else:
        return jsonify({'message': 'File is valid'}), 200



if __name__ == '__main__':
    app.run(debug=True)
