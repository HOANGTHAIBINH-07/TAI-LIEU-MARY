# TAI-LIEU-MARY

This folder contains a document viewer landing page with previews for `Docs/` files.

## Setup

1. Run `generate_previews.py` to create PDF previews from the source Word/Excel files:

```bash
python generate_previews.py
```

2. Start a local HTTP server from this folder:

```bash
python -m http.server 8000
```

3. Open `http://localhost:8000/index.html` in your browser.

## Notes

- The preview generator uses LibreOffice (`soffice`) to convert `.doc`, `.docx`, `.xls`, and `.xlsx` to PDF. Install LibreOffice and add it to your PATH if needed.
- The page loads generated `previews/*.pdf` files in the modal for correct font rendering.
