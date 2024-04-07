
from io import BytesIO
from abc import ABC, abstractmethod

class BaseConverter(ABC):
    def __init__(self, input_stream: BytesIO):
        self.input_stream = input_stream

    @abstractmethod
    def convert(self, output_stream: BytesIO):
        pass
