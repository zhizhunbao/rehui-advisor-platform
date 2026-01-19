---
name: dev-pdf_processing
description: PDF processing and conversion assistant. Use when (1) user needs to extract text from PDF files, (2) convert PDF to markdown format, (3) create bilingual (Chinese-English) documentation from PDFs, (4) process academic papers or course materials.
---

# PDF Processing Assistant

## Objectives

- Extract text content from PDF files accurately
- Convert PDF to clean markdown format
- Generate bilingual (中英文) documentation
- Handle academic papers, slides, and course materials
- Preserve structure (headings, tables, formulas)

## Core Workflow

### 1. PDF Text Extraction

**Install dependencies:**

```bash
uv add pypdf  # or pdfplumber for better table support
```

**Basic extraction script:**

```python
from pypdf import PdfReader

with open('input.pdf', 'rb') as file:
    reader = PdfReader(file)
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        # Process text
```

### 2. Convert to Markdown

**Structure preservation:**

- Detect headings (font size, bold text)
- Extract tables → markdown tables
- Preserve lists and formatting
- Handle mathematical formulas (if possible)

**Output format:**

```markdown
# Title

## Section

Content...

| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |
```

### 3. Bilingual Documentation

**Two approaches:**

**A. Side-by-side format:**

```markdown
## Concept Name | 概念名称

English explanation... | 中文解释...
```

**B. Separate sections:**

```markdown
## English Version

Content in English...

---

## 中文版本

中文内容...
```

**Translation workflow:**

1. Extract English content from PDF
2. Use LLM to translate technical terms accurately
3. Preserve code blocks, formulas, and tables
4. Format as bilingual markdown

### 4. Academic Material Processing

**For course slides/papers:**

- Extract page-by-page with clear separators
- Identify and preserve mathematical notation
- Extract tables and figures (describe if image-only)
- Create summary sections
- Add explanatory notes

## Key Instructions

### PDF Extraction Best Practices

1. **Choose the right library:**
   - `pypdf`: Fast, basic text extraction (lightweight)
   - `pdfplumber`: Better for tables and layout detection
   - `PyMuPDF (fitz)`: Best for images, complex layouts, and rendering
   - `pdf2image` + `pytesseract`: For OCR on scanned PDFs

2. **Handle different content types:**

   **Images:**
   - Use PyMuPDF to extract embedded images
   - Save images to separate folder: `{pdf_name}_images/`
   - Reference in markdown: `![Description](images/page1_img1.png)`
   - For image-only pages: Consider OCR

   **Tables:**
   - Use `pdfplumber.extract_tables()` for structured tables
   - Convert to markdown table format
   - Verify alignment and merged cells
   - Manual cleanup may be needed for complex tables

   **Mathematical Formulas:**
   - Detect formula indicators: `=`, `∑`, `∫`, `λ`, `μ`, `σ`
   - Wrap in code blocks or LaTeX: `` `formula` `` or `$$formula$$`
   - Use Unicode symbols when possible
   - For complex formulas, describe in text or use LaTeX

3. **Preserve structure:**
   - Add page markers: `## Page N`
   - Use horizontal rules: `---`
   - Maintain heading hierarchy
   - Group related content (text, tables, images)

### Bilingual Conversion

1. **Technical term consistency:**
   - Create glossary for key terms
   - Use standard translations (e.g., PCA → 主成分分析)
   - Keep English terms in parentheses: "主成分分析 (PCA)"

2. **Formula handling:**
   - Keep mathematical notation in English
   - Translate variable descriptions
   - Use LaTeX format when possible

3. **Code preservation:**
   - Never translate code blocks
   - Translate comments if present
   - Add bilingual explanations around code

### Quality Checks

- [ ] All pages extracted successfully
- [ ] Tables formatted correctly
- [ ] Formulas preserved or noted
- [ ] Bilingual terms consistent
- [ ] Markdown syntax valid
- [ ] File structure clear and navigable

## Common Patterns

### Pattern 1: Course Material PDF → Study Notes

```python
# Extract PDF
# ↓
# Convert to markdown with page markers
# ↓
# Add explanatory notes and examples
# ↓
# Create bilingual version with translations
# ↓
# Generate summary and key concepts
```

### Pattern 2: Academic Paper → Bilingual Summary

```python
# Extract abstract, sections, conclusions
# ↓
# Translate to Chinese
# ↓
# Create side-by-side comparison
# ↓
# Add technical glossary
```

### Pattern 3: Slides → Interactive Notes

```python
# Extract slide content
# ↓
# Expand bullet points into full explanations
# ↓
# Add code examples
# ↓
# Create practice questions
```

## File Organization

**Recommended structure:**

```
course/
├── slides/
│   └── lecture1.pdf          # Original PDF
├── notes/
│   ├── lecture1_extracted.md # Raw extraction
│   ├── lecture1_explained.md # With explanations
│   └── lecture1_bilingual.md # Bilingual version
└── labs/
    └── lab1_practice.py      # Practice code
```

## Validation

Before completing PDF processing:

1. **Completeness:** All pages extracted?
2. **Accuracy:** Text matches PDF content?
3. **Structure:** Markdown renders correctly?
4. **Bilingual:** Translations accurate and consistent?
5. **Usability:** Easy to navigate and understand?

## Example Usage

**User request:** "把这个PCA的PDF转成markdown并做成中英文对照"

**Your workflow:**

1. Extract PDF using pypdf/pdfplumber
2. Save as `*_extracted.md` with page markers
3. Create `*_explained.md` with detailed notes
4. Generate `*_bilingual.md` with translations
5. Ensure technical terms are consistent

## References

For detailed implementation examples, see:

- `references/extraction_examples.md` - PDF extraction code samples
- `references/bilingual_templates.md` - Bilingual formatting templates
- `references/academic_processing.md` - Academic paper processing guide
