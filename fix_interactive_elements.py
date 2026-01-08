#!/usr/bin/env python3
"""
Fix interactive elements in AsciiDoc files - convert to HTML passthrough blocks
"""
import re
import os
import glob

def fix_knowledge_checks(content):
    """Convert knowledge check blocks to HTML passthrough"""
    # Pattern for knowledge check with options
    pattern = r'=== 🧠 Knowledge Check: (.+?)\s*\*Answer Options:\*\s*(.+?)\s*\*✅ Correct Feedback:\*\s*(.+?)\s*\*❌ Incorrect Feedback:\*\s*(.+?)(?=\n{3}|\n===|$)'
    
    def replace_kc(match):
        question = match.group(1).strip()
        options_text = match.group(2).strip()
        correct_fb = match.group(3).strip()
        incorrect_fb = match.group(4).strip()
        
        # Parse options (A, B, C, D format)
        options = re.findall(r'([A-D])\.\s*(.+?)(?=\n[A-D]\.|\*\*|$)', options_text, re.DOTALL)
        correct_letter = None
        options_html = []
        
        for letter, opt_text in options:
            opt_text = opt_text.strip()
            # Check if this is the correct answer
            if '✅' in opt_text or opt_text.endswith('✅'):
                correct_letter = letter
                opt_text = re.sub(r'✅\s*', '', opt_text).strip()
            options_html.append(f'        <label class="knowledge-check-option"><input type="radio" name="kc-{hash(question) % 10000}" value="{letter}" /> <span>{opt_text}</span></label>')
        
        # Escape quotes in feedback
        correct_fb = correct_fb.replace('"', '&quot;')
        incorrect_fb = incorrect_fb.replace('"', '&quot;')
        question_escaped = question.replace('"', '&quot;')
        
        html = f'''[.knowledge-check]
[source,html]
----
<div class="knowledge-check" data-question="{question_escaped}" data-correct="{correct_letter}" data-correct-feedback="{correct_fb}" data-incorrect-feedback="{incorrect_fb}">
  <div class="knowledge-check-question">
    <strong>{question}</strong>
  </div>
  <div class="knowledge-check-options">
{chr(10).join(options_html)}
  </div>
  <button class="knowledge-check-submit">Check Answer</button>
  <div class="knowledge-check-feedback" style="display: none;"></div>
</div>
----
'''
        return html
    
    content = re.sub(pattern, replace_kc, content, flags=re.DOTALL)
    return content

def fix_interactive_placeholders(content):
    """Fix interactive element placeholders"""
    # Interactive Process
    content = re.sub(
        r'\[\.interactive-process\]\s*\n====\s*\n_Interactive content will be rendered here_\s*\n====',
        '[.interactive-process]\n====\n_Interactive process content_\n====',
        content
    )
    
    # Sorting Activity
    content = re.sub(
        r'\[\.sorting-activity\]\s*\n====\s*\n(.+?)\s*\n====',
        r'[.sorting-activity]\n====\n\1\n====',
        content,
        flags=re.DOTALL
    )
    
    # Flashcards
    content = re.sub(
        r'\[\.flashcards\]\s*\n====\s*\n(.+?)\s*\n====',
        r'[.flashcards]\n====\n\1\n====',
        content,
        flags=re.DOTALL
    )
    
    # Accordion
    content = re.sub(
        r'\[\.interactive-accordion\]\s*\n====\s*\n_Accordion content will be rendered here_\s*\n====',
        '[.interactive-accordion]\n====\n_Accordion content_\n====',
        content
    )
    
    return content

def fix_media_blocks(content):
    """Fix media content blocks"""
    content = re.sub(
        r'\[\.media-content\]\s*\n====\s*\n_Media content_\s*\n====',
        '[.media-content]\n====\n_Media content (video/audio)_\n====',
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
        
        # Apply fixes
        content = fix_knowledge_checks(content)
        content = fix_interactive_placeholders(content)
        content = fix_media_blocks(content)
        
        # Clean up extra blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed interactive elements in {filename}")

if __name__ == '__main__':
    main()
