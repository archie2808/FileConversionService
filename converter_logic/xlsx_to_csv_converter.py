import pandas as pd
from io import BytesIO
from base_converter import BaseConverter


class XlSXtoCSVConverter(BaseConverter):
    """
    Converts an Excel file (XLSX) to CSV format.

    This class reads an Excel file from the input stream, converts it to a CSV format
    using Pandas, and writes the result to the output stream.
    """

    def convert(self, output_stream: BytesIO):
        """
        Converts the input Excel content to CSV format and writes it to the output stream.

        Parameters:
            output_stream (BytesIO): The stream to write the converted CSV content to.
        """

        self.input_stream.seek(0)

        df = pd.read_excel(self.input_stream)

        # Convert the DataFrame to XLSX and write to the output stream
        with BytesIO() as intermediate_stream:
            df.to_csv(intermediate_stream, index=False)
            intermediate_stream.seek(0)
            return output_stream.write(intermediate_stream.read())
