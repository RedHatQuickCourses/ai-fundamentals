#!/usr/bin/env python3
"""
Convert markdown course content to AsciiDoc format
"""
import re
import os

def fix_special_chars(text):
    """Fix special character issues from markdown export"""
    # Fix 'ss to apostrophe
    text = text.replace("'ss", "'")
    text = text.replace("'sst", "'t")
    text = text.replace("don'sst", "don't")
    text = text.replace("it'sss", "it's")
    text = text.replace("it'ss", "it's")
    text = text.replace("you'ssve", "you've")
    text = text.replace("you'ss", "you're")
    text = text.replace("won'sst", "won't")
    text = text.replace("isn'sst", "isn't")
    text = text.replace("aren'sst", "aren't")
    text = text.replace("doesn'sst", "doesn't")
    text = text.replace("let'sss", "let's")
    text = text.replace("let'ss", "let's")
    # Fix URLs
    text = re.sub(r'https//', 'https://', text)
    text = re.sub(r'http//', 'http://', text)
    # Fix percentage signs
    text = re.sub(r'(\d+)\s+of', r'\1% of', text)
    text = re.sub(r'(\d+)\s+believe', r'\1% believe', text)
    return text

def convert_image_block(text):
    """Convert image blocks to AsciiDoc image syntax"""
    # Pattern: ### 🖼️ Image: Image Content followed by description and file info
    pattern = r'### 🖼️ Image: Image Content\s*\*\*Description:\*\* (.*?)\s*\*\*📁 File Information:\*\*\s*-\s*\*\*Filename:\*\* (.*?)\s*-\s*\*\*Location:\*\* (.*?)\s*'
    
    def replace_image(match):
        desc = match.group(1).strip()
        filename = match.group(2).strip()
        location = match.group(3).strip()
        # Extract just the filename from location if needed
        img_name = os.path.basename(location) if '/' in location else filename
        # Remove scormcontent/assets/ prefix
        img_name = img_name.replace('scormcontent/assets/', '')
        return f'image::{img_name}[{desc}]'
    
    text = re.sub(pattern, replace_image, text, flags=re.DOTALL)
    
    # Also handle Alt Text pattern
    alt_pattern = r'### 🖼️ Image: Image Content\s*\*\*Alt Text:\*\* (.*?)\s*\*\*📁 File Information:\*\*\s*-\s*\*\*Filename:\*\* (.*?)\s*-\s*\*\*Location:\*\* (.*?)\s*'
    
    def replace_alt_image(match):
        alt = match.group(1).strip()
        filename = match.group(2).strip()
        location = match.group(3).strip()
        img_name = os.path.basename(location) if '/' in location else filename
        img_name = img_name.replace('scormcontent/assets/', '')
        return f'image::{img_name}[{alt}]'
    
    text = re.sub(alt_pattern, replace_alt_image, text, flags=re.DOTALL)
    return text

def convert_headers(text):
    """Convert markdown headers to AsciiDoc"""
    text = re.sub(r'^# (.+)$', r'= \1', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'== \1', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'=== \1', text, flags=re.MULTILINE)
    return text

def convert_lists(text):
    """Convert markdown lists to AsciiDoc"""
    # Bullet points
    text = re.sub(r'^• (.+)$', r'* \1', text, flags=re.MULTILINE)
    return text

def convert_knowledge_check(text):
    """Convert knowledge check blocks to placeholder for interactive component"""
    # Pattern for knowledge checks
    pattern = r'### 🧠 Knowledge Check: (.+?)\s*\*\*Answer Options:\*\*\s*(.+?)\s*\*\*✅ Correct Feedback:\*\* (.+?)\s*\*\*❌ Incorrect Feedback:\*\* (.+?)(?=\n---|\n###|$)'
    
    def replace_kc(match):
        question = match.group(1).strip()
        options = match.group(2).strip()
        correct_fb = match.group(3).strip()
        incorrect_fb = match.group(4).strip()
        
        # Parse options (A, B, C, D format)
        options_list = re.findall(r'([A-D])\.\s*(.+?)(?=\n[A-D]\.|\*\*|$)', options, re.DOTALL)
        correct_letter = None
        options_text = []
        for letter, opt_text in options_list:
            opt_text = opt_text.strip()
            if '✅' in opt_text:
                correct_letter = letter
                opt_text = opt_text.replace('✅', '').strip()
            options_text.append((letter, opt_text))
        
        # Create HTML block for knowledge check component
        options_html = '\n'.join([f'        <option value="{letter}">{opt}</option>' 
                                 for letter, opt in options_text])
        
        return f'''[.knowledge-check]
====
{question}

[source,html]
----
<knowledge-check question="{question}" correct="{correct_letter}" correct-feedback="{correct_fb}" incorrect-feedback="{incorrect_fb}">
{options_html}
</knowledge-check>
----
===='''
    
    text = re.sub(pattern, replace_kc, text, flags=re.DOTALL)
    return text

