import tempfile
import subprocess
import os
from io import BytesIO
from logger_config import configure_logger
from base_converter import BaseConverter
from Config import libreoffice_path

logger = configure_logger(__name__)


class DocxToPDFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):

        with tempfile.TemporaryDirectory() as tmpdirname:
            docx_path = os.path.join(tmpdirname, "input.docx")
            pdf_path = os.path.join(tmpdirname, "input.pdf")

            with open(docx_path, 'wb') as tmp_docx:
                tmp_docx.write(self.input_stream.read())

            try:
                subprocess.run([libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', tmpdirname, docx_path],
                               check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                logger.error(f"LibreOffice conversion failed: {e.stderr}")
                raise RuntimeError("Failed to convert DOCX to PDF using LibreOffice.")

            if not os.path.exists(pdf_path):
                logger.error("Expected PDF file was not created.")
                raise FileNotFoundError("Expected PDF file was not created.")

            with open(pdf_path, 'rb') as pdf_file:
                output_stream.write(pdf_file.read())

        return output_stream
