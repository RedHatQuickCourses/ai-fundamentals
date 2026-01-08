#!/usr/bin/env python3
"""
Fix HTML attributes that got broken across lines
"""
import re
import os
import glob

def fix_html_attributes(content):
    """Fix HTML data attributes that span multiple lines"""
    # Fix data attributes that have line breaks
    content = re.sub(
        r'data-incorrect-feedback="([^"]*?)\n\n',
        r'data-incorrect-feedback="\1"',
        content
    )
    content = re.sub(
        r'data-correct-feedback="([^"]*?)\n\n',
        r'data-correct-feedback="\1"',
        content
    )
    # Fix any remaining issues with quotes and line breaks in attributes
    content = re.sub(
        r'(data-[^=]+="[^"]*?)\n([^"]*?")',
        r'\1\2',
        content
    )
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
        
        content = fix_html_attributes(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed HTML attributes in {filename}")

if __name__ == '__main__':
    main()
