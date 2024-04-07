from io import BytesIO
from base_converter import BaseConverter
from pdf_to_docx_converter import PDFToDocxConverter
from docx_to_pdf_converter import DocxToPDFConverter
from pdf_to_txt_converter import PDFToTXTConverter
from docx_to_txt_converter import DOCXtoTXTConverter
from txt_to_pdf_converter import TXTtoPDFConverter
from txt_to_docx_converter import TXTToDocxConverter
from txt_to_rtf_converter import TXTtoRTFConverter
from rtf_to_docx_converter import RTFToDocxConverter
from rtf_to_txt_converter import RTFToTXTConverter
from rtf_to_pdf_converter import RTFtoPDFConverter
from docx_to_rtf_converter import DocxToRTFConverter
from pdf_to_rtf_converter import PDFToRTFConverter



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
            ('docx', 'rtf'): DocxToRTFConverter

        }

        # Attempt to fetch the converter class based on the provided source and target formats
        converter_class = converter_map.get((source_format, target_format))
        if converter_class:
            return converter_class(input_stream)
        else:
            raise ValueError(f"Unsupported conversion from {source_format} to {target_format}")

