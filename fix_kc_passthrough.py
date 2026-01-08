#!/usr/bin/env python3
"""
Fix knowledge checks: replace [source,html] blocks with passthrough blocks
"""
import re
import os
import glob

def fix_knowledge_checks(content):
    """Replace [source,html]----...---- with passthrough blocks"""
    # Find all [.knowledge-check] blocks followed by [source,html]
    lines = content.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is a knowledge-check block start
        if line.strip() == '[.knowledge-check]' and i + 1 < len(lines):
            result.append(line)
            i += 1
            # Check if next line is [source,html]
            if i < len(lines) and lines[i].strip() == '[source,html]':
                # Skip [source,html] and replace with passthrough start
                result.append('++++')
                i += 1
                # Skip the ---- line
                if i < len(lines) and lines[i].strip() == '----':
                    i += 1
                # Collect HTML content until we find closing ----
                html_lines = []
                while i < len(lines) and lines[i].strip() != '----':
                    html_lines.append(lines[i])
                    i += 1
                # Add HTML content
                result.extend(html_lines)
                # Skip closing ---- and add closing passthrough
                if i < len(lines) and lines[i].strip() == '----':
                    i += 1
                result.append('++++')
            else:
                result.append(lines[i])
                i += 1
        else:
            result.append(line)
            i += 1
    
    return '\n'.join(result)

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
        content = fix_knowledge_checks(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed knowledge checks in {filename}")
        else:
            print(f"No changes needed in {filename}")

if __name__ == '__main__':
    main()
