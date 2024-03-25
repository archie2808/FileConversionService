import io
import os
import fitz #PyMuPDF
from app import app
import pytest
import docx

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


import fitz  # PyMuPDF


def read_pdf(file_content):
    """
    Reads and extracts text from PDF file content.

    Parameters:
    file_content (bytes): The binary content of a PDF file.

    Returns:
    str: The text extracted from the PDF document.
    """
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def test_txt_to_pdf_content_verification(client):
    """
    Test verifying the content of the converted PDF file.
    """
    data = {'file': (io.BytesIO(b"Hello, PDF world!"), 'test.txt')}
    response = client.post('/txt_to_pdf', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    pdf_text = read_pdf(response.data)
    assert "Hello, PDF world!" in pdf_text


def read_docx(file_content):
    """
    Reads and extracts text from a DOCX file content.

    Parameters:
    file_content (bytes): The binary content of a DOCX file.

    Returns:
    str: The text extracted from the DOCX document.
    """
    doc = docx.Document(io.BytesIO(file_content))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)
def test_index_route(client):
    """Test the index route can be accessed and loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"File Conversion Service" in response.data

def test_txt_to_pdf_conversion(client):
    """Test text to PDF conversion route with valid input."""
    # Assuming the route expects a file part in the form
    data = {'file': (io.BytesIO(b"Hello, world!"), 'test.txt')}
    response = client.post('/txt_to_pdf', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'application/pdf' in response.content_type

def test_validation_route(client):
    """Test file validation route with no file attached."""
    response = client.post('/validate_file')
    assert response.status_code == 400
    assert b"No file part" in response.data


def test_txt_to_docx_conversion(client):
    """
    Test the TXT to DOCX conversion route operates as expected.
    """
    # Prepare a text file for uploading
    data = {'file': (io.BytesIO(b"Hello, world! This is a test."), 'test.txt')}
    response = client.post('/txt_to_docx', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in response.content_type

def test_txt_to_docx_content_verification(client):
    """
    Test verifying the content of the converted DOCX file.
    """
    data = {'file': (io.BytesIO(b"Hello, world! This is a test."), 'test.txt')}
    response = client.post('/txt_to_docx', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    docx_text = read_docx(response.data)
    assert "Hello, world! This is a test." in docx_text

