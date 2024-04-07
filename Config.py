import os

libreoffice_path = os.getenv('LIBREOFFICE_PATH', '/Applications/LibreOffice.app/Contents/MacOS/soffice')

mime_types = {
    'pdf': 'application/pdf',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'rtf': 'application/rtf',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv': 'text/csv'

}
