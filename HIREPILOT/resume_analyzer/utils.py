import docx2txt
import PyPDF2

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return ""
