import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import io
import zipfile
import streamlit as st
from facade import ConverterFacade

facade = ConverterFacade()

MAX_FILES = 30
MAX_TOTAL_MB = 100
SUPPORTED = facade.supported_extensions()          # {'.pdf', '.docx', ...}
SUPPORTED_DISPLAY = ", ".join(sorted(SUPPORTED))   # for UI labels

st.set_page_config(page_title="MD Converter", page_icon="📄", layout="wide")
st.title("📄 Document → Markdown Converter")
st.caption(
    f"Supported formats: {SUPPORTED_DISPLAY.upper()}  ·  "
    f"Max {MAX_FILES} files  ·  Max {MAX_TOTAL_MB} MB total"
)

uploaded_files = st.file_uploader(
    "Upload files",
    accept_multiple_files=True,
    label_visibility="collapsed",
)

if not uploaded_files:
    st.stop()

# ------------------------------------------------------------------
# 1. Enforce limits
# ------------------------------------------------------------------
total_mb = sum(f.size for f in uploaded_files) / (1024 * 1024)

if len(uploaded_files) > MAX_FILES:
    st.error(
        f"Too many files: {len(uploaded_files)} uploaded, limit is {MAX_FILES}. "
        "Please remove some files and try again."
    )
    st.stop()

if total_mb > MAX_TOTAL_MB:
    st.error(
        f"Total size {total_mb:.1f} MB exceeds the {MAX_TOTAL_MB} MB limit. "
        "Please remove some files and try again."
    )
    st.stop()

# ------------------------------------------------------------------
# 2. Split into valid / invalid
# ------------------------------------------------------------------
valid_files = []
invalid_files = []

for f in uploaded_files:
    ext = os.path.splitext(f.name)[-1].lower()
    if ext in SUPPORTED:
        valid_files.append(f)
    else:
        invalid_files.append(f)

if invalid_files:
    with st.warning("The following files will be skipped (unsupported format):"):
        for f in invalid_files:
            ext = os.path.splitext(f.name)[-1] or "(no extension)"
            st.markdown(f"- **{f.name}** — `{ext}` is not supported")

if not valid_files:
    st.info(f"No supported files found. Please upload files in: {SUPPORTED_DISPLAY}")
    st.stop()

st.info(f"{len(valid_files)} file(s) will be converted.")

# ------------------------------------------------------------------
# 3. Convert each valid file
# ------------------------------------------------------------------
if st.button("Convert", type="primary"):
    results = []   # list of (original_name, markdown | None, error | None)
    progress = st.progress(0, text="Starting…")

    for i, f in enumerate(valid_files):
        progress.progress(i / len(valid_files), text=f"Converting {f.name}…")
        try:
            result = facade.convert_stream(f, f.name)
            results.append((f.name, result, None))
        except Exception as e:
            results.append((f.name, None, str(e)))

    progress.progress(1.0, text="Done.")

    # ------------------------------------------------------------------
    # 4. Report per-file outcome
    # ------------------------------------------------------------------
    successes = [(name, res) for name, res, err in results if res is not None]
    failures  = [(name, err) for name, res, err in results if err is not None]

    if failures:
        with st.expander(f"⚠️ {len(failures)} file(s) failed to convert", expanded=True):
            for name, err in failures:
                st.error(f"**{name}**: {err}")

    if not successes:
        st.error("No files were converted successfully.")
        st.stop()

    st.success(f"{len(successes)} file(s) converted successfully.")

    # ------------------------------------------------------------------
    # 5. Package into ZIP and offer download
    # ------------------------------------------------------------------
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, result in successes:
            stem = os.path.splitext(name)[0]
            if result.assets:
                # Files with images: place in subfolder stem/stem.md + stem/images/...
                zf.writestr(f"{stem}/{stem}.md", result.markdown.encode("utf-8"))
                for asset_path, asset_bytes in result.assets.items():
                    zf.writestr(f"{stem}/{asset_path}", asset_bytes)
            else:
                zf.writestr(f"{stem}.md", result.markdown.encode("utf-8"))
    zip_buffer.seek(0)

    st.download_button(
        label=f"⬇️ Download results ({len(successes)} files)",
        data=zip_buffer,
        file_name="converted.zip",
        mime="application/zip",
    )

    # ------------------------------------------------------------------
    # 6. Per-file preview
    # ------------------------------------------------------------------
    st.divider()
    st.subheader("Preview")

    for name, result in successes:
        with st.expander(name, expanded=len(successes) == 1):
            col1, col2 = st.columns(2)
            with col1:
                st.caption("Markdown source")
                st.code(result.markdown, language="markdown")
            with col2:
                st.caption("Rendered")
                st.markdown(result.markdown)
