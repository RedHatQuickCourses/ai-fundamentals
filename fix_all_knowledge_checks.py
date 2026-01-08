#!/usr/bin/env python3
"""
Fix all knowledge check blocks to use passthrough (++++ instead of [source,html])
"""
import re
import os
import glob

def fix_knowledge_checks(content):
    """Convert [source,html] blocks to passthrough blocks for knowledge checks"""
    # Pattern: [.knowledge-check] followed by [source,html] block with HTML content
    pattern = r'\[\.knowledge-check\]\s*\[source,html\]\s*----\s*(<div class="knowledge-check".*?</div>)\s*----'
    
    def replace_kc(match):
        html_content = match.group(1)
        # Use passthrough block (++++ instead of [source,html]----)
        return f'[.knowledge-check]\n++++\n{html_content}\n++++'
    
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
        content = fix_knowledge_checks(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed knowledge checks in {filename}")
        else:
            print(f"No changes needed in {filename}")

if __name__ == '__main__':
    main()
