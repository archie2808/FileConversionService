import pandas as pd
from io import BytesIO
from base_converter import BaseConverter


class CSVtoXLSXConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):

        self.input_stream.seek(0)

        df = pd.read_csv(self.input_stream)

        # Convert the DataFrame to XLSX and write to the output stream
        with BytesIO() as intermediate_stream:
            df.to_excel(intermediate_stream, index=False)
            intermediate_stream.seek(0)
            return output_stream.write(intermediate_stream.read())
