# md-converter

Convert PDF, DOCX, XLSX, XLS, and PPTX files to Markdown — with a web UI for non-technical users and a CLI for scripting.

## Supported formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Text and tables per page |
| Word | `.docx` | Headings, bold/italic, tables, equations (LaTeX) |
| Excel | `.xlsx` `.xls` | Each sheet as a markdown table; merged cells filled |
| PowerPoint | `.pptx` | Slide titles as H1, body text, tables, images, charts |

> DOC and PPT (legacy formats) are not supported. Convert them to DOCX/PPTX first using Word or LibreOffice.

---

## Prerequisites

- Python 3.10 or later
- No system-level dependencies — everything is installed via `pip`

---

## Setup

```bash
# Create virtual environment
python -m venv .venv

# Install dependencies (Windows)
.venv\Scripts\pip install -r requirements.txt

# Install dependencies (macOS / Linux)
.venv/bin/pip install -r requirements.txt
```

---

## Usage

### Web UI (Streamlit)

```bash
# Windows
.venv\Scripts\streamlit run ui/streamlit_app.py

# macOS / Linux
.venv/bin/streamlit run ui/streamlit_app.py
```

Open `http://localhost:8501` in your browser, upload a file, and download the result.

### CLI

```bash
# Print markdown to stdout
.venv\Scripts\python ui/cli.py report.pdf

# Save to a file
.venv\Scripts\python ui/cli.py report.pdf -o report.md

# Works with all supported formats
.venv\Scripts\python ui/cli.py data.xlsx -o data.md
.venv\Scripts\python ui/cli.py slides.pptx -o slides.md
```

---

## Running tests

```bash
# Generate test files first (only needed once)
.venv\Scripts\python tests/create_test_files.py

# Run the full test suite
.venv\Scripts\pytest tests/ -v
```

---

## Adding a new format

1. Create `converters/<format>.py` implementing `BaseConverter.accepts()` and `BaseConverter.convert()`
2. Register it in `facade.py`: add to `SUPPORTED_EXTENSIONS` and `self._converters`
3. Add a `FileTestVector` in `tests/_test_vectors.py` and a generator in `tests/create_test_files.py`

Nothing else needs to change.

---

## Contributing

Contributions are welcome! Feel free to open an issue to report a bug or suggest a feature, or submit a pull request directly.
