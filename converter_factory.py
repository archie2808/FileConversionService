from io import BytesIO
from base_converter import BaseConverter
from converter_logic.pdf_to_docx_converter import PDFToDocxConverter
from converter_logic.docx_to_pdf_converter import DocxToPDFConverter
from converter_logic.pdf_to_txt_converter import PDFToTXTConverter
from converter_logic.docx_to_txt_converter import DOCXtoTXTConverter
from converter_logic.txt_to_pdf_converter import TXTtoPDFConverter
from converter_logic.txt_to_docx_converter import TXTToDocxConverter
from converter_logic.txt_to_rtf_converter import TXTtoRTFConverter
from converter_logic.rtf_to_docx_converter import RTFToDocxConverter
from converter_logic.rtf_to_txt_converter import RTFToTXTConverter
from converter_logic.rtf_to_pdf_converter import RTFtoPDFConverter
from converter_logic.docx_to_rtf_converter import DocxToRTFConverter
from converter_logic.pdf_to_rtf_converter import PDFToRTFConverter
from converter_logic.csv_to_xlsx_converter import CSVtoXLSXConverter
from converter_logic.xlsx_to_csv_converter import XlSXtoCSVConverter
from converter_logic.image_converter import DynamicImageConverter


class ConverterFactory:
    """
    A factory class to retrieve the appropriate converter class based on the specified source and target formats.

    The factory method `get_converter` maps pairs of source and target formats to their corresponding
    converter classes. If a conversion between the specified formats is supported, an instance of the
    converter class is returned. This class encapsulates the logic required to select the correct
    converter for a given file conversion task, abstracting away the need for the caller to
    directly instantiate converter classes.
    """

    @staticmethod
    def get_converter(input_stream: BytesIO, source_format: str, target_format: str) -> BaseConverter:
        """
        Retrieves a converter object capable of converting files from the source format to the target format.

        This method uses a predefined mapping of source and target format pairs to their corresponding converter
        classes. If the specified formats are supported, an instance of the appropriate converter class is returned.
        If the formats involve image conversion and are supported, a `DynamicImageConverter` is returned. If no
        suitable converter is found, a ValueError is raised.

        Parameters:
            input_stream (BytesIO): A binary stream of the input file to be converted.
            source_format (str): The format of the input file.
            target_format (str): The desired format of the output file.

        Returns:
            BaseConverter: An instance of a subclass of `BaseConverter` tailored to the requested conversion.

        Raises:
            ValueError: If the conversion from source_format to target_format is unsupported.
        """
        converter_map = {
            ('pdf', 'docx'): PDFToDocxConverter,
            ('docx', 'pdf'): DocxToPDFConverter,
            ('pdf', 'txt'): PDFToTXTConverter,
            ('docx', 'txt'): DOCXtoTXTConverter,
            ('txt', 'pdf'): TXTtoPDFConverter,
            ('txt', 'docx'): TXTToDocxConverter,
            ('txt', 'rtf'): TXTtoRTFConverter,
            ('rtf', 'docx'): RTFToDocxConverter,
            ('rtf', 'txt'): RTFToTXTConverter,
            ('rtf', 'pdf'): RTFtoPDFConverter,
            ('pdf', 'rtf'): PDFToRTFConverter,
            ('docx', 'rtf'): DocxToRTFConverter,
            ('xlsx', 'csv'): XlSXtoCSVConverter,
            ('csv', 'xlsx'): CSVtoXLSXConverter

        }

        image_formats = ['png', 'jpeg', 'jpg', 'gif', 'tiff', 'bmp']
        if source_format in image_formats and target_format in image_formats:
            return DynamicImageConverter(input_stream, target_format)

        # Fetch the converter class from the mapping
        converter_class = converter_map.get((source_format, target_format))
        if converter_class:
            return converter_class(input_stream)
        else:
            raise ValueError(f"Unsupported conversion from {source_format} to {target_format}")
