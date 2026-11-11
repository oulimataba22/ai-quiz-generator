import sys
import time
from pathlib import Path

import numpy as np
import pymupdf
from rapidocr_onnxruntime import RapidOCR

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
pdf_path = UPLOAD_DIR / sys.argv[1]
page_number = int(sys.argv[2])

ocr = RapidOCR()

with pymupdf.open(pdf_path) as doc:
    page = doc[page_number - 1]
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = img[:, :, :3]

    start = time.time()
    result, _ = ocr(img)

print(f"Temps : {time.time() - start:.1f} s")
for _box, text, _conf in result or []:
    print(text)