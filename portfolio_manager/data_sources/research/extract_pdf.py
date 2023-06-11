import io
from pathlib import Path
from typing import List

import PyPDF2


def read_pdf(file_path: Path) -> str:
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        content = []

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            content.append(text)

        return "".join(content)


def process_files(file_paths: List[Path]) -> List[str]:
    results = []

    for file_path in file_paths:
        result = read_pdf(file_path)
        results.append(result)

    return results
