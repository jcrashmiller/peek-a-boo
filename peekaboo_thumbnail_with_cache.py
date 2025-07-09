#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import shutil
import time
import os
import hashlib
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "peekaboo"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_EXPIRY = 60 * 60  # 60 minutes

def get_cache_filename(file_path):
    hasher = hashlib.md5()
    hasher.update(str(file_path.resolve()).encode('utf-8'))
    return CACHE_DIR / (hasher.hexdigest() + ".png")

def is_cache_valid(cached_file):
    if not cached_file.exists():
        return False
    age = time.time() - cached_file.stat().st_mtime
    return age < CACHE_EXPIRY

def convert_to_pdf(input_file, out_dir):
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf",
        str(input_file), "--outdir", str(out_dir)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Path(out_dir) / (input_file.stem + ".pdf")

def convert_pdf_to_png(pdf_file, out_path):
    subprocess.run([
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

    cached_preview = get_cache_filename(input_path)

    if is_cache_valid(cached_preview):
        show_image(cached_preview)
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        pdf_file = convert_to_pdf(input_path, tmp)
        if not pdf_file.exists():
            print("Failed to convert to PDF.")
            sys.exit(1)

        temp_png_base = tmp / "preview"
        temp_png_file = convert_pdf_to_png(pdf_file, temp_png_base)
        if not temp_png_file.exists():
            print("Failed to generate PNG preview.")
            sys.exit(1)

        # Save to cache
        shutil.copy(temp_png_file, cached_preview)
        show_image(cached_preview)

if __name__ == "__main__":
    main()
