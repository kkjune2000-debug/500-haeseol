from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import fitz
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
SOURCE = Path(r"C:\Users\김광준\OneDrive\SCAN\기독교\성경\갈라디아서\갈라디아서 강해")
OUTPUT = Path(__file__).resolve().parent
TARGETS = [
    "성경 갈라디아서 갈라디아서 강해 이중수.pdf",
    "성경 갈라디아서 갈라디아서 최갑종.pdf",
    "성경 갈라디아서 당신을 위한 갈라디아서 팀켈러.pdf",
    "성경 갈라디아서 존스토트.pdf",
]


def ocr_pdf(name: str) -> tuple[str, int]:
    pdf = SOURCE / name
    doc = fitz.open(pdf)
    sections = []
    for index in range(min(45, len(doc))):
        page = doc[index]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.45, 1.45), colorspace=fitz.csGRAY, alpha=False)
        image = Image.frombytes("L", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(
            image,
            lang="script/Hangul+eng",
            config="--psm 6",
        )
        sections.append(f"\n===== PDF PAGE {index + 1} =====\n{text}")
    output = OUTPUT / f"{pdf.stem}.front45.txt"
    output.write_text("".join(sections), encoding="utf-8")
    return output.name, len(sections)


with ThreadPoolExecutor(max_workers=4) as pool:
    jobs = [pool.submit(ocr_pdf, name) for name in TARGETS]
    for job in as_completed(jobs):
        print(job.result(), flush=True)
