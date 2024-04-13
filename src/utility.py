import os
import pyclamd
from logger_config import configure_logger

logger = configure_logger(__name__)

"""
Utility module for file conversion service.

This module provides helper functions and constants used throughout the file conversion service,
including paths to external tools, MIME type mappings, and interfacing with ClamAV for malware scanning.
"""

# Path to the LibreOffice executable. This is used for document conversions.
# The path can be specified via an environment variable; otherwise, a default path is used.
libreoffice_path = os.getenv('LIBREOFFICE_PATH', '/usr/bin/libreoffice')

# Mapping of file extensions to their MIME types. This is used for setting the Content-Type
# in HTTP responses when sending files to the client.
mime_types = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'rtf': 'application/rtf',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv': 'text/csv'
}

# mapping for image file extensions to their respective MIME types.
image_mime_types = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'tiff': 'image/tiff',
    'bmp': 'image/bmp'
}


import pyclamd

def scan_file_with_clamav(file_path):
    """
    Scans a file for malware using ClamAV.

    This function interfaces with a running ClamAV daemon to scan a specified file for malware.
    If malware is detected, the scan result is returned; otherwise, None is returned, indicating
    the file is clean. If an error occurs during the scan, an error dictionary is returned.

    Parameters:
        file_path (str): The path to the file to be scanned.

    Returns:
        dict: The scan result if malware is detected or an error occurs.
        None: If the file is clean or no malware is detected.
    """
    # Update to use ClamdNetworkSocket for TCP connection
    cd = pyclamd.ClamdNetworkSocket('clamav', 3310)

    try:
        scan_result = cd.scan_file(file_path)
        if scan_result:

            for key, value in scan_result.items():
                return {key: value}
    except Exception as e:
        logger.debug(f"An error occurred during ClamAV scan: {e}")
        return {'error': 'Failed to scan the file', 'details': str(e)}

    # Return None if the file is clean
    return None

