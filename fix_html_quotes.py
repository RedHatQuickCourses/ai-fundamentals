#!/usr/bin/env python3
"""
Fix HTML attribute quote issues in knowledge checks
"""
import re
import os
import glob

def fix_html_quotes(content):
    """Fix double quotes at end of data attributes"""
    # Fix pattern like: data-incorrect-feedback="..."">
    content = re.sub(r'(data-[^=]+="[^"]*?)"">', r'\1">', content)
    # Fix pattern like: data-incorrect-feedback="..."">
    content = re.sub(r'(data-[^=]+="[^"]*?)"\'\'\'', r'\1"', content)
    return content

def main():
    pages_dir = 'modules/ROOT/pages'
    adoc_files = glob.glob(f'{pages_dir}/*.adoc')
    
    for filepath in adoc_files:
        filename = os.path.basename(filepath)
        if filename == 'index.adoc':
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_html_quotes(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed HTML quotes in {filename}")
        else:
            print(f"No changes needed in {filename}")

if __name__ == '__main__':
    main()
