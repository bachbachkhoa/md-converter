# CLAUDE.md

> Operating context and rules for any AI assistant working in this repo.
> **Read this file fully before touching code.** If something here conflicts
> with what you see in the code, this file wins — but flag the conflict
> instead of silently following one side.
>
> Every rule below exists to prevent a mistake that has actually happened or
> could trivially happen in this codebase. If a rule no longer maps to a real
> risk, delete it.

---

## 1. What this repo is

**md-converter** — a document-to-Markdown conversion tool with a Facade
pattern so that multiple UI layers (web, CLI, future desktop) share the same
conversion logic without duplication.

| Path                    | Purpose                                        |
|-------------------------|------------------------------------------------|
| `converters/base.py`    | Abstract `BaseConverter` — the contract        |
| `converters/*.py`       | One converter per format                       |
| `facade.py`             | `ConverterFacade` — the **only** public API    |
| `ui/streamlit_app.py`   | Streamlit web interface                        |
| `ui/cli.py`             | Command-line interface                         |
| `tests/`                | pytest suite + test file generator             |

Supported formats: **PDF, DOCX, XLSX, XLS, PPTX**.
DOC and PPT are intentionally not supported (legacy formats, no good
pure-Python parser; users are expected to convert to DOCX/PPTX first).

---

## 2. Stack (do not change without asking)

- Python 3.10+
- `pdfplumber` — PDF parsing (text + tables)
- `python-docx` — DOCX (headings, bold/italic, tables)
- `python-pptx` — PPTX (slides, titles, tables, charts)
- `openpyxl` — XLSX (read-write mode required for merged-cell handling)
- `xlrd` — XLS (read-only; no write support without additional library)
- `streamlit` — web UI
- `pytest` + `fpdf2` — test suite and test file generation

All packages are pinned inside `.venv`. Never install globally.

---

## 3. Commands

```bash
# Setup (first time)
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# Run web UI
.venv\Scripts\streamlit run ui/streamlit_app.py

# Run CLI
.venv\Scripts\python ui/cli.py input.pdf
.venv\Scripts\python ui/cli.py input.xlsx -o output.md

# Tests — always use the venv's pytest
.venv\Scripts\pytest tests/ -v

# Generate test files (run once before first test run)
.venv\Scripts\python tests/create_test_files.py
```

---

## 4. Where things live

```
converters/
  base.py      # BaseConverter ABC — accepts() + convert()
  pdf.py       # pdfplumber: text per page + tables
  docx.py      # python-docx: headings, inline formatting, tables
  xlsx.py      # openpyxl: merged-cell fill, then rows → markdown table
  xls.py       # xlrd: rows → markdown table (merged cells: first cell only)
  pptx.py      # python-pptx: slide title, text frames, tables, charts
facade.py      # ConverterFacade: convert(path) + convert_stream(stream, filename)
ui/
  streamlit_app.py  # file uploader → ConverterFacade → preview + download
  cli.py            # argparse → ConverterFacade → stdout or file
tests/
  _test_vectors.py      # FileTestVector: must_include / must_not_include
  test_converters.py    # parametrised pytest tests
  create_test_files.py  # generates test_files/ programmatically
  test_files/           # generated binary test files (commit these)
```

---

## 5. Architecture rules

- **UI code must only import `ConverterFacade`.** Never import a converter
  class directly from `ui/`. The whole point of the Facade is that UI code
  is format-agnostic. A UI file that imports `PdfConverter` directly is a bug.

- **One converter, one format.** Each file in `converters/` handles exactly
  one file extension. If a format needs sub-cases, handle them inside that
  file — don't split across two converters.

- **Adding a new format requires three changes** — and only three:
  1. New file in `converters/`
  2. Import + register in `facade.py` (`SUPPORTED_EXTENSIONS` + `_converters` list)
  3. Test vector in `tests/_test_vectors.py` + entry in `create_test_files.py`
  Nothing else should need to change.

- **`accepts()` and `convert()` must not change the stream position.** If a
  converter reads from the stream, it must `seek()` back to the original
  position before returning. The Facade resets position between converter
  attempts, but relying on that instead of doing it yourself is fragile.

- **`facade.py`'s public interface is stable.** `convert(path)` and
  `convert_stream(stream, filename)` are the contract UI code depends on.
  Changing their signature breaks every UI layer at once — propose first.

