from io import BytesIO
from base_converter import BaseConverter
import fitz
import io


class PDFToRTFConverter(BaseConverter):
    """
    Converts PDF documents to RTF format.
    """

    def convert(self, output_stream: BytesIO):
        """
        Converts the input PDF (from input_stream) to RTF format, writing the result to output_stream.

        Parameters:
            output_stream (BytesIO): The stream to which the RTF data will be written.

        Returns:
            The output stream with the RTF data.
        """
        doc = fitz.open(stream=self.input_stream, filetype="pdf")
        rtf_text = "{\\rtf1\\ansi\\deff0\\pard "

        for page in doc:
            text = page.get_text()
            rtf_text += text.replace('\n', '\\par\n') + '\\par\n'

        rtf_text += "}"


        output_stream.write(rtf_text.encode('utf-8'))


        output_stream.seek(0)

        return output_stream
