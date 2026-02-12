import pdfplumber
import docx

def extract_text(file):
    text = ""

    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "

    else:
        text = file.read().decode('utf-8')

    return text
