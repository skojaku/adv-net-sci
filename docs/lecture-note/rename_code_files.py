#!/usr/bin/env python3
"""
Rename .md files with code blocks to .qmd extension and update _quarto.yml
"""

import os
import re

def has_code_blocks(filepath):
    """Check if file has Python code blocks."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return '```{python}' in content
    except:
        return False

def rename_files_with_code():
    """Rename .md files with code blocks to .qmd extension."""
    renamed_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'_build', 'tmp', '_book', '.quarto'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if has_code_blocks(filepath):
                    new_filepath = filepath[:-3] + '.qmd'
                    os.rename(filepath, new_filepath)
                    # Store relative path for updating config
                    rel_old = os.path.relpath(filepath, '.')
                    rel_new = os.path.relpath(new_filepath, '.')
                    renamed_files.append((rel_old, rel_new))
                    print(f"Renamed: {rel_old} -> {rel_new}")
    
    return renamed_files

def update_quarto_config(renamed_files):
    """Update _quarto.yml to reflect renamed files."""
    config_path = '_quarto.yml'
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace .md with .qmd for renamed files
        for old_path, new_path in renamed_files:
            if old_path in content:
                content = content.replace(old_path, new_path)
                print(f"Updated config: {old_path} -> {new_path}")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Updated _quarto.yml configuration")
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")

if __name__ == '__main__':
    print("🔄 Renaming files with code blocks to .qmd extension...")
    renamed_files = rename_files_with_code()
    
    if renamed_files:
        print(f"\n📝 Updating _quarto.yml configuration...")
        update_quarto_config(renamed_files)
        print(f"\n✅ Successfully renamed {len(renamed_files)} files")
    else:
        print("\n✅ No files needed renaming")