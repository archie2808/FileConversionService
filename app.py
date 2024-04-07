from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO, FileIO
import traceback
from logger_config import configure_logger
from converter_factory import ConverterFactory
from werkzeug.utils import secure_filename
import utility
import os

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

        mimetype = utility.mime_types.get(target_format, 'application/octet-stream')

        output_stream.seek(0)

        return send_file(output_stream, mimetype=mimetype, as_attachment=True, download_name= f"{file.filename.rsplit('.', 1)[0]}")
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Conversion failed: {traceback.format_exc()}")
        return jsonify({'error': 'Conversion failed'}), 500


@app.route('/convert_image', methods=['POST'])
def convert_image():
    logger.debug("hiya")
    file = request.files['file']
    target_format = request.form['target_format'].lower()

    # Infer the source format from the file extension
    source_format = file.filename.rsplit('.', 1)[-1].lower()

    input_stream = BytesIO(file.read())
    output_stream = BytesIO()

    try:
        converter = ConverterFactory.get_converter(input_stream, source_format, target_format)
        converter.convert(output_stream)
        logger.debug(f"Converting from {source_format} to {target_format}")
        output_stream.seek(0)
        mime_types = utility.image_mime_types.get(target_format, 'image')
        return send_file(output_stream, mimetype=mime_types, as_attachment=True, download_name=f"{file.filename.rsplit('.', 1)[0]}")
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return jsonify({'error': 'Conversion failed: ' + str(e)}), 500


@app.route('/validate_file', methods=['POST'])
def validate_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the filename is secure
    filename = secure_filename(file.filename)

    temp_path = os.path.join('/tmp', filename)
    file.save(temp_path)

    # Perform the ClamAV file scan
    scan_result = utility.scan_file_with_clamav(temp_path)


    os.remove(temp_path)

    if scan_result is not None:
        # If malware is detected, return an error
        return jsonify({'error': 'Malicious file detected', 'details': scan_result}), 400

    # If no malware is detected, proceed with further validation
    # (file type check, etc.)

    return jsonify({'message': 'File is valid and safe to process'}), 200


if __name__ == '__main__':
    app.run(debug=True)
