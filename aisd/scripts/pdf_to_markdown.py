"""
Convert PDF slides to markdown with bilingual support
"""
import sys
from pathlib import Path
import pdfplumber
import fitz  # PyMuPDF
import re
from PIL import Image
import io


def extract_images_from_page(pdf_document, page_num, output_dir: Path, min_width=200, min_height=150):
    """Extract meaningful images from a PDF page using PyMuPDF
    
    Args:
        min_width: Minimum image width to extract (filters out icons/logos)
        min_height: Minimum image height to extract
    """
    page = pdf_document[page_num - 1]  # 0-indexed
    image_list = page.get_images()
    
    extracted_images = []
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        try:
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_width = base_image["width"]
            image_height = base_image["height"]
            
            # Filter out small images (likely icons, logos, decorations)
            if image_width < min_width or image_height < min_height:
                continue
            
            # Filter out very small file sizes (likely decorative elements)
            if len(image_bytes) < 20000:  # Less than 20KB
                continue
            
            # Save image
            image_filename = f"page{page_num}_img{img_index + 1}.{image_ext}"
            image_path = output_dir / image_filename
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            extracted_images.append({
                'filename': image_filename,
                'width': image_width,
                'height': image_height
            })
        except Exception as e:
            print(f"  Warning: Could not extract image {img_index + 1} from page {page_num}: {e}")
    
    return extracted_images


