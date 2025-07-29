import os, csv, fitz

os.makedirs("data", exist_ok=True)
out_csv = "data/annotations_template.csv"
pdf_folder = "data/sample_pdfs"

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([
        "pdf_file","page","text","font_size","x0","y0","flags","label"
    ])
    for fname in sorted(os.listdir(pdf_folder)):
        if not fname.lower().endswith(".pdf"):
            continue
        path = os.path.join(pdf_folder, fname)
        doc = fitz.open(path)
        for page in doc:
            pno = page.number + 1
            for block in page.get_text("dict")["blocks"]:
                # each block is a group of lines; we iterate block["lines"]
                for line in block.get("lines", []):
                    spans = line["spans"]
                    if not spans: continue
                    # join all spans’ text into one line
                    text = " ".join(s["text"].strip() for s in spans).strip()
                    if not text: continue
                    # use the first span’s font_size, flags, and bbox as representative
                    rep = spans[0]
                    bbox = rep.get("bbox", [0,0,0,0])
                    w.writerow([
                        fname,
                        pno,
                        text,
                        round(rep["size"], 1),
                        round(bbox[0], 1),
                        round(bbox[1], 1),
                        rep["flags"],
                        ""  # label to fill in
                    ])
print("→ Wrote line‑level template to", out_csv)
