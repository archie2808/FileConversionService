from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import docx

def convert_txt_to_pdf(input_data, output_stream):
    c = canvas.Canvas(output_stream, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    lines = input_data.split('\n')

    for i, line in enumerate(lines):
        y = height - (i * 20) - 20  # Increase line spacing to 20 units
        text = Paragraph(line.strip(), styleN)
        text.wrapOn(c, width-20, height)
        text.drawOn(c, 10, y)

    c.save()

def convert_txt_to_docx(input_data):
    doc = docx.Document()
    for line in input_data.split('\n'):
        doc.add_paragraph(line.strip())
    return doc

def convert_docx_to_txt(input_path):
    doc = docx.Document(input_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)