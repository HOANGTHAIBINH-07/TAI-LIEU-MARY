#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "Docs"
PREVIEWS_DIR = ROOT / "previews"
PREVIEWS_DIR.mkdir(exist_ok=True)

SUPPORTED = {".doc", ".docx", ".xls", ".xlsx"}

WINDOWS_CANDIDATES = [
    Path("C:/Program Files/LibreOffice/program/soffice.exe"),
    Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
]


def find_soffice():
    for name in ["soffice", "soffice.exe"]:
        path = which(name)
        if path:
            return Path(path)
    for candidate in WINDOWS_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def convert_file(soffice_path: Path, source_path: Path):
    target_name = source_path.with_suffix('.pdf').name
    target_path = PREVIEWS_DIR / target_name
    print(f"Converting {source_path.name} -> {target_path.name}")
    cmd = [str(soffice_path), "--headless", "--convert-to", "pdf", "--outdir", str(PREVIEWS_DIR), str(source_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error converting {source_path.name}: {result.stderr.strip()}")
        return False
    if not target_path.exists():
        print(f"Warning: output not found for {source_path.name}")
        return False
    return True


def main():
    if not DOCS_DIR.exists():
        print(f"Docs folder not found: {DOCS_DIR}")
        sys.exit(1)

    soffice = find_soffice()
    if not soffice:
        print("LibreOffice/soffice not found. Install LibreOffice and add it to PATH.")
        sys.exit(1)

    print(f"Using LibreOffice at: {soffice}")
    files = sorted([p for p in DOCS_DIR.iterdir() if p.suffix.lower() in SUPPORTED])
    if not files:
        print("No supported docs found in Docs/.")
        sys.exit(0)

    success = 0
    for file_path in files:
        if convert_file(soffice, file_path):
            success += 1

    print(f"Converted {success}/{len(files)} files into {PREVIEWS_DIR}")
    print("Open index.html through a local HTTP server and the modal will display preview PDFs.")


if __name__ == '__main__':
    main()
