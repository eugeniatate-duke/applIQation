import pdfplumber
from docx import Document


def extract_resume_text(upload_file):
    """
    Extract text from PDF, DOCX, or TXT resumes.
    """

    filename = upload_file.filename.lower()

    if filename.endswith(".pdf"):

        upload_file.file.seek(0)

        text = ""

        with pdfplumber.open(upload_file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    if filename.endswith(".docx"):

        document = Document(upload_file.file)

        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    if filename.endswith(".txt"):

        return upload_file.file.read().decode("utf-8")

    raise ValueError("Unsupported file format")
