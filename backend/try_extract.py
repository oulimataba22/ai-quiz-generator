import sys
import time
from pathlib import Path

from app.services.extraction import extract_pages

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"

pdf_path = UPLOAD_DIR / sys.argv[1]

start = time.time()
pages = extract_pages(pdf_path)
elapsed = time.time() - start

print(f"Nombre de pages : {len(pages)}  (temps : {elapsed:.1f} s)")
for p in pages:
    print(f"  page {p['page']} : {len(p['text'])} caractères ({p['method']})")

print("\n----- DÉBUT DU TEXTE -----")
print("\n\n".join(p["text"] for p in pages)[:800])