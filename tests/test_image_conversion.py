import unittest
from io import BytesIO
from PIL import Image
from src.converter_logic.image_converter import DynamicImageConverter

class TestDynamicImageConverter(unittest.TestCase):
    def setUp(self):
        """Set up the test environment for each test."""
        self.size = (100, 100)
        self.color = 'red'

    def create_test_image(self, mode, format):
        """Helper method to create an image and return a BytesIO object."""
        input_image = Image.new(mode, self.size, color=self.color)
        input_stream = BytesIO()
        input_image.save(input_stream, format=format)
        input_stream.seek(0)
        return input_stream

    def perform_conversion_test(self, source_format, target_format, expected_mode):
        """Method to perform conversion test and verify attributes."""
        input_stream = self.create_test_image('RGB', source_format)
        output_stream = BytesIO()

        converter = DynamicImageConverter(input_stream, target_format)
        converter.convert(output_stream)

        output_stream.seek(0)
        output_image = Image.open(output_stream)

        self.assertEqual(output_image.format, target_format.upper())
        self.assertEqual(output_image.mode, expected_mode)
        self.assertEqual(output_image.size, self.size)

        if source_format == target_format:
            original = Image.open(input_stream)
            self.assertEqual(list(original.getdata()), list(output_image.getdata()))

    def test_convert_jpeg_to_png(self):
        """Test converting a JPEG to PNG and verify that conversion preserves image size and mode."""
        self.perform_conversion_test('JPEG', 'PNG', 'RGB')

    def test_convert_png_to_png(self):
        """Test converting a PNG to another PNG, ensuring the image remains unchanged."""
        self.perform_conversion_test('PNG', 'PNG', 'RGB')

    def test_convert_png_to_jpeg(self):
        """Test converting a PNG to JPEG."""
        self.perform_conversion_test('PNG', 'JPEG', 'RGB')

    def test_convert_png_to_jpeg(self):
        """Test converting a PNG to JPEG."""
        self.perform_conversion_test('PNG', 'JPEG', 'RGB')

    def test_convert_gif_to_png(self):
        """Test converting a GIF to PNG."""
        self.perform_conversion_test('GIF', 'PNG', 'RGB')

    def test_convert_bmp_to_png(self):
        """Test converting a BMP to PNG."""
        self.perform_conversion_test('BMP', 'PNG', 'RGB')

    def test_convert_tiff_to_jpeg(self):
        """Test converting a TIFF to JPEG."""
        self.perform_conversion_test('TIFF', 'JPEG', 'RGB')

    def test_convert_png_to_gif(self):
        """Test converting a PNG to GIF."""
        self.perform_conversion_test('PNG', 'GIF', 'P')

    def test_convert_png_to_bmp(self):
        """Test converting a PNG to BMP."""
        self.perform_conversion_test('PNG', 'BMP', 'RGB')

    def test_convert_png_to_tiff(self):
        """Test converting a PNG to TIFF."""
        self.perform_conversion_test('PNG', 'TIFF', 'RGB')

if __name__ == '__main__':
    unittest.main()
