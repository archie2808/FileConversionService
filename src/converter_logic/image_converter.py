from PIL import Image
from io import BytesIO
from src.base_converter import BaseConverter
from src.logger_config import configure_logger

logger = configure_logger(__name__)


class DynamicImageConverter(BaseConverter):
    """
    A converter class for image files that supports converting between different image formats.

    This class handles image format conversions, including handling transparency
    for formats that do not support it by adding a white background where necessary.
    """

    def __init__(self, input_stream: BytesIO, target_format: str):
        """
        Initializes the DynamicImageConverter with the input stream and target format.

        Parameters:
            input_stream (BytesIO): The stream containing the image to be converted.
            target_format (str): The target image format.
        """
        super().__init__(input_stream)
        self.target_format = target_format.lower()

    def convert(self, output_stream: BytesIO):
        """
        Converts the image from the source format to the target format and writes the result to the output stream.

        Parameters:
            output_stream (BytesIO): The stream to write the converted image to.

        Returns:
            The output stream with the converted image data.
        """

        image = Image.open(self.input_stream)
        logger.info(f"image mode: {image}")

        # Handle transparency for formats that don't support it
        if self.target_format == 'jpeg' and (image.mode in ('RGBA', 'LA') or ('transparency' in image.info)):
            logger.debug(f"target format {self.target_format} and image mode {image.mode}")

            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        else:
            image = image.convert("RGB")

        logger.debug(f"image mode1: {image}")
        save_format = self.target_format.upper()
        if save_format == 'JPG':
            save_format = 'JPEG'

        image.save(output_stream, format=save_format)

        logger.info(f"Image converted to {self.target_format.upper()} format")
        output_stream.seek(0)
        return output_stream
