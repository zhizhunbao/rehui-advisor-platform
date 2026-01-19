# Handling Complex PDF Content

## Overview

This guide covers advanced techniques for extracting and processing images, tables, and mathematical formulas from PDF files.

---

## 1. Image Extraction

### Method 1: Using PyMuPDF (Recommended)

**Installation:**

```bash
uv add pymupdf
```

**Code:**

```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")

for page_num, page in enumerate(doc, 1):
    image_list = page.get_images()

    for img_index, img in enumerate(image_list, 1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        # Save image
        filename = f"page{page_num}_img{img_index}.{image_ext}"
        with open(filename, "wb") as f:
            f.write(image_bytes)
```

### Method 2: Using pdfplumber

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        # Get image information
        images = page.images
        for img in images:
            # img contains: x0, y0, x1, y1, width, height
            print(f"Image at ({img['x0']}, {img['y0']})")
```

**Note:** pdfplumber detects image locations but doesn't extract pixel data. Use PyMuPDF for actual extraction.

### Markdown Reference Format

```markdown
## Page 1

### Content

Some text before the image...

![Figure 1: PCA Visualization](images/page1_img1.png)

_Figure 1: Principal components shown as green axes_

More text after the image...
```

### Handling Image-Only Pages

For scanned PDFs or image-only pages:

```python
from pdf2image import convert_from_path
import pytesseract

# Convert PDF page to image
images = convert_from_path('document.pdf', first_page=1, last_page=1)

# OCR the image
text = pytesseract.image_to_string(images[0])
```

---

## 2. Table Extraction

### Using pdfplumber (Best for Tables)

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]

    # Extract all tables
    tables = page.extract_tables()

    for table in tables:
        # table is a list of lists
        for row in table:
            print(row)
```

### Convert to Markdown Table

```python
def table_to_markdown(table):
    """Convert table data to markdown format"""
    if not table or not table[0]:
        return ""

    lines = []

    # Header
    header = table[0]
    lines.append("| " + " | ".join(str(cell or "") for cell in header) + " |")

    # Separator
    lines.append("| " + " | ".join("---" for _ in header) + " |")

    # Data rows
    for row in table[1:]:
        if row:
            lines.append("| " + " | ".join(str(cell or "") for cell in row) + " |")

    return "\n".join(lines)
```

### Handling Complex Tables

**Merged Cells:**

```python
# pdfplumber settings for better table detection
table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "intersection_tolerance": 3,
}

tables = page.extract_tables(table_settings)
```

**Multi-line Cells:**

```python
# Clean cell content
def clean_cell(cell):
    if cell:
        return cell.replace('\n', ' ').strip()
    return ""
```

### Example Output

**Original Table:**

```
Length  Width
4       11
8       4
13      5
```

**Markdown:**

```markdown
| Length | Width |
| ------ | ----- |
| 4      | 11    |
| 8      | 4     |
| 13     | 5     |
```

---

## 3. Mathematical Formula Handling

### Detection Strategies

**Method 1: Character-based Detection**

```python
def detect_formula(text):
    """Detect if text contains mathematical formulas"""
    formula_chars = ['=', '∑', '∫', '√', 'λ', 'μ', 'σ', 'α', 'β', 'γ',
                     '±', '×', '÷', '≈', '≠', '≤', '≥', '∞', '∂', '∇']

    return any(char in text for char in formula_chars)
```

**Method 2: Pattern-based Detection**

```python
import re

def is_formula_line(line):
    """Check if line is likely a formula"""
    # Short lines with math operators
    if len(line.strip()) < 100:
        if re.search(r'[=+\-*/^]', line) and re.search(r'\d', line):
            return True
    return False
```

### Formatting Options

**Option 1: Code Blocks**

```markdown
For the first value 4:
```

(4 - 8) / 3.74 = -1.07

```

```

**Option 2: Inline Code**

```markdown
The formula `z = (x - μ) / σ` standardizes the data.
```

**Option 3: LaTeX (for complex formulas)**

```markdown
$$
\lambda_1 = 1.61, \quad \lambda_2 = 0.39
$$

The eigenvalue equation:

$$
|C - \lambda I| = 0
$$
```

**Option 4: Unicode Symbols**

```markdown
λ₁ = 1.61, λ₂ = 0.39

Covariance: Sxy = Σ(Xi × Yi) / (n-1)
```

### Common Mathematical Symbols

| Symbol | Unicode | LaTeX    | Description           |
| ------ | ------- | -------- | --------------------- |
| λ      | λ       | \lambda  | Lambda                |
| μ      | μ       | \mu      | Mu (mean)             |
| σ      | σ       | \sigma   | Sigma (std dev)       |
| Σ      | Σ       | \Sigma   | Summation             |
| √      | √       | \sqrt    | Square root           |
| ≈      | ≈       | \approx  | Approximately         |
| ≠      | ≠       | \neq     | Not equal             |
| ≤      | ≤       | \leq     | Less than or equal    |
| ≥      | ≥       | \geq     | Greater than or equal |
| ∞      | ∞       | \infty   | Infinity              |
| ∂      | ∂       | \partial | Partial derivative    |
| ∫      | ∫       | \int     | Integral              |

