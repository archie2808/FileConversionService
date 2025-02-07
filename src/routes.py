import os
import traceback
from io import BytesIO
from . import utility
from . converter_factory import ConverterFactory
from flask import Flask, render_template, request, jsonify, send_file, Blueprint
from . logger_config import configure_logger
from werkzeug.utils import secure_filename


logger = configure_logger(__name__)
main = Blueprint('main', __name__)




@main.route('/')
def index():
    """
    Renders the main page of the file conversion service.

    Returns:
        A rendered template of Index.html which contains the user interface
        for uploading files and selecting the conversion type.
    """
    return render_template("Index.html")


@main.route('/convert', methods=['POST'])
def convert_file():
    """
    Handles file conversion requests. Validates the request form and file,
     performs the conversion based on the target format specified by the user,
    and sends the converted file back as a response.

    Returns:
        send_file: Sends the converted file as an attachment to the user if successful.
        jsonify: Returns a JSON object with an error message if the conversion fails or if validation fails.
    """
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


@main.route('/convert_image', methods=['POST'])
def convert_image():
    """
        Handles image conversion requests specifically. Similar to convert_file, but
        optimized for image files. Uses a different set of MIME types..

        Returns:
            send_file: Sends the converted image file as an attachment if successful.
            jsonify: Returns a JSON object with an error message if the conversion fails or if validation fails
        """
    file = request.files['file']
    target_format = request.form['target_format'].lower()

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


@main.route('/validate_file', methods=['POST'])
def validate_file():
    """
       Validates the uploaded file for presence and non-emptiness, then performs
       a malware scan using ClamAV. Returns a message indicating whether the file
       is safe to process or not.

       Returns:
           jsonify: Returns a JSON object indicating the file is valid and safe, or
           containing an error if the file is found to be malicious or if the scan fails.
       """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Ensure the filename is secure
        filename = secure_filename(file.filename)
        logger.info(f"Validating file: {filename}")

        # Use the configured TMPDIR for temporary file storage
        temp_path = os.path.join(os.getenv('TMPDIR', '/tmp'), filename)
        file.save(temp_path)

        # Perform the ClamAV file scan
        scan_result = utility.scan_file_with_clamav(temp_path)

        # Clean up the temporary file
        os.remove(temp_path)

        if scan_result is not None:
            # If malware is detected, return an error
            return jsonify({'error': 'Malicious file detected', 'details': scan_result}), 400
        else:
            return jsonify({'message': 'File is valid and safe to process'}), 200
    except Exception as e:
        logger.error(f"An error occurred during file validation: {e}")
        return jsonify({'error': 'Failed to validate the file: ' + str(e)}), 500




