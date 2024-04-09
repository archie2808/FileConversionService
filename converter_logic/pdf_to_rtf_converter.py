from io import BytesIO
from base_converter import BaseConverter
import fitz
import io


class PDFToRTFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        doc = fitz.open(stream=self.input_stream, filetype="pdf")
        rtf_text = "{\\rtf1\\ansi\\deff0\\pard "

        for page in doc:
            text = page.get_text()
            rtf_text += text.replace('\n', '\\par\n') + '\\par\n'

        rtf_text += "}"
        output_stream = io.BytesIO(rtf_text.encode('utf-8'))
        return output_stream

