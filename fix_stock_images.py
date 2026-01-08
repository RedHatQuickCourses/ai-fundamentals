#!/usr/bin/env python3
"""
Extract stock-image.jpg files with unique names and create mapping
"""
import os
import shutil
import re

# Mapping from original path to unique filename
image_mapping = {
    'scormcontent/assets/stock-image.jpg': 'stock-image-intro-1.jpg',
    'scormcontent/assets/79AzwS/stock-image.jpg': 'stock-image-intro-2.jpg',
    'scormcontent/assets/Uettbr/stock-image.jpg': 'stock-image-intro-3.jpg',
    'scormcontent/assets/KfrlT7/stock-image.jpg': 'stock-image-predictive-1.jpg',
    'scormcontent/assets/S-oN69/stock-image.jpg': 'stock-image-predictive-2.jpg',
    'scormcontent/assets/Va3Gu4/stock-image.jpg': 'stock-image-predictive-3.jpg',
    'scormcontent/assets/_nM_yG/stock-image.jpg': 'stock-image-security-1.jpg',
    'scormcontent/assets/MTPS-b/stock-image.jpg': 'stock-image-security-2.jpg',
    'scormcontent/assets/nmmmtB/stock-image.jpg': 'stock-image-other-1.jpg',
    'scormcontent/assets/jdWXSw/stock-image.jpg': 'stock-image-other-2.jpg',
}

def extract_and_rename_images():
    """Extract stock images with unique names"""
    # Extract all stock-image.jpg files
    os.system('unzip -q -o ai-fundamenals-scorm.zip "scormcontent/assets/*/stock-image.jpg" "scormcontent/assets/stock-image.jpg" -d temp-extract 2>&1')
    
    # Copy with unique names
    for orig_path, new_name in image_mapping.items():
        src = f'temp-extract/{orig_path}'
        if os.path.exists(src):
            dst = f'modules/ROOT/images/{new_name}'
            shutil.copy2(src, dst)
            print(f'Copied {orig_path} -> {new_name}')
    
    # Clean up
    shutil.rmtree('temp-extract', ignore_errors=True)

def update_references():
    """Update image references in AsciiDoc files based on context"""
    import glob
    
    # Based on the original markdown, map descriptions to unique filenames
    description_to_image = {
        "Suppose you were to find yourself in an informal conversation": "stock-image-intro-1.jpg",
        "So, the million-dollar question: Why is AI so important now?": "stock-image-intro-2.jpg",
        "There are many definitions of AI; scholars and computer scientists": "stock-image-intro-3.jpg",
        "UPS uses predictive AI to combat package theft": "stock-image-predictive-1.jpg",
        "According to the United Nations": "stock-image-predictive-2.jpg",
        "Through its mobile banking app": "stock-image-predictive-3.jpg",
        "At the Wimbledon Tennis Championships": "stock-image-predictive-4.jpg",
        "AI security and AI safety are related": "stock-image-security-1.jpg",
        "Every phase of the AI lifecycle": "stock-image-security-2.jpg",
    }
    
    for filepath in glob.glob('modules/ROOT/pages/*.adoc'):
        if 'index' in filepath:
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all stock-image.jpg references with their context
        pattern = r'image::stock-image\.jpg\[([^\]]+)\]'
        
        def replace_image(match):
            desc = match.group(1)
            # Find matching image based on description
            for key, img_name in description_to_image.items():
                if key.lower() in desc.lower():
                    return f'image::{img_name}[{desc}]'
            # Default fallback
            return f'image::stock-image-intro-1.jpg[{desc}]'
        
        new_content = re.sub(pattern, replace_image, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated references in {os.path.basename(filepath)}')

if __name__ == '__main__':
    extract_and_rename_images()
    update_references()