---

## 6. Coding rules

- **Simplest thing that works.** No new abstraction until the same pattern
  appears at least 3 times.
- **No new dependencies without asking.** Check if the existing libraries
  already cover the need.
- **Don't touch code outside the scope of the task.** Refactoring nearby
  "ugly" code while fixing a bug muddies the diff. Do it in a separate task.
- Comments explain **why**, not **what**. A comment that just restates the
  code should be deleted.
- **No silent swallowing of exceptions.** If a converter fails, let the
  exception propagate so `ConverterFacade` can record it properly. An empty
  `except: pass` hides real bugs.

---

## 7. Blast-radius zones 🟢 🟡 🔴

- 🟢 **Green — edit freely:** `ui/`, `tests/_test_vectors.py`,
  `tests/create_test_files.py`. Self-contained; a mistake here is local.

- 🟡 **Yellow — edit carefully, run tests afterward:** individual
  `converters/*.py` files. A change to `xlsx.py` could silently break merged-
  cell handling or corrupt table output. Run the full test suite.

- 🔴 **Red — propose before editing:** `converters/base.py` and the public
  interface of `facade.py`. Changing `BaseConverter` forces every converter
  to update. Changing `ConverterFacade`'s method signatures breaks every UI.
  Stop and present the plan before writing.

---

## 8. Multi-step work

For any non-trivial task spanning multiple files or steps:

- After each significant step, state plainly: **what's done, what's
  verified, what's left.**
- If a test goes red, stop. Do not stack the next step on a broken state.
- If you're re-trying fixes already rejected, stop and restart fresh.

---

## 9. Git & commits

- Branches: `feat/…`, `fix/…`, `chore/…`
- Commit messages: imperative present tense — `add pptx title detection`,
  not `added` or `adds`. One logical change per commit.
- Never commit: `.env`, secrets, `__pycache__/`, `.pytest_cache/`, or the
  `.venv/` directory.
- Tests must pass before a commit is considered done:
  `.venv\Scripts\pytest tests/ -v`

---

## 10. Definition of Done

A change is done only when **all** of these are true:

- [ ] It does what the task asked — nothing more, nothing less.
- [ ] `pytest tests/ -v` is fully green.
- [ ] New behavior has a test vector in `_test_vectors.py` with strings that
      **would actually fail if the conversion were wrong** — not a string so
      generic it could appear anywhere.
- [ ] If a bug was fixed, a test exists that fails on the old code.
- [ ] No unrelated files were touched.
- [ ] You can explain every line you wrote.

---

## 11. When to stop and ask

Pause and ask, **not guess**, when:

- The task is ambiguous or could reasonably mean two different things.
- It requires a 🔴-zone change.
- Adding a new format that doesn't fit the current `accepts(extension)` model.
- A new dependency is needed.
- You would change `facade.py`'s public interface.
- You are about to delete or rewrite more than ~20 lines you didn't write.

---

## 12. Anti-patterns already hit in this codebase

- **`openpyxl` `read_only=True` + merged cells** — read-only mode doesn't
  expose `merged_cells.ranges`, so merged cells appear as `None` in all
  positions except the top-left. Always open with `read_only=False` when
  you need to handle merges.

- **python-pptx shape identity** — `slide.shapes.title` creates a new Python
  wrapper object every call, so `shape is title_shape` always returns `False`.
  Compare by XML element: `shape._element is title_el`.

- **UI importing converters directly** — this was caught before it shipped,
  but defeats the Facade entirely. All UI code goes through `ConverterFacade`.

---

## 13. Hard NOs

- ❌ Don't install packages outside `.venv`.
- ❌ Don't add support for DOC or PPT — direct users to convert to DOCX/PPTX.
- ❌ Don't add `llm_client` or any network call to converters without an
  explicit task and discussion first.
- ❌ Don't bypass `SUPPORTED_EXTENSIONS` in `facade.py` — it's the single
  source of truth for what the tool accepts.
- ❌ Don't commit generated test files to `.gitignore` — they must be
  reproducible via `create_test_files.py` and committed so CI can run offline.

---

_Keep this file current. If a rule here is wrong or outdated, fixing
CLAUDE.md is itself a valid and welcome change._
