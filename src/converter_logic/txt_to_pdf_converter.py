from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from ..base_converter import BaseConverter


class TXTtoPDFConverter(BaseConverter):
    """
    Converts plain text to PDF format.

    Utilizes ReportLab to generate a PDF document from plain text content. Inherits from
    BaseConverter and implements the document creation process.
    """

    def convert(self, output_stream: BytesIO):
        """
        Transforms the input plain text into a PDF document and writes it to the output stream.

        Parameters:
            output_stream (BytesIO): The stream where the PDF content will be written.
        """
        c = canvas.Canvas(output_stream, pagesize=letter)
        width, height = letter
        styles = getSampleStyleSheet()
        styleN = styles['Normal']

        input_text = self.input_stream.getvalue().decode('utf-8')
        lines = input_text.split('\n')

        for i, line in enumerate(lines):
            y = height - (i * 20) - 20
            text = Paragraph(line.strip(), styleN)
            text.wrapOn(c, width - 20, height)
            text.drawOn(c, 10, y)

        c.save()
