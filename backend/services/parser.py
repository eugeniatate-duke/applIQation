import pdfplumber
from io import BytesIO
from docx import Document


def extract_resume_text(upload_file):
    filename = upload_file.filename.lower()
    upload_file.file.seek(0)
    file_bytes = upload_file.file.read()

    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif filename.endswith(".docx"):
        document = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in document.paragraphs)

    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8")

    raise ValueError("Unsupported file format")
