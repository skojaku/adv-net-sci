#!/usr/bin/env python3
"""
Convert MyST Markdown files to Quarto-compatible format.

This script:
1. Removes Jupytext frontmatter that confuses Quarto
2. Converts MyST directives to Quarto equivalents
3. Updates citations and cross-references
"""

import os
import re
import glob

def convert_file(filepath):
    """Convert a single MyST file to Quarto format."""
    print(f"Converting {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove Jupytext frontmatter
    # Pattern: ---\njupytext:...\n---
    jupytext_pattern = r'^---\s*\njupytext:.*?\n---\s*\n'
    content = re.sub(jupytext_pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Remove kernelspec frontmatter
    # Pattern: ---\nkernelspec:...\n---
    kernelspec_pattern = r'^---\s*\nkernelspec:.*?\n---\s*\n'
    content = re.sub(kernelspec_pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Convert MyST admonitions to Quarto callouts
    # {admonition} Problem -> ::: {.callout-note title="Problem"}
    content = re.sub(
        r'```\{admonition\}\s+([^\n]+)\n(.*?)\n```',
        r'::: {.callout-note title="\1"}\n\2\n:::',
        content,
        flags=re.DOTALL
    )
    
    # Convert remaining MyST admonitions with ::: syntax
    content = re.sub(
        r':::\{admonition\}\s+([^\n]+)\n(.*?)\n:::',
        r'::: {.callout-note title="\1"}\n\2\n:::',
        content,
        flags=re.DOTALL
    )
    
    # Convert MyST figure directives to Quarto figures
    # :::{figure-md} label -> ![](image){#fig-label}
    figure_pattern = r':::\{figure-md\}\s+([^\n]+)\n!\[([^\]]*)\]\(([^)]+)\)\n\n([^\n]+)\n:::'
    content = re.sub(
        figure_pattern,
        r'![\2](\3){#fig-\1 fig-alt="\4"}\n\n: \4 {#fig-\1}',
        content
    )
    
    # Convert remaining figure directives with img tags
    img_figure_pattern = r':::\{figure-md\}\s+([^\n]+)\n<img src="([^"]+)"[^>]*>\n\n([^\n]+)\n:::'
    content = re.sub(
        img_figure_pattern,
        r'![](\2){#fig-\1 fig-alt="\3"}\n\n: \3 {#fig-\1}',
        content
    )
    
    # Convert MyST bibliography directive
    content = re.sub(
        r'```\{bibliography\}\s*\n:style: unsrt\s*\n:filter: docname in docnames\s*\n```',
        '## References\n\n::: {#refs}\n:::',
        content
    )
    
    # Convert MyST footbibliography directive
    content = re.sub(
        r'```\{footbibliography\}.*?\n```',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Convert remaining MyST figure directives
    content = re.sub(
        r'```\{figure-md\}.*?\n```',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Convert citations from {cite:p}`ref` to [@ref]
    content = re.sub(r'\{cite:p\}`([^`]+)`', r'[@\1]', content)
    content = re.sub(r'\{cite\}`([^`]+)`', r'[@\1]', content)
    
    # Convert cross-references from {numref}`ref` to @fig-ref or @tbl-ref
    content = re.sub(r'\{numref\}`([^`]+)`', r'@fig-\1', content)
    
    # Convert MyST code-cell directives to Quarto code blocks
    content = re.sub(
        r'```\{code-cell\}\s+(python|ipython3?)\n(.*?)\n```',
        r'```{python}\n\2\n```',
        content,
        flags=re.DOTALL
    )
    
    # Convert MyST note directives to Quarto callouts
    content = re.sub(
        r'```\{note\}\s*\n:name:\s*([^\n]+)\n(.*?)\n```',
        r'::: {.callout-note}\n\2\n:::',
        content,
        flags=re.DOTALL
    )
    
    # Convert remaining MyST note directives
    content = re.sub(
        r':::\{note\}\s*\n(.*?)\n:::',
        r'::: {.callout-note}\n\1\n:::',
        content,
        flags=re.DOTALL
    )
    
    # Convert MyST important directives to Quarto callouts
    content = re.sub(
        r':::\{important\}\s*\n(.*?)\n:::',
        r'::: {.callout-important}\n\1\n:::',
        content,
        flags=re.DOTALL
    )
    
    # Convert MyST tip directives to Quarto callouts  
    content = re.sub(
        r':::\{tip\}\s*\n(.*?)\n:::',
        r'::: {.callout-tip}\n\1\n:::',
        content,
        flags=re.DOTALL
    )
    
    # Save the converted content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Converted {filepath}")

def main():
    """Convert all markdown files in the lecture-note directory."""
    
    # Find all .md files recursively, excluding certain directories
    exclude_dirs = {'_build', 'tmp', '_book', '.quarto'}
    
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                convert_file(filepath)
    
    print("\n✅ Conversion complete!")
    print("\nNext steps:")
    print("1. Review converted files for any issues")
    print("2. Test rendering with: quarto render")
    print("3. Add more chapters to _quarto.yml as needed")

if __name__ == '__main__':
    main()