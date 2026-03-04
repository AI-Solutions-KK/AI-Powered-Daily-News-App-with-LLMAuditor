#!/usr/bin/env python3
"""
Convert PDF certification report to images for README display
"""

from pathlib import Path

def convert_pdf_to_images():
    """Convert the PDF report to images"""
    
    pdf_files = list(Path("reports").glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in reports/")
        return False
        
    pdf_path = pdf_files[0]  # Use the first PDF found
    print(f"🔄 Converting {pdf_path} to images...")
    
    # Create images directory
    images_dir = Path("reports/images")
    images_dir.mkdir(exist_ok=True)
    
    try:
        from pdf2image import convert_from_path
        
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=150)
        
        image_paths = []
        for i, image in enumerate(images):
            image_path = images_dir / f"certification_page_{i+1}.png"
            image.save(image_path, "PNG", optimize=True)
            image_paths.append(str(image_path))
            print(f"✅ Saved: {image_path}")
        
        print(f"\n📷 Generated {len(image_paths)} images")
        return image_paths[0] if image_paths else False  # Return first image
        
    except ImportError:
        print("❌ pdf2image not available")
        return False
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        return False

if __name__ == "__main__":
    convert_pdf_to_images()