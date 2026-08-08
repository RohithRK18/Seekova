# pyright: reportMissingImports=false
# pyrefly: ignore [missing-import]

import os

from pypdf import PdfReader
from docx import Document


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    # TXT
    if extension == ".txt":
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            return file.read()

    # Markdown
    if extension == ".md":
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            return file.read()

    # PDF
    if extension == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    # DOCX
    if extension == ".docx":
        document = Document(file_path)
        text = []
        for paragraph in document.paragraphs:
            text.append(paragraph.text)
        return "\n".join(text)

    return ""
