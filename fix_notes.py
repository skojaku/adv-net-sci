
import os
import re

def convert_notes(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.qmd', '.md')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # This regex finds ```{note} blocks and captures the content inside.
                    # It assumes the block starts with ```{note} on a new line and ends with ``` on a new line.
                    new_content = re.sub(r'^```{note}((?:.|
)*?)^```', r'::: {.callout-note}\1:::', content, flags=re.MULTILINE)

                    if new_content != content:
                        print(f"Updating {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Error processing file {filepath}: {e}")

convert_notes('/Users/skojaku-admin/Documents/projects/adv-net-sci/docs/lecture-note/m07-random-walks')
