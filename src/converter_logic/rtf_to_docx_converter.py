import os
import subprocess
import tempfile
from io import BytesIO
from ..base_converter import BaseConverter
from ..logger_config import configure_logger
from ..utility import libreoffice_path

logger = configure_logger(__name__)


class RTFToDocxConverter(BaseConverter):
    """
    Converts RTF documents to DOCX format using LibreOffice.
    """

    def convert(self, output_stream: BytesIO):
        """
        Converts the input RTF (from input_stream) to a DOCX file, writing the result to output_stream.

        Parameters:
            output_stream (BytesIO): The stream to which the converted DOCX file will be written.

        Raises:
            RuntimeError: If the RTF to DOCX conversion process fails.
            FileNotFoundError: If the expected DOCX file is not created.
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            rtf_path = os.path.join(tmpdirname, "input.rtf")
            docx_path = os.path.join(tmpdirname, "input.docx")

            logger.info(f"Temporary RTF path: {rtf_path}")
            logger.info(f"Temporary DOCX path: {docx_path}")

            with open(rtf_path, 'wb') as tmp_rtf:
                tmp_rtf.write(self.input_stream.read())
            logger.info(f"Written RTF content to temporary file")
            cmd = [libreoffice_path, '--headless', '--convert-to', 'docx', '--outdir', tmpdirname, rtf_path]

            #logger.info(f"Executing command: {' '.join(cmd)}")

            try:
                subprocess.run(cmd, check=True, capture_output=True)
                logger.info("Conversion command executed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"LibreOffice conversion failed: {e.output}")
                raise RuntimeError("LibreOffice conversion failed.")

            if not os.path.exists(docx_path):
                logger.error("The expected DOCX file was not created.")
                raise FileNotFoundError("The expected DOCX file was not created.")

            with open(docx_path, 'rb') as docx_file:
                output_stream.write(docx_file.read())

            return output_stream
