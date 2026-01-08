#!/usr/bin/env python3
"""
Clean up and fix AsciiDoc files after conversion
"""
import re
import os
import glob

def fix_image_blocks(content):
    """Fix image blocks that weren't properly converted"""
    # Pattern 1: Image with Description
    pattern1 = r'=== 🖼️ Image: Image Content\s*\*Description:\*\s*(.+?)\s*\*📁 File Information:\*\s*-\s*\*Filename:\*\s*(.+?)\s*-\s*\*Location:\*\s*scormcontent/assets/(.+?)\s*(?=\n\n|\n===|$)'
    
    def replace_img1(match):
        desc = match.group(1).strip()
        filename = match.group(2).strip()
        location = match.group(3).strip()
        img_name = os.path.basename(location) if '/' in location else filename
        return f'image::{img_name}[{desc}]\n'
    
    content = re.sub(pattern1, replace_img1, content, flags=re.DOTALL)
    
    # Pattern 2: Image with Alt Text
    pattern2 = r'=== 🖼️ Image: Image Content\s*\*Alt Text:\*\s*(.+?)\s*\*📁 File Information:\*\s*-\s*\*Filename:\*\s*(.+?)\s*-\s*\*Location:\*\s*scormcontent/assets/(.+?)\s*(?=\n\n|\n===|$)'
    
    def replace_img2(match):
        alt = match.group(1).strip()
        filename = match.group(2).strip()
        location = match.group(3).strip()
        img_name = os.path.basename(location) if '/' in location else filename
        # Clean up alt text - remove newlines
        alt = ' '.join(alt.split())
        return f'image::{img_name}[{alt}]\n'
    
    content = re.sub(pattern2, replace_img2, content, flags=re.DOTALL)
    
    # Remove any remaining image metadata blocks
    content = re.sub(r'=== 🖼️ Image: Image Content.*?\*Access:.*?\n', '', content, flags=re.DOTALL)
    
    return content

def fix_special_chars(content):
    """Fix remaining special character issues"""
    # Fix it' to it's
    content = re.sub(r"it'\s+expected", "it's expected", content)
    content = re.sub(r"it'\s+", "it's ", content)
    # Fix That' to That's
    content = re.sub(r"That'\s+", "That's ", content)
    # Fix URLs
    content = re.sub(r'https://www\.thomsonreuterscom/', 'https://www.thomsonreuters.com/', content)
    content = re.sub(r'https://www\.gartner\.com/en/newsroom/pressreleases2025-09-17-gartner-saysworldwide-ai-spending-will-total-1-point-5-trillion-in-2025', 'https://www.gartner.com/en/newsroom/press-releases/2025-09-17-gartner-says-worldwide-ai-spending-will-total-1-point-5-trillion-in-2025', content)
    content = re.sub(r'https://info\.idc\.com/futurescape-generative-ai-2025-predictionshtml', 'https://info.idc.com/futurescape-generative-ai-2025-predictions.html', content)
    # Fix percentage signs that might be missing
    content = re.sub(r'(\d+)\s+of organizations', r'\1% of organizations', content)
    return content

def fix_duplicate_headers(content):
    """Remove duplicate section headers"""
    # Remove duplicate "Why should you care about AI?" headers
    lines = content.split('\n')
    result = []
    prev_line = None
    for line in lines:
        if line == prev_line and line.startswith('==='):
            continue  # Skip duplicate
        result.append(line)
        prev_line = line
    return '\n'.join(result)

def fix_media_blocks(content):
    """Fix media content blocks"""
    # Replace media blocks with placeholders
    content = re.sub(r'### 📱 Media: Media Content.*?\n', '[.media-content]\n====\n_Media content_\n====\n\n', content, flags=re.DOTALL)
    return content

def main():
    pages_dir = 'modules/ROOT/pages'
    adoc_files = glob.glob(f'{pages_dir}/*.adoc')
    
    # Skip index and fix filename
    for filepath in adoc_files:
        filename = os.path.basename(filepath)
        if filename == 'index.adoc':
            continue
        
        # Fix the security filename
        if filename.startswith('ai-security-and-using-ai-responsibly'):
            new_path = os.path.join(pages_dir, 'ai-security-responsibility.adoc')
            if os.path.exists(filepath):
                os.rename(filepath, new_path)
                filepath = new_path
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        content = fix_image_blocks(content)
        content = fix_special_chars(content)
        content = fix_duplicate_headers(content)
        content = fix_media_blocks(content)
        
        # Clean up extra blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {filename}")

if __name__ == '__main__':
    main()