### Extracting Formulas from PDF

```python
def extract_formulas(page):
    """Extract potential formulas from page"""
    text = page.extract_text()
    lines = text.split('\n')

    formulas = []
    for line in lines:
        if is_formula_line(line):
            formulas.append(line.strip())

    return formulas
```

---

## 4. Complete Workflow Example

````python
import pdfplumber
import fitz  # PyMuPDF
from pathlib import Path

def extract_pdf_with_all_content(pdf_path):
    """Extract text, images, tables, and formulas"""

    pdf_path = Path(pdf_path)
    output_dir = pdf_path.parent
    images_dir = output_dir / f"{pdf_path.stem}_images"
    images_dir.mkdir(exist_ok=True)

    markdown_lines = []
    markdown_lines.append(f"# {pdf_path.stem}\n")

    # Open with both libraries
    pdf_plumber = pdfplumber.open(pdf_path)
    pdf_fitz = fitz.open(pdf_path)

    for page_num in range(len(pdf_plumber.pages)):
        page_pb = pdf_plumber.pages[page_num]
        page_fitz = pdf_fitz[page_num]

        markdown_lines.append(f"## Page {page_num + 1}\n")

        # 1. Extract images with PyMuPDF
        image_list = page_fitz.get_images()
        if image_list:
            markdown_lines.append("### Images\n")
            for img_index, img in enumerate(image_list, 1):
                xref = img[0]
                base_image = pdf_fitz.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                img_filename = f"page{page_num+1}_img{img_index}.{image_ext}"
                img_path = images_dir / img_filename

                with open(img_path, "wb") as f:
                    f.write(image_bytes)

                markdown_lines.append(f"![Image {img_index}]({images_dir.name}/{img_filename})\n")

        # 2. Extract tables with pdfplumber
        tables = page_pb.extract_tables()
        if tables:
            markdown_lines.append("### Tables\n")
            for i, table in enumerate(tables, 1):
                markdown_lines.append(f"**Table {i}:**\n")
                markdown_lines.append(table_to_markdown(table))
                markdown_lines.append("\n")

        # 3. Extract text and detect formulas
        text = page_pb.extract_text()
        markdown_lines.append("### Content\n")

        lines = text.split('\n')
        for line in lines:
            if is_formula_line(line):
                markdown_lines.append(f"```\n{line}\n```\n")
            else:
                markdown_lines.append(line + "\n")

        markdown_lines.append("\n---\n")

    # Save markdown
    output_path = output_dir / f"{pdf_path.stem}_complete.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_lines))

    pdf_plumber.close()
    pdf_fitz.close()

    return output_path
````

---

## 5. Best Practices

### For Images

- ✅ Save images in separate folder
- ✅ Use descriptive filenames: `page1_fig1_pca_plot.png`
- ✅ Add captions in markdown
- ✅ Compress large images if needed
- ❌ Don't embed base64 images in markdown (too large)

### For Tables

- ✅ Verify table structure after extraction
- ✅ Clean up merged cells manually if needed
- ✅ Add table captions
- ✅ Use consistent column alignment
- ❌ Don't force complex tables into markdown (use image instead)

### For Formulas

- ✅ Use LaTeX for complex formulas
- ✅ Use Unicode for simple symbols
- ✅ Add explanations for variables
- ✅ Test formula rendering
- ❌ Don't mix notation styles

### General

- ✅ Test extraction on sample pages first
- ✅ Manual review is always needed
- ✅ Keep original PDF as reference
- ✅ Document any manual corrections
- ❌ Don't expect 100% automated accuracy

---

## 6. Troubleshooting

### Images Not Extracting

- Check if PDF has embedded images (not just rendered graphics)
- Try different libraries (PyMuPDF vs pdfplumber)
- Consider converting page to image and cropping

### Tables Misaligned

- Adjust pdfplumber table settings
- Try different strategies: "lines", "lines_strict", "text"
- Manual cleanup may be needed

### Formulas Garbled

- Check PDF encoding
- Use OCR for scanned documents
- Manually rewrite complex formulas in LaTeX

### Large File Size

- Compress images before embedding
- Use external image references
- Split large PDFs into sections

---

## 7. Tools Summary

| Tool           | Best For              | Installation         |
| -------------- | --------------------- | -------------------- |
| pypdf          | Basic text extraction | `uv add pypdf`       |
| pdfplumber     | Tables, layout        | `uv add pdfplumber`  |
| PyMuPDF (fitz) | Images, rendering     | `uv add pymupdf`     |
| pdf2image      | Page to image         | `uv add pdf2image`   |
| pytesseract    | OCR                   | `uv add pytesseract` |

**Recommended Stack:**

- **pdfplumber** for tables and text
- **PyMuPDF** for images
- **pytesseract** for scanned PDFs (if needed)
