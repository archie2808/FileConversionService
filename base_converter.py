from io import BytesIO
from abc import ABC, abstractmethod


class BaseConverter(ABC):
    """
    Abstract base class for file conversion.

    This class provides a template for file converters, specifying that all
    converters must implement a `convert` method. It handles the storage of the
    input stream, which contains the file to be converted.

    Attributes:
        input_stream (BytesIO): A binary stream of the input file to be converted.
    """

    def __init__(self, input_stream: BytesIO):
        """
        Initializes the BaseConverter with the specified input stream.

        Parameters:
            input_stream (BytesIO): The binary stream of the file to be converted.
        """
        self.input_stream = input_stream

    @abstractmethod
    def convert(self, output_stream: BytesIO):
        """
        Converts the input file and writes the converted file to the output stream.

        This is an abstract method and must be implemented by subclasses.

        Parameters:
            output_stream (BytesIO): The binary stream to which the converted file will be written.
        """
        pass
