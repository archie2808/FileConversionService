from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import docx
import fitz
import io
import logging
import subprocess
import tempfile
import os
from pdf2docx import Converter


def txt_to_pdf(input_data, output_stream):
    """
    Converts plain text to a PDF file.

    This function takes plain text data and an output stream (a BytesIO object),
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
        text.wrapOn(c, width - 20, height)
        text.drawOn(c, 10, y)

    c.save()


def txt_to_docx(input_data):
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


def docx_to_txt(input_stream):
    """
    Converts a DOCX document to plain text.

    This function reads a DOCX file from the given BytesIO object, extracts all text from
    the document, and returns it as a single plain text string.

    Parameters:
    - input_stream (io.BytesIO): A BytesIO object containing the DOCX document to be converted.

    Returns:
    str: A string containing the text extracted from the DOCX document.
    """
    # Ensure the stream is at the start
    input_stream.seek(0)

    # Load the DOCX file from the BytesIO object
    doc = docx.Document(input_stream)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def pdf_to_txt(input_stream):
    """
    Extracts all text from a PDF file.

    Parameters:
    - input_stream (io.BytesIO): The stream of the PDF document to be converted.

    Returns:
    str: A string containing all text extracted from the PDF document.
    """

    text = ''
    with fitz.open(stream=input_stream) as doc:
        for page in doc:
            text += page.get_text()

    return text


def docx_to_pdf(input_stream, output_stream):
    """
       Converts a DOCX document to a PDF file.

       This function utilizes LibreOffice's command-line interface to convert
       a DOCX document from the given BytesIO object to PDF format, writing the result
       to another BytesIO object specified as the output stream.

       Parameters:
       - input_stream (io.BytesIO): A BytesIO object containing the DOCX document to be converted.
       - output_stream (io.BytesIO): The output stream where the PDF content will be written.

       Requires:
       - LibreOffice to be installed on the system where this code is run.

       Raises:
       - FileNotFoundError: If LibreOffice does not create the expected PDF file.

       Note:
       This function creates temporary files to facilitate the conversion process since
       LibreOffice operates on file paths. These temporary files are cleaned up before the
       function returns.
       """
    # Path to the LibreOffice executable
    libreoffice_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Define paths for the input DOCX and the expected output PDF
        docx_path = os.path.join(tmpdirname, "input.docx")

        # Adjust the expected PDF filename to match the input filename but with .pdf extension
        pdf_path = os.path.join(tmpdirname, "input.pdf")

        # Write the DOCX content to a temporary file
        with open(docx_path, 'wb') as tmp_docx:
            tmp_docx.write(input_stream.read())

        # Convert DOCX to PDF using LibreOffice
        process = subprocess.run([
            libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir',
            tmpdirname, docx_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # For debugging: print or log the standard output and error
        print("STDOUT:", process.stdout.decode())
        print("STDERR:", process.stderr.decode())

        # Ensure the PDF file exists before attempting to read it
        if os.path.exists(pdf_path):
            # Read the converted PDF and write it to the provided output_stream
            with open(pdf_path, 'rb') as pdf_file:
                output_stream.write(pdf_file.read())
        else:
            print(f"Expected PDF file was not created: {pdf_path}")
            # Optionally, handle the error appropriately
            raise FileNotFoundError(f"Expected PDF file was not created: {pdf_path}")


def pdf_to_docx(input_stream, output_stream):
    """
    Converts a PDF file to DOCX format using the pdf2docx library.

    Parameters:
    - input_stream (io.BytesIO): A BytesIO object containing the PDF document to be converted.
    - output_stream (io.BytesIO): The output stream where the DOCX content will be written.
    """

    # Create a temporary file for the input PDF as pdf2docx works with file paths
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
        temp_pdf_file.write(input_stream.read())
        input_pdf_path = temp_pdf_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_docx_file:
        output_docx_path = temp_docx_file.name

    cv = Converter(input_pdf_path)
    cv.convert(output_docx_path)
    cv.close()

    os.unlink(input_pdf_path)

    with open(output_docx_path, 'rb') as docx_file:
        output_stream.write(docx_file.read())

    os.unlink(output_docx_path)
