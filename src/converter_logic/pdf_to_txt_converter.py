from io import BytesIO
import fitz
from ..base_converter import BaseConverter


class PDFToTXTConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        """
        Extracts all text from a PDF file and writes it to an output BytesIO stream.

        Overrides the convert method in the BaseConverter class to provide specific
        functionality for converting PDF to TXT.

        Returns:
        BytesIO: An output stream containing all text extracted from the PDF document.
        """

        self.input_stream.seek(0)

        text = ''
        with fitz.open(stream=self.input_stream) as doc:
            for page in doc:
                text += page.get_text()

        output_stream.write(text.encode('utf-8'))

        output_stream.seek(0)

        return output_stream
