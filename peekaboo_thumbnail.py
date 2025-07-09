#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

def convert_to_pdf(input_file, out_dir):
    result = subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf",
        str(input_file), "--outdir", str(out_dir)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Path(out_dir) / (input_file.stem + ".pdf")

def convert_pdf_to_png(pdf_file, out_path):
    result = subprocess.run([
        "pdftoppm", "-png", "-singlefile", str(pdf_file), str(out_path)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_path.with_suffix(".png")

def show_image(image_file):
    subprocess.run(["feh", "--auto-zoom", str(image_file)])

def main():
    if len(sys.argv) < 2:
        print("Usage: peekaboo_thumbnail <spreadsheet file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        pdf_file = convert_to_pdf(input_path, tmp)
        if not pdf_file.exists():
            print("Failed to convert to PDF.")
            sys.exit(1)

        png_base = tmp / "preview"
        png_file = convert_pdf_to_png(pdf_file, png_base)
        if not png_file.exists():
            print("Failed to generate PNG preview.")
            sys.exit(1)

        show_image(png_file)

if __name__ == "__main__":
    main()
