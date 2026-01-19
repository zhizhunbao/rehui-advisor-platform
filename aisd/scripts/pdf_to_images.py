"""
Convert PDF pages to images
将PDF页面转换为图片

This is useful for extracting vector graphics/charts that can't be extracted as separate images.
"""

import sys
import argparse
from pathlib import Path

try:
    from pdf2image import convert_from_path
except ImportError:
    print("Error: pdf2image not installed. Run: uv add pdf2image")
    sys.exit(1)


def pdf_to_images(pdf_path: str, output_dir: str = None, dpi: int = 300, 
                  first_page: int = None, last_page: int = None):
    """
    Convert PDF pages to images
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory for images
        dpi: Resolution (default 300 for high quality)
        first_page: First page to convert (1-indexed)
        last_page: Last page to convert (1-indexed)
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        return
    
    # Setup output directory
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print("PDF to Images Converter")
    print(f"{'='*60}")
    print(f"PDF: {pdf_path.name}")
    print(f"Output: {output_dir}")
    print(f"DPI: {dpi}")
    if first_page or last_page:
        print(f"Pages: {first_page or 1} to {last_page or 'end'}")
    print(f"{'='*60}\n")
    
    try:
        # Convert PDF to images
        print("Converting PDF pages to images...")
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page
        )
        
        print(f"✓ Converted {len(images)} pages\n")
        
        # Save images
        print("Saving images...")
        for i, image in enumerate(images, start=first_page or 1):
            image_path = output_dir / f"page_{i:03d}.png"
            image.save(image_path, 'PNG')
            print(f"  ✓ Saved: {image_path.name}")
        
        print(f"\n{'='*60}")
        print("✓ Conversion complete!")
        print(f"{'='*60}")
        print(f"\nImages saved to: {output_dir}")
        print(f"Total images: {len(images)}")
        
        # File size info
        total_size = sum(f.stat().st_size for f in output_dir.glob("*.png"))
        print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
        
        print("\nNext steps:")
        print("1. Review the generated images")
        print("2. Crop specific charts/figures if needed")
        print("3. Reference images in your markdown documents")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: pdf2image requires poppler to be installed:")
        print("  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/")
        print("  Mac: brew install poppler")
        print("  Linux: sudo apt-get install poppler-utils")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to high-quality images"
    )
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--output-dir", help="Output directory for images")
    parser.add_argument("--dpi", type=int, default=300, 
                       help="Image resolution (default: 300)")
    parser.add_argument("--first-page", type=int, 
                       help="First page to convert (1-indexed)")
    parser.add_argument("--last-page", type=int,
                       help="Last page to convert (1-indexed)")
    
    args = parser.parse_args()
    
    pdf_to_images(
        args.pdf_path,
        args.output_dir,
        args.dpi,
        args.first_page,
        args.last_page
    )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("PDF to Images Converter")
        print("=" * 60)
        print("\nUsage:")
        print("  python scripts/pdf_to_images.py <pdf_path> [options]")
        print("\nOptions:")
        print("  --output-dir <dir>    Output directory")
        print("  --dpi <number>        Resolution (default: 300)")
        print("  --first-page <n>      First page to convert")
        print("  --last-page <n>       Last page to convert")
        print("\nExamples:")
        print("  # Convert all pages")
        print("  python scripts/pdf_to_images.py lecture.pdf")
        print("\n  # Convert specific pages")
        print("  python scripts/pdf_to_images.py lecture.pdf --first-page 1 --last-page 3")
        print("\n  # High resolution")
        print("  python scripts/pdf_to_images.py lecture.pdf --dpi 600")
        print("\nNote: Requires poppler to be installed on your system")
        sys.exit(0)
    
    main()
