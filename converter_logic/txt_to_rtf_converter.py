from io import BytesIO
from base_converter import BaseConverter


class TXTtoRTFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        # RTF header, document area start, and footer. Adjust formatting as needed.
        rtf_header = r"{\rtf1\ansi\deff0{\fonttbl{\f0\fswiss Arial;}}\f0\pard "
        rtf_footer = r"\par}"

        input_text = self.input_stream.getvalue().decode('utf-8')

        # Escape RTF special characters in the input text
        escaped_text = input_text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\par\n')

        # Assemble the RTF content
        rtf_content = f"{rtf_header}{escaped_text}{rtf_footer}"

        output_stream.write(rtf_content.encode('utf-8'))
