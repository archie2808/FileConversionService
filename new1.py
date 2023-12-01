from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def convert_txt_to_pdf(txt_filename, pdf_buffer):
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setFont("Helvetica", 10)
    y_position = 750

    with open(txt_filename, 'r') as txt_file:
        for line in txt_file:
            pdf.drawString(72, y_position, line.strip())
            y_position -= 12
            if y_position < 72:
                y_position = 750
                pdf.showPage()

    pdf.save()