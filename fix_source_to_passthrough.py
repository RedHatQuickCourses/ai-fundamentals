#!/usr/bin/env python3
"""
Convert [source,html] blocks to passthrough blocks (++++ for knowledge checks
"""
import re
import os
import glob

def fix_source_blocks(content):
    """Convert [source,html] blocks to passthrough blocks for knowledge checks"""
    # Pattern: [.knowledge-check] followed by [source,html]----...----
    pattern = r'(\[\.knowledge-check\])\s*\[source,html\]\s*----\s*(<div class="knowledge-check".*?</div>)\s*----'
    
    def replace_kc(match):
        role = match.group(1)
        html_content = match.group(2)
        # Use passthrough block (++++ instead of [source,html]----)
        return f'{role}\n++++\n{html_content}\n++++'
    
    content = re.sub(pattern, replace_kc, content, flags=re.DOTALL)
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
        content = fix_source_blocks(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed source blocks in {filename}")
        else:
            print(f"No changes needed in {filename}")

if __name__ == '__main__':
    main()
