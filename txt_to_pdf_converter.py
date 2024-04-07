from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from base_converter import BaseConverter
from io import BytesIO

class TXTtoPDFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
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
