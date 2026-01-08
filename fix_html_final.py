#!/usr/bin/env python3
"""
Final fix for HTML issues in AsciiDoc files
"""
import re
import os
import glob

def fix_html_issues(content):
    """Fix remaining HTML issues"""
    # Remove stray ''' in data attributes
    content = re.sub(r'(".*?)\'\'\'(")', r'\1\2', content)
    # Fix any remaining quote issues
    content = re.sub(r'data-incorrect-feedback="([^"]*?)"\'\'\'', r'data-incorrect-feedback="\1"', content)
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
        
        content = fix_html_issues(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed HTML in {filename}")

if __name__ == '__main__':
    main()
