# PDF Processing Scripts

Comprehensive PDF processing toolkit combining Anthropic's official PDF skill best practices with academic-focused conversion tools.

## 🚀 pdf_converter.py (Recommended - Unified Tool)

**All-in-one PDF converter** for academic materials - course slides, papers, lab manuals.

### Features

- ✅ Convert PDF to structured markdown
- ✅ Extract and save images (smart filtering)
- ✅ Preserve structure (headings, lists, tables)
- ✅ Create bilingual (English-Chinese) templates
- ✅ Multiple bilingual formats (inline, side-by-side, separate)
- ✅ Smart duplicate detection
- ✅ Bilingual note sections

### Quick Start

```bash
# Basic conversion (recommended for most use cases)
uv run python pdf_converter.py lecture.pdf

# Bilingual template
uv run python pdf_converter.py lecture.pdf --bilingual

# No image extraction (faster)
uv run python pdf_converter.py lecture.pdf --no-images

# Custom output path
uv run python pdf_converter.py lecture.pdf -o notes/lecture1.md

# Bilingual with specific format
uv run python pdf_converter.py lecture.pdf --bilingual --format separate
```

### Real-World Examples

```bash
# Convert NLP lab PDF
uv run python pdf_converter.py "aisd/courses/nlp/labs/CST8507_Lab 1_W26.pdf"

# Convert ML slides with bilingual notes
uv run python pdf_converter.py "aisd/courses/ml/slides/PCA_ExampleInClass.pdf" --bilingual

# Convert without images (for text-heavy documents)
uv run python pdf_converter.py "aisd/courses/rl/resources/SuttonReinforcementLearning.pdf" --no-images
```

---

## 📚 Additional Capabilities (from Anthropic PDF Skill)

Our SKILL.md integrates best practices from Anthropic's official PDF skill:

### Core Operations

- **Extract text and tables** - `pdfplumber` for best results
- **Merge/split PDFs** - `pypdf` for fast operations
- **Fill PDF forms** - Programmatic form filling
- **Create PDFs** - `reportlab` for professional output
- **OCR scanned PDFs** - `pytesseract` + `pdf2image`
- **Extract images** - `pdfimages` CLI or `PyMuPDF`
- **Password protection** - Encrypt/decrypt PDFs
- **Add watermarks** - Overlay content on pages

### Command-Line Tools

```bash
# Extract text (fastest)
pdftotext -layout input.pdf output.txt

# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Extract images
pdfimages -all document.pdf images/img

# Convert to images
pdftoppm -png -r 300 document.pdf output_prefix
```

### Python Examples

See `SKILL.md` for comprehensive examples of:

- Table extraction with pandas
- Form filling workflows
- Batch processing with error handling
- Metadata extraction
- Advanced PDF manipulation

---

## Dependencies

```bash
# Install required dependencies for pdf_converter.py
uv add pdfplumber pymupdf pypdf

# Optional: For OCR support
uv add pytesseract pdf2image
```

## See Also

- **SKILL.md** - Comprehensive PDF processing guide with all techniques
- **Anthropic PDF Skill** - Official skill in `backend/scripts/discover/raw_data/ai_skills/skills/pdf/`
