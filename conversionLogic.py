from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import docx

def convert_txt_to_pdf(input_data, output_stream):
    """
    Converts plain text to a PDF file.

    This function takes plain text data and an output stream (typically a BytesIO object),
    and writes the text to the output stream as a formatted PDF file.

    Parameters:
    - input_data (str): The text to be converted into PDF format.
    - output_stream (io.BytesIO): The output stream where the PDF content will be written.

    Returns:
    None: The function writes the output directly to the provided output stream.
    """
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
    """
    Converts plain text to a DOCX document.

    This function takes plain text data, creates a new DOCX document, and adds the text
    to the document as paragraphs.

    Parameters:
    - input_data (str): The text to be converted into DOCX format.

    Returns:
    docx.Document: A DOCX document object containing the input text.
    """
    doc = docx.Document()
    for line in input_data.split('\n'):
        doc.add_paragraph(line.strip())
    return doc

def convert_docx_to_txt(input_path):
    """
    Converts a DOCX document to plain text.

    This function reads a DOCX file from the given path, extracts all text from
    the document, and returns it as a single plain text string.

    Parameters:
    - input_path (str): The file path of the DOCX document to be converted.

    Returns:
    str: A string containing the text extracted from the DOCX document.
    """
    doc = docx.Document(input_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
