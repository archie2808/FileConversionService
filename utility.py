import os
import pyclamd

libreoffice_path = os.getenv('LIBREOFFICE_PATH', '/Applications/LibreOffice.app/Contents/MacOS/soffice')

mime_types = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'rtf': 'application/rtf',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv': 'text/csv'

}
image_mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'tiff': 'image/tiff',
            'bmp': 'image/bmp'

        }

def scan_file_with_clamav(file_path):
    cd = pyclamd.ClamdUnixSocket()

    try:
        scan_result = cd.scan_file(file_path)
        if scan_result:

            return scan_result
    except Exception as e:
        print(f"An error occurred during ClamAV scan: {e}")


        return {'error': 'Failed to scan the file'}

    # Return None if the file is clean
    return None