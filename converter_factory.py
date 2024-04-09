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
    @staticmethod
    def get_converter(input_stream: BytesIO, source_format: str, target_format: str) -> BaseConverter:
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

        # Attempt to fetch the converter class based on the provided source and target formats
        converter_class = converter_map.get((source_format, target_format))
        if converter_class:
            return converter_class(input_stream)
        else:
            raise ValueError(f"Unsupported conversion from {source_format} to {target_format}")

