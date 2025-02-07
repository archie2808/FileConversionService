from io import BytesIO

import docx

from ..base_converter import BaseConverter


class DOCXtoTXTConverter(BaseConverter):
    """
    Converter for transforming a DOCX file into a plain text file.

    Reads the contents of a DOCX file from input_stream, extracts the text, and writes
    it to the output_stream in plain text format. Inherits from BaseConverter and
    implements the convert method to perform this specific conversion.
    """

    def convert(self, output_stream: BytesIO):
        """
        Extracts text from DOCX and writes it as plain text to output_stream.

        Parameters:
            output_stream (BytesIO): The stream to which the extracted text will be written.

        Returns:
            The number of bytes written to output_stream.
        """

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
