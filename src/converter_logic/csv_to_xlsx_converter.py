import pandas as pd
from io import BytesIO
from src.base_converter import BaseConverter


class CSVtoXLSXConverter(BaseConverter):
    """
    Converter for transforming a CSV file into an XLSX file.

    Inherits from BaseConverter and implements the convert method to read a CSV
    file from the input_stream, convert it to XLSX format, and write the result
    to the output_stream.
    """

    def convert(self, output_stream: BytesIO):
        """
        Reads CSV from input_stream, converts it to XLSX, and writes to output_stream.

        Parameters:
            output_stream (BytesIO): The stream to write the converted XLSX file to.

        Returns:
            The number of bytes written to output_stream.
        """

        self.input_stream.seek(0)

        df = pd.read_csv(self.input_stream)

        # Convert the DataFrame to XLSX and write to the output stream
        with BytesIO() as intermediate_stream:
            df.to_excel(intermediate_stream, index=False)
            intermediate_stream.seek(0)
            return output_stream.write(intermediate_stream.read())
