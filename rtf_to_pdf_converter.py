from base_converter import BaseConverter
from io import BytesIO
import os
import tempfile
from Config import libreoffice_path
import subprocess
from logger_config import configure_logger

logger = configure_logger(__name__)


class RTFtoPDFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        with tempfile.TemporaryDirectory() as tmpdirname:
            rtf_path = os.path.join(tmpdirname, "input.rtf")
            pdf_path = os.path.join(tmpdirname, "input.pdf")  # Changed to "output.pdf" for clarity

            logger.info(f"Temporary RTF path: {rtf_path}")
            logger.info(f"Temporary PDF path: {pdf_path}")

            with open(rtf_path, 'wb') as tmp_rtf:
                tmp_rtf.write(self.input_stream.read())  # Ensure self.input_stream is used
            logger.info("Written RTF content to temporary file")

            cmd = [libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', tmpdirname, rtf_path]
            logger.info(f"Executing command: {' '.join(cmd)}")

            try:
                subprocess.run(cmd, check=True, capture_output=True)
                logger.info("Conversion command executed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"LibreOffice conversion failed: {e.stderr}")  # Use e.stderr.decode() if needed
                raise RuntimeError("LibreOffice conversion failed.")

            if not os.path.exists(pdf_path):
                logger.error("The expected PDF file was not created.")
                raise FileNotFoundError("The expected PDF file was not created.")

            with open(pdf_path, 'rb') as pdf_file:
                output_stream.write(pdf_file.read())

        return output_stream