def extract_pdf_to_markdown(pdf_path: Path, output_path: Path, extract_images: bool = True):
    """Extract PDF content and convert to structured markdown"""
    
    # Create images directory if extracting images
    images_dir = None
    if extract_images:
        images_dir = output_path.parent / f"{output_path.stem}_images"
        images_dir.mkdir(parents=True, exist_ok=True)
    
    # Open PDF with PyMuPDF for image extraction
    pdf_document = fitz.open(pdf_path) if extract_images else None
    
    with pdfplumber.open(pdf_path) as pdf:
        markdown_content = []
        markdown_content.append(f"# {pdf_path.stem.replace('_', ' ').title()}\n\n")
        markdown_content.append(f"**Source:** `{pdf_path.name}`  \n")
        markdown_content.append(f"**Total Pages:** {len(pdf.pages)}\n\n")
        markdown_content.append("---\n\n")
        
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text
            text = page.extract_text()
            
            if not text or not text.strip():
                markdown_content.append(f"## Page {page_num}\n\n")
                markdown_content.append("*[No text content or image-only page]*\n\n")
                markdown_content.append("---\n\n")
                continue
            
            # Add page header
            markdown_content.append(f"## Page {page_num}\n\n")
            
            # Extract images if enabled
            if extract_images and pdf_document:
                images = extract_images_from_page(pdf_document, page_num, images_dir)
                if images:
                    markdown_content.append("\n**📷 Images:**\n\n")
                    for img_info in images:
                        rel_path = f"{images_dir.name}/{img_info['filename']}"
                        markdown_content.append(f"![Page {page_num} Image]({rel_path})  \n")
                    markdown_content.append("\n")
            
            # Clean and format text
            lines = text.split('\n')
            formatted_lines = []
            prev_line = ""
            title_buffer = []  # Buffer for multi-line titles
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    # Flush title buffer if exists
                    if title_buffer:
                        combined_title = " ".join(title_buffer)
                        formatted_lines.append(f"\n### {combined_title}\n")
                        title_buffer = []
                    continue
                
                # Skip page numbers at the end
                if line.isdigit() or re.match(r'^Page\s+\d+$', line):
                    continue
                
                # Skip duplicate content (common in PDF extraction)
                if line == prev_line:
                    continue
                
                # Detect potential title lines (short, all caps or title case)
                # Exclude lines that start with bullet points or special markers
                is_potential_title = (
                    len(line) < 50 and 
                    (line.isupper() or (line.istitle() and len(line.split()) <= 5)) and 
                    not line.endswith(('.', ',', ';', ':')) and
                    not re.match(r'^[❑•\-·○]\s+', line) and  # Not a bullet point
                    not line.startswith('❑')  # Not a checkbox item
                )
                
                if is_potential_title:
                    # Add to title buffer
                    title_buffer.append(line)
                else:
                    # Flush title buffer if exists
                    if title_buffer:
                        combined_title = " ".join(title_buffer)
                        formatted_lines.append(f"\n### {combined_title}\n")
                        title_buffer = []
                    
                    # Detect bullet points (❑, •, -, ·, ○)
                    bullet_pattern = r'^[❑•\-·○]\s+'
                    if re.match(bullet_pattern, line):
                        formatted_lines.append(f"- {re.sub(bullet_pattern, '', line)}")
                    # Detect numbered lists
                    elif re.match(r'^\d+[\.\)]\s+', line):
                        formatted_lines.append(line)
                    # Regular text
                    else:
                        formatted_lines.append(line)
                
                prev_line = line
            
            # Flush any remaining title buffer
            if title_buffer:
                combined_title = " ".join(title_buffer)
                formatted_lines.append(f"\n### {combined_title}\n")
            
            markdown_content.append('\n'.join(formatted_lines))
            markdown_content.append("\n\n")
            
            # Extract tables if any (only if they have meaningful content and not duplicate text)
            tables = page.extract_tables()
            if tables:
                # Get all text content for comparison (remove all whitespace for better matching)
                page_text_normalized = ''.join(text.lower().split())
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    # Check if table has meaningful content (not just empty cells)
                    has_content = any(
                        any(cell and str(cell).strip() for cell in row)
                        for row in table
                    )
                    
                    if not has_content or len(table[0]) <= 1:
                        continue
                    
                    # Normalize table content for comparison
                    table_text_normalized = ''.join(
                        ''.join(str(cell or '').strip() for cell in row)
                        for row in table
                    ).lower().replace(' ', '')
                    
                    # Calculate similarity - if >80% of table text is in page text, it's duplicate
                    if len(table_text_normalized) > 20:
                        # Count how many characters from table are in page text
                        similarity = sum(1 for char in table_text_normalized if char in page_text_normalized) / len(table_text_normalized)
                        if similarity > 0.8:
                            continue  # Skip duplicate table
                    
                    # This is a unique table, add it
                    markdown_content.append("\n**Table:**\n\n")
                    # Header
                    header = [str(cell or "").strip() for cell in table[0]]
                    if any(header):  # Only add if header has content
                        markdown_content.append("| " + " | ".join(header) + " |\n")
                        markdown_content.append("| " + " | ".join(["---"] * len(header)) + " |\n")
                        # Rows
                        for row in table[1:]:
                            cells = [str(cell or "").strip() for cell in row]
                            if any(cells):  # Only add rows with content
                                markdown_content.append("| " + " | ".join(cells) + " |\n")
                    markdown_content.append("\n")
            
            # Add note section for each page
            markdown_content.append("**📝 Notes / 笔记:**\n\n")
            markdown_content.append("> [Add your notes here / 在此添加笔记]\n\n")
            markdown_content.append("---\n\n")
        
        # Close PyMuPDF document
        if pdf_document:
            pdf_document.close()
        
        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text('\n'.join(markdown_content), encoding='utf-8')
        print(f"✓ Converted: {pdf_path.name} → {output_path.name}")
        print(f"  Pages: {len(pdf.pages)}")
        if extract_images and images_dir:
            image_count = len(list(images_dir.glob("*")))
            if image_count > 0:
                print(f"  Images: {image_count} extracted to {images_dir.name}/")


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_markdown.py <pdf_file> [output_file] [--no-images]")
        print("Example: python pdf_to_markdown.py lecture1.pdf notes/lecture1.md")
        print("         python pdf_to_markdown.py lecture1.pdf notes/lecture1.md --no-images")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    # Check for --no-images flag
    extract_images = "--no-images" not in sys.argv
    
    # Determine output path
    if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
        output_path = Path(sys.argv[2])
    else:
        output_path = pdf_path.parent / "notes" / f"{pdf_path.stem}_notes.md"
    
    extract_pdf_to_markdown(pdf_path, output_path, extract_images)
    print(f"\n✓ Markdown file created: {output_path}")


if __name__ == "__main__":
    main()
