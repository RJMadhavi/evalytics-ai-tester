#!/usr/bin/env python3
"""Build synthetic multiple-choice papers (PDF) with known correct answers.

Every question here is invented for testing, so the files are safe to publish and contain
nothing copyrighted or real. Each PDF gets a matching .truth.json that says exactly what
a perfect extraction would return.

Run from the automation/ folder:
    pip install -r ai_eval/requirements.txt
    python3 ai_eval/make_golden_pdfs.py
"""
import json
import pathlib

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = pathlib.Path(__file__).parent / "corpus"

# (question, A, B, C, D, correct)
POOL = {
    1: ("A body of mass 2 kg moves with a velocity of 3 m/s. What is its kinetic energy?", "3 J", "6 J", "9 J", "12 J", "C"),
    2: ("The SI unit of force is", "Newton", "Joule", "Watt", "Pascal", "A"),
    3: ("What is the chemical formula of water?", "H2O", "CO2", "NaCl", "O2", "A"),
    4: ("Which gas is most abundant in the Earth's atmosphere?", "Oxygen", "Nitrogen", "Carbon dioxide", "Argon", "B"),
    5: ("If x + 5 = 12, what is the value of x?", "5", "6", "7", "8", "C"),
    6: ("What is the derivative of x^2 with respect to x?", "x", "2x", "x^2", "2", "B"),
    7: ("The pH of a neutral solution at 25 C is", "0", "7", "14", "1", "B"),
    8: ("Which of the following is a prime number?", "21", "27", "29", "33", "C"),
    9: ("The speed of light in vacuum is approximately", "3 x 10^8 m/s", "3 x 10^6 m/s", "3 x 10^5 m/s", "3 x 10^10 m/s", "A"),
    10: ("What is the sum of the angles of a triangle?", "90 degrees", "180 degrees", "270 degrees", "360 degrees", "B"),
    11: ("Which element has the atomic number 6?", "Nitrogen", "Oxygen", "Carbon", "Boron", "C"),
    12: ("Photosynthesis takes place mainly in the", "Roots", "Stem", "Leaves", "Flowers", "C"),
    13: ("The value of 7 x 8 is", "54", "56", "58", "64", "B"),
    14: ("Which law states that force equals mass times acceleration?", "Newton's first law", "Newton's second law", "Newton's third law", "Ohm's law", "B"),
    15: ("The formula of sulphuric acid is", "HCl", "HNO3", "H2SO4", "H3PO4", "C"),
    16: ("What is 25% of 200?", "25", "40", "50", "75", "C"),
    17: ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B"),
    18: ("The square root of 144 is", "10", "11", "12", "14", "C"),
    19: ("Which organ pumps blood through the human body?", "Lungs", "Liver", "Heart", "Kidney", "C"),
    20: ("Water boils at what temperature at sea level?", "90 C", "100 C", "110 C", "120 C", "B"),
    21: ("Which compound is formed when sodium reacts with chlorine?", "NaCl", "NaOH", "Na2O", "NaClO", "A"),
    22: ("The chemical formula of calcium hydroxide is", "CaOH", "Ca(OH)2", "CaO2", "Ca2OH", "B"),
    23: ("When hydrogen burns in oxygen, the balanced equation 2H2 + O2 gives", "H2O", "2H2O", "H2O2", "2H2O2", "B"),
    24: ("If x^2 = 49 and x > 0, then x equals", "5", "6", "7", "8", "C"),
    25: ("The molecular formula of glucose is", "C6H12O6", "C12H22O11", "C6H6", "CH4", "A"),
}

# name -> (pool numbers, layout, answer key printed in the PDF?)
PAPERS = {
    "clean_with_key": (list(range(1, 11)), "single", True),
    "clean_no_key": (list(range(11, 21)), "single", False),
    "two_column_with_key": ([3, 5, 7, 9, 11, 13, 15, 16, 18, 20], "two_column", True),
    "formulas_with_key": ([3, 15, 21, 22, 23, 24, 25, 6, 9], "single", True),
}


def wrap(text, width, canv, font, size):
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if canv.stringWidth(trial, font, size) <= width:
            line = trial
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def draw_paper(path, numbers, layout, with_key):
    page_w, page_h = A4
    c = canvas.Canvas(str(path), pagesize=A4)
    margin, top, bottom = 50, page_h - 60, 60
    cols = 2 if layout == "two_column" else 1
    col_w = (page_w - 2 * margin - (30 if cols == 2 else 0)) / cols
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, page_h - 35, "Sample practice paper (synthetic test data)")
    col, y = 0, top - 10
    per_column = (len(numbers) + 1) // 2 if cols == 2 else len(numbers)  # even columns, like a real paper
    for n_shown, num in enumerate(numbers, start=1):
        q, a, b, cc, d, _ = POOL[num]
        block = [("q", line) for line in wrap(f"{n_shown}. {q}", col_w, c, "Helvetica-Bold", 10)]
        for letter, text in zip("ABCD", (a, b, cc, d)):
            block += [("o", line) for line in wrap(f"({letter}) {text}", col_w - 15, c, "Helvetica", 10)]
        height = len(block) * 13 + 14
        if cols == 2 and col == 0 and n_shown == per_column + 1:
            col, y = 1, top - 10
        elif y - height < bottom:
            c.showPage()
            col, y = (0, top) if cols == 1 else (0, top - 10)
        x = margin + col * (col_w + 30)
        for kind, line in block:
            c.setFont("Helvetica-Bold" if kind == "q" else "Helvetica", 10)
            c.drawString(x + (0 if kind == "q" else 15), y, line)
            y -= 13
        y -= 14
    if with_key:
        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, page_h - 60, "Answer Key")
        c.setFont("Helvetica", 11)
        yy = page_h - 90
        for n_shown, num in enumerate(numbers, start=1):
            c.drawString(margin, yy, f"{n_shown} - {POOL[num][5]}")
            yy -= 16
    c.save()


def truth_for(numbers, layout, with_key, file_name):
    return {
        "file": file_name,
        "layout": layout,
        "answer_key_in_file": with_key,
        "questions": [
            {
                "id": f"q{n_shown:02d}",
                "question_text": POOL[num][0],
                "option_a": POOL[num][1],
                "option_b": POOL[num][2],
                "option_c": POOL[num][3],
                "option_d": POOL[num][4],
                "correct_option": POOL[num][5],
                "difficulty": "easy",
            }
            for n_shown, num in enumerate(numbers, start=1)
        ],
    }


def main():
    OUT.mkdir(exist_ok=True)
    for name, (numbers, layout, with_key) in PAPERS.items():
        pdf = OUT / f"{name}.pdf"
        draw_paper(pdf, numbers, layout, with_key)
        (OUT / f"{name}.truth.json").write_text(json.dumps(truth_for(numbers, layout, with_key, pdf.name), indent=2))
        print(f"wrote {pdf.name} ({len(numbers)} questions, key in file: {with_key})")


if __name__ == "__main__":
    main()
