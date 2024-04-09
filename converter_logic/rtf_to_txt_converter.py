from io import BytesIO
from base_converter import BaseConverter


class RTFToTXTConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        raise NotImplemented