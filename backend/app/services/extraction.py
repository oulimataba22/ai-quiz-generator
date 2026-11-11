from pathlib import Path

import numpy as np
import pymupdf

MIN_CHARS = 20  # en dessous, on considère que la page n'a pas de vrai texte

_ocr_engine = None


def _get_ocr():
    """Charge l'OCR seulement quand on en a besoin (il est lent à démarrer)."""
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR

        _ocr_engine = RapidOCR()
    return _ocr_engine


def _ocr_page(page) -> str:
    pix = page.get_pixmap(dpi=150)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = img[:, :, :3]
    result, _ = _get_ocr()(img)
    return "\n".join(text for _box, text, _conf in (result or []))


def extract_pages(pdf_path: Path) -> list[dict]:
    pages = []
    with pymupdf.open(pdf_path) as doc:
        for number, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            method = "text"
            if len(text) < MIN_CHARS:
                text = _ocr_page(page)
                method = "ocr"
            pages.append({"page": number, "method": method, "text": text})
    return pages


def extract_text(pdf_path: Path) -> str:
    return "\n\n".join(page["text"] for page in extract_pages(pdf_path))