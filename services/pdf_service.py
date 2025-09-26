import os
import markdown2
from fpdf import FPDF
from bs4 import BeautifulSoup

def save_markdown_as_pdf(markdown_text, filename, title="Document"):
    """
    Converts markdown text to PDF using Unicode font (DejaVuSans).
    """
    # Convert markdown → HTML → plain text
    html = markdown2.markdown(markdown_text)
    text = BeautifulSoup(html, "html.parser").get_text()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Load Unicode font
    font_path = os.path.join(os.path.dirname(__file__), "..", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)

    # Title
    pdf.set_font("DejaVu", '', 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(5)

    # Content
    pdf.set_font("DejaVu", '', 12)
    pdf.multi_cell(0, 8, text)

    pdf.output(filename)
    print(f"✅ Saved PDF: {filename}")
