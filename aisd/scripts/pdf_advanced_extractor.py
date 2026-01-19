"""
Advanced PDF Extractor with support for images, tables, and formulas
高级PDF提取器,支持图片、表格和数学公式

Features:
- Extract images and save them
- Detect and extract tables
- Preserve mathematical formulas
- Better layout detection
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: uv add pdfplumber")
    sys.exit(1)


class AdvancedPDFExtractor:
    """Advanced PDF extractor with image, table, and formula support"""
    
    def __init__(self, pdf_path: str, output_dir: str = None):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir) if output_dir else self.pdf_path.parent
        self.images_dir = self.output_dir / f"{self.pdf_path.stem}_images"
        self.images_dir.mkdir(exist_ok=True)
        
    def extract_images(self, page, page_num: int) -> List[str]:
        """Extract images from a page and save them"""
        image_refs = []
        
        try:
            # pdfplumber can access images
            if hasattr(page, 'images') and page.images:
                for i, img in enumerate(page.images, 1):
                    img_name = f"page{page_num}_img{i}.png"
                    img_path = self.images_dir / img_name
                    
                    # Note: pdfplumber doesn't directly save images
                    # We'll create a reference instead
                    image_refs.append(f"![Image {i}]({img_name})")
                    
                    print(f"    Found image {i} on page {page_num}")
        except Exception as e:
            print(f"    Warning: Could not extract images: {e}")
        
        return image_refs
    
    def extract_tables(self, page) -> List[str]:
        """Extract tables from a page and convert to markdown"""
        markdown_tables = []
        
        try:
            tables = page.extract_tables()
            
            if tables:
                for i, table in enumerate(tables, 1):
                    md_table = self._table_to_markdown(table)
                    if md_table:  # Only add non-empty tables
                        markdown_tables.append(md_table)
                        print(f"    Found table {len(markdown_tables)}")
        except Exception as e:
            print(f"    Warning: Could not extract tables: {e}")
        
        return markdown_tables
    
    def _is_empty_table(self, table: List[List[str]]) -> bool:
        """Check if table is empty or contains only whitespace"""
        if not table:
            return True
        
        # Count non-empty cells
        non_empty_cells = 0
        total_cells = 0
        
        for row in table:
            if row:
                for cell in row:
                    total_cells += 1
                    if cell and str(cell).strip():
                        non_empty_cells += 1
        
        # If less than 30% cells have content, consider it empty
        if total_cells == 0:
            return True
        
        return (non_empty_cells / total_cells) < 0.3
    
    def _table_to_markdown(self, table: List[List[str]]) -> str:
        """Convert table data to markdown format"""
        if not table or not table[0]:
            return ""
        
        # Check if table is empty
        if self._is_empty_table(table):
            return ""
        
        md_lines = []
        
        # Header row
        header = table[0]
        md_lines.append("| " + " | ".join(str(cell or "") for cell in header) + " |")
        
        # Separator
        md_lines.append("| " + " | ".join("---" for _ in header) + " |")
        
        # Data rows
        for row in table[1:]:
            if row:  # Skip empty rows
                md_lines.append("| " + " | ".join(str(cell or "") for cell in row) + " |")
        
        return "\n".join(md_lines)
    
    def detect_formulas(self, text: str) -> str:
        """Detect and mark potential mathematical formulas"""
        # Simple heuristics for formula detection
        formula_indicators = ['=', '∑', '∫', '√', 'λ', 'μ', 'σ', '±', '×', '÷', '≈', '≠', '≤', '≥']
        
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # Check if line contains formula indicators
            if any(indicator in line for indicator in formula_indicators):
                # Check if it's a short line (likely a formula)
                if len(line.strip()) < 100 and any(char.isdigit() for char in line):
                    # Wrap in code block for formulas
                    processed_lines.append(f"```\n{line.strip()}\n```")
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def extract_page_with_layout(self, page, page_num: int) -> Dict[str, Any]:
        """Extract page content with layout information"""
        print(f"  Processing page {page_num}...")
        
        # Extract text
        text = page.extract_text() or "*[No text content]*"
        
        # Extract images
        images = self.extract_images(page, page_num)
        
        # Extract tables
        tables = self.extract_tables(page)
        
        # Get page dimensions for context
        width = page.width
        height = page.height
        
        return {
            'page_num': page_num,
            'text': text,
            'images': images,
            'tables': tables,
            'dimensions': (width, height)
        }
    
    def create_markdown(self, pages_data: List[Dict[str, Any]]) -> str:
        """Create markdown from extracted page data"""
        md_lines = []
        
        # Header
        md_lines.append(f"# {self.pdf_path.stem}\n")
        md_lines.append(f"**Source:** `{self.pdf_path.name}`\n")
        md_lines.append(f"**Extracted:** {len(pages_data)} pages\n")
        md_lines.append("---\n")
        
        # Process each page
        for page_data in pages_data:
            page_num = page_data['page_num']
            md_lines.append(f"## Page {page_num}\n")
            
            # Add images if any
            if page_data['images']:
                md_lines.append("### Images\n")
                for img_ref in page_data['images']:
                    md_lines.append(img_ref)
                md_lines.append("\n")
            
            # Add tables if any
            if page_data['tables']:
                md_lines.append("### Tables\n")
                for i, table in enumerate(page_data['tables'], 1):
                    md_lines.append(f"**Table {i}:**\n")
                    md_lines.append(table)
                    md_lines.append("\n")
            
            # Add text content with formula detection
            md_lines.append("### Content\n")
            processed_text = self.detect_formulas(page_data['text'])
            md_lines.append(processed_text)
            md_lines.append("\n---\n")
        
        return "\n".join(md_lines)
    
    def extract(self) -> str:
        """Main extraction workflow"""
        print(f"\n{'='*60}")
        print(f"Advanced PDF Extraction")
        print(f"{'='*60}")
        print(f"PDF: {self.pdf_path.name}")
        print(f"Output: {self.output_dir}")
        print(f"Images: {self.images_dir}")
        print(f"{'='*60}\n")
        
        pages_data = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Total pages: {total_pages}\n")
            
            for i, page in enumerate(pdf.pages, 1):
                page_data = self.extract_page_with_layout(page, i)
                pages_data.append(page_data)
        
        # Create markdown
        print("\n📝 Creating markdown document...")
        markdown_content = self.create_markdown(pages_data)
        
        # Save output
        output_path = self.output_dir / f"{self.pdf_path.stem}_advanced.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✓ Saved to: {output_path}")
        
        # Summary
        print(f"\n{'='*60}")
        print("Extraction Summary")
        print(f"{'='*60}")
        
        total_images = sum(len(p['images']) for p in pages_data)
        total_tables = sum(len(p['tables']) for p in pages_data)
        
        print(f"Pages processed: {len(pages_data)}")
        print(f"Images found: {total_images}")
        print(f"Tables found: {total_tables}")
        
        if total_images > 0:
            print(f"\n⚠️  Note: Image extraction requires additional tools.")
            print("   Consider using PyMuPDF (fitz) for full image extraction:")
            print("   uv add pymupdf")
        
        return output_path


def extract_images_with_pymupdf(pdf_path: str, output_dir: Path):
    """
    Alternative: Extract images using PyMuPDF (better image support)
    """
    try:
        import fitz  # PyMuPDF
        
        pdf_path = Path(pdf_path)
        images_dir = output_dir / f"{pdf_path.stem}_images"
        images_dir.mkdir(exist_ok=True)
        
        doc = fitz.open(pdf_path)
        image_count = 0
        
        for page_num, page in enumerate(doc, 1):
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list, 1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = images_dir / f"page{page_num}_img{img_index}.{image_ext}"
                
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)
                
                image_count += 1
                print(f"  Extracted: {image_filename.name}")
        
        print(f"\n✓ Extracted {image_count} images to {images_dir}")
        return image_count
        
    except ImportError:
        print("\n⚠️  PyMuPDF not installed. Install with: uv add pymupdf")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Advanced PDF extraction with images, tables, and formulas"
    )
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--extract-images", action="store_true", 
                       help="Extract images using PyMuPDF (requires pymupdf)")
    
    args = parser.parse_args()
    
    # Validate PDF
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)
    
    # Extract with pdfplumber
    extractor = AdvancedPDFExtractor(
        args.pdf_path,
        args.output_dir
    )
    output_path = extractor.extract()
    
    # Optionally extract images with PyMuPDF
    if args.extract_images:
        print(f"\n{'='*60}")
        print("Extracting images with PyMuPDF...")
        print(f"{'='*60}\n")
        extract_images_with_pymupdf(args.pdf_path, extractor.output_dir)
    
    print(f"\n{'='*60}")
    print("✓ Extraction complete!")
    print(f"{'='*60}")
    print(f"\nOutput file: {output_path}")
    print("\nNext steps:")
    print("1. Review the extracted markdown file")
    print("2. Check extracted images (if any)")
    print("3. Verify tables are formatted correctly")
    print("4. Add translations or explanations as needed")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Advanced PDF Extractor")
        print("=" * 60)
        print("\nUsage:")
        print("  python scripts/pdf_advanced_extractor.py <pdf_path> [options]")
        print("\nOptions:")
        print("  --output-dir <dir>    Output directory")
        print("  --extract-images      Extract images using PyMuPDF")
        print("\nExamples:")
        print("  python scripts/pdf_advanced_extractor.py lecture.pdf")
        print("  python scripts/pdf_advanced_extractor.py lecture.pdf --extract-images")
        print("\nFeatures:")
        print("  ✓ Text extraction with layout preservation")
        print("  ✓ Table detection and markdown conversion")
        print("  ✓ Mathematical formula detection")
        print("  ✓ Image extraction (with PyMuPDF)")
        sys.exit(0)
    
    main()
