from io import BytesIO
from base_converter import BaseConverter
import docx


class DOCXtoTXTConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):

        # Ensure the input stream is at the start
        self.input_stream.seek(0)

        # Load the DOCX file from the BytesIO object
        doc = docx.Document(self.input_stream)
        full_text = []

        # Extract all text from the document
        for para in doc.paragraphs:
            full_text.append(para.text)

        # Join all text pieces into a single string and write to the output stream
        output_text = '\n'.join(full_text)
        output_stream.write(output_text.encode('utf-8'))

        # Reset the stream position to the start for reading
        output_stream.seek(0)

        return output_stream
