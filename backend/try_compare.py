import sys
from pathlib import Path

import pymupdf
from pypdf import PdfReader

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
pdf_path = UPLOAD_DIR / sys.argv[1]
page_number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
index = page_number - 1

pypdf_text = PdfReader(pdf_path).pages[index].extract_text()

with pymupdf.open(pdf_path) as doc:
    mupdf_text = doc[index].get_text()

print(f"##### PAGE {page_number} #####")
print("\n=== pypdf ===")
print(pypdf_text[:1000])
print("\n=== PyMuPDF ===")
print(mupdf_text[:1000])