def convert_interactive_elements(text):
    """Convert interactive elements to placeholders"""
    # Interactive Process
    text = re.sub(r'### 📋 Interactive Process', '[.interactive-process]\n====\n_Interactive content will be rendered here_\n====', text)
    # Sorting Activity
    text = re.sub(r'### 🗂️ Sorting Activity: (.+?)', r'[.sorting-activity]\n====\n\1\n====', text, flags=re.DOTALL)
    # Flashcards
    text = re.sub(r'### 🃏 Flashcards: (.+?)', r'[.flashcards]\n====\n\1\n====', text, flags=re.DOTALL)
    # Interactive Accordion
    text = re.sub(r'### Interactive Accordion', '[.interactive-accordion]\n====\n_Accordion content will be rendered here_\n====', text)
    return text

def convert_hr(text):
    """Convert horizontal rules"""
    text = re.sub(r'^---$', "'''", text, flags=re.MULTILINE)
    return text

def convert_bold(text):
    """Convert bold text"""
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
    return text

def main():
    input_file = 'ai-fundamentals-content.md'
    output_dir = 'modules/ROOT/pages'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply conversions
    content = fix_special_chars(content)
    content = convert_headers(content)
    content = convert_image_block(content)
    content = convert_lists(content)
    content = convert_bold(content)
    content = convert_hr(content)
    content = convert_knowledge_check(content)
    content = convert_interactive_elements(content)
    
    # Split into lessons
    lessons = re.split(r'^== (.+)$', content, flags=re.MULTILINE)
    
    # First part is title and intro
    title_section = lessons[0] if lessons else ""
    
    # Process each lesson (every other item starting from index 1)
    lesson_files = {}
    for i in range(1, len(lessons), 2):
        if i + 1 < len(lessons):
            lesson_title = lessons[i]
            lesson_content = lessons[i + 1]
            
            # Clean up lesson title for filename
            filename = lesson_title.lower().replace(' ', '-').replace(':', '').replace('📊', '')
            filename = re.sub(r'[^\w-]', '', filename)
            if filename == 'course-analysis':
                continue  # Skip analysis section
            
            lesson_files[filename] = {
                'title': lesson_title,
                'content': lesson_content
            }
    
    # Create index page
    index_content = """= AI Fundamentals
:navtitle: Home

== Introduction

Course Title: AI Fundamentals

Description:
This course introduces artificial intelligence (AI) and explains why you should care about it. You'll learn about the AI market opportunity, different types of AI (predictive, generative, and agentic), inferencing and optimization, and how to use AI responsibly.

Duration: Approximately 1 hour

== Objectives

On completing this course, you should be able to:

* Explain, at a high level, the AI market opportunity
* Define artificial intelligence, machine learning, and deep learning
* Distinguish between predictive AI and generative AI
* Understand the importance of inferencing and optimization in AI
* Describe agentic AI and its use cases
* Identify AI security concerns and best practices for responsible AI use

== Prerequisites

This course assumes that you have:

* Basic computer literacy
* An interest in learning about artificial intelligence
* No prior technical knowledge of AI required

== Course Structure

The course is organized into the following lessons:

* xref:introduction.adoc[Introduction]
* xref:predictive-generative-ai.adoc[Predictive AI and Generative AI]
* xref:inferencing-optimization.adoc[Inferencing and Optimization]
* xref:agentic-ai.adoc[Agentic AI]
* xref:ai-security-responsibility.adoc[AI Security and Using AI Responsibly]
"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/index.adoc', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # Write lesson files
    filename_map = {
        'introduction': 'introduction',
        'predictive-ai-and-generative-ai': 'predictive-generative-ai',
        'inferencing-and-optimization': 'inferencing-optimization',
        'agentic-ai': 'agentic-ai',
        'ai-security-and-using-ai-responsibly': 'ai-security-responsibility'
    }
    
    for orig_name, data in lesson_files.items():
        filename = filename_map.get(orig_name, orig_name)
        full_content = f"= {data['title']}\n:navtitle: {data['title']}\n\n{data['content']}"
        
        with open(f'{output_dir}/{filename}.adoc', 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"Created {filename}.adoc")

if __name__ == '__main__':
    main()
