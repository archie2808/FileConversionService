from io import BytesIO
from ..base_converter import BaseConverter


class TXTtoRTFConverter(BaseConverter):
    """
    Converts plain text to RTF format.

    This converter generates RTF content from plain text input, applying basic RTF
    formatting to the output.
    """

    def convert(self, output_stream: BytesIO):
        """
        Creates RTF formatted text from the input plain text and writes it to the provided stream.

        Parameters:
            output_stream (BytesIO): The stream to write the RTF content to.
        """
        # RTF header, document area start, and footer.
        rtf_header = r"{\rtf1\ansi\deff0{\fonttbl{\f0\fswiss Arial;}}\f0\pard "
        rtf_footer = r"\par}"

        input_text = self.input_stream.getvalue().decode('utf-8')

        escaped_text = input_text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\par\n')

        rtf_content = f"{rtf_header}{escaped_text}{rtf_footer}"

        output_stream.write(rtf_content.encode('utf-8'))
