from io import BytesIO
import tempfile
from pdf2docx import Converter
from src.logger_config import configure_logger
from src.base_converter import BaseConverter

logger = configure_logger(__name__)


class PDFToDocxConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        """
        Converts a PDF file to DOCX format using the pdf2docx library.

        This method overrides the convert method in the BaseConverter class to provide specific
        functionality for converting PDF to DOCX.

        Raises:
        - RuntimeError: If the conversion process fails.
        """

        with tempfile.NamedTemporaryFile(delete=True, suffix='.pdf') as temp_pdf_file, \
                tempfile.NamedTemporaryFile(delete=True, suffix='.docx') as temp_docx_file:


            self.input_stream.seek(0)
            temp_pdf_file.write(self.input_stream.read())
            temp_pdf_file.flush()

            input_pdf_path = temp_pdf_file.name
            output_docx_path = temp_docx_file.name

            try:
                cv = Converter(input_pdf_path)
                cv.convert(output_docx_path)
                cv.close()
            except Exception as e:
                logger.error(f"PDF to DOCX conversion failed: {e}")
                raise RuntimeError("Failed to convert PDF to DOCX.")


            with open(output_docx_path, 'rb') as docx_file:
                output_stream.write(docx_file.read())

                output_stream.seek(0)
                return output_stream
