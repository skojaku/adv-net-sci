#!/usr/bin/env python3
"""Convert Quarto Markdown files to Marimo notebooks via Jupyter notebooks."""

import argparse
import subprocess
import sys
import re
import tempfile
from pathlib import Path

# Optional YAML import - fallback to regex parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def run_command(cmd, cwd=None):
    """Run shell command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running: {cmd}")
            print(f"stderr: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running {cmd}: {e}")
        return False


def check_dependencies():
    """Check if required tools are installed."""
    dependencies = ['quarto', 'jupyter', 'marimo']
    missing = []

    for tool in dependencies:
        if not run_command(f"{tool} --version"):
            missing.append(tool)

    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("\nInstall with:")
        for tool in missing:
            if tool == 'quarto':
                print("  - Quarto: https://quarto.org/docs/get-started/")
            elif tool == 'jupyter':
                print("  - Jupyter: pip install jupyter")
            elif tool == 'marimo':
                print("  - Marimo: pip install marimo")
        return False
    return True


def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter and return title, remaining content."""
    lines = content.split('\n')
    if not lines[0].strip() == '---':
        return None, content

    yaml_lines = []
    content_start = None

    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            content_start = i + 1
            break
        yaml_lines.append(line)

    if content_start is None:
        return None, content

    title = None
    remaining_content = '\n'.join(lines[content_start:])

    if HAS_YAML:
        try:
            yaml_data = yaml.safe_load('\n'.join(yaml_lines))
            title = yaml_data.get('title', '') if yaml_data else ''
        except yaml.YAMLError:
            title = None
    else:
        # Fallback: simple string parsing for title
        for line in yaml_lines:
            if line.strip().startswith('title:'):
                # Extract title after 'title:'
                title_part = line.split('title:', 1)[1].strip()
                # Remove quotes if present
                title = title_part.strip('"\'')
                break

    return title, remaining_content


def convert_callouts(content):
    """Convert Quarto callouts to Marimo format."""
    lines = content.split('\n')
    result = []
    in_callout = False
    callout_title = None
    expecting_title = False

    # Map Quarto callout types to Marimo admonition types
    callout_type_map = {
        'note': 'admonition',
        'info': 'admonition',
        'tip': 'admonition',
        'warning': 'attention',
        'important': 'attention',
        'caution': 'attention',
        'danger': 'attention',
        'error': 'attention',
        'success': 'admonition'
    }

    # Pattern for callouts with optional collapse and title
    callout_pattern = re.compile(r'^:::\s*\{\.callout-([^}]+)(?:\s+collapse="[^"]*")?\}\s*(.*?)$')

    for line in lines:
        # Handle callout start
        match = callout_pattern.match(line)
        if match:
            callout_type = match.group(1).lower()
            inline_title = match.group(2).strip()

            # Map to Marimo admonition type
            marimo_type = callout_type_map.get(callout_type, 'admonition')

            if inline_title:
                # Title provided inline
                result.append(f"/// {marimo_type} | {inline_title}")
                in_callout = True
                expecting_title = False
            else:
                # No inline title, check if next line has ## Title
                callout_title = callout_type.replace('-', ' ').title()  # fallback
                result.append(f"/// {marimo_type} | {callout_title}")
                in_callout = True
                expecting_title = True
            continue

        # Handle ## Title immediately after callout start
        if expecting_title and line.strip().startswith('## '):
            # Replace the previous line with the proper title
            actual_title = line.strip()[3:].strip()  # Remove ## and whitespace
            result[-1] = result[-1].rsplit('|', 1)[0] + f"| {actual_title}"
            expecting_title = False
            continue
        elif expecting_title:
            # No title found, keep the default
            expecting_title = False

        # Handle callout end
        if line.strip() == ':::' and in_callout:
            result.append("///")
            in_callout = False
            continue

        # Remove column margins and other div blocks
        if re.match(r'^:::\s*\{[^}]*\}', line):
            continue

        # Remove standalone ::: that aren't callouts
        if line.strip() == ':::' and not in_callout:
            continue

        # Convert #| comments to regular comments
        if line.startswith('#|'):
            result.append(f"# {line[2:].strip()}")
            continue

        result.append(line)

    return '\n'.join(result)


def clean_quarto_content(content):
    """Clean Quarto content for better Jupyter conversion."""
    # Extract title and remove frontmatter
    title, content_without_yaml = extract_yaml_frontmatter(content)

    # Convert callouts and clean other syntax
    cleaned_content = convert_callouts(content_without_yaml)

    # Add title as first heading if present
    if title:
        cleaned_content = f"# {title}\n\n{cleaned_content}"

    return cleaned_content


def convert_quarto_to_jupyter(qmd_path, output_dir=None):
    """Convert Quarto markdown to Jupyter notebook."""
    qmd_path = Path(qmd_path)
    if not qmd_path.exists():
        print(f"❌ File not found: {qmd_path}")
        return None

    # Read and clean the Quarto file
    with open(qmd_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = clean_quarto_content(content)

    # Create temporary cleaned file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.qmd', delete=False, encoding='utf-8') as tmp:
        tmp.write(cleaned_content)
        tmp_path = Path(tmp.name)

    try:
        # Determine output path
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            ipynb_path = output_dir / f"{qmd_path.stem}.ipynb"
        else:
            ipynb_path = qmd_path.parent / f"{qmd_path.stem}.ipynb"

        # Convert using quarto
        cmd = f"quarto convert {tmp_path} --output {ipynb_path}"
        print(f"⚠️  Step 1: Converting Quarto to Jupyter...")
        print(f"Running: {cmd}")

        if run_command(cmd):
            print(f"✅ Created Jupyter notebook: {ipynb_path}")
            return ipynb_path
        else:
            print(f"❌ Failed to convert {qmd_path} to Jupyter")
            return None

    finally:
        # Clean up temporary file
        tmp_path.unlink()


def convert_jupyter_to_marimo(ipynb_path, output_dir=None):
    """Convert Jupyter notebook to Marimo notebook."""
    ipynb_path = Path(ipynb_path)
    if not ipynb_path.exists():
        print(f"❌ Jupyter notebook not found: {ipynb_path}")
        return None

    # Determine output path
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        marimo_path = output_dir / f"{ipynb_path.stem}.py"
    else:
        marimo_path = ipynb_path.parent / f"{ipynb_path.stem}.py"

    # Convert using marimo
    cmd = f"marimo convert {ipynb_path}"
    print(f"⚠️  Step 2: Converting Jupyter to Marimo...")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            # Add script metadata configuration at the top
            script_metadata = '''# /// script
# [tool.marimo.display]
# default_width = "full"
# [tool.marimo.formatting]
# line_length = 120
# ///

'''
            marimo_content = script_metadata + result.stdout

            with open(marimo_path, 'w', encoding='utf-8') as f:
                f.write(marimo_content)
            print(f"✅ Created Marimo notebook: {marimo_path}")
            return marimo_path
        else:
            print(f"❌ Failed to convert {ipynb_path} to Marimo")
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Exception during Marimo conversion: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Convert Quarto Markdown files to Marimo notebooks via Jupyter notebooks"
    )
    parser.add_argument(
        "input_file",
        help="Input Quarto markdown file (.qmd)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory (default: same as input file)"
    )
    parser.add_argument(
        "--keep-jupyter",
        action="store_true",
        help="Keep intermediate Jupyter notebook file"
    )

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)

    if input_path.suffix != '.qmd':
        print(f"❌ Input file must be a Quarto markdown file (.qmd)")
        sys.exit(1)

    print(f"Converting: {input_path}")
    if args.output_dir:
        print(f"Output directory: {args.output_dir}")
    print()

    # Step 1: Convert Quarto to Jupyter
    jupyter_path = convert_quarto_to_jupyter(input_path, args.output_dir)
    if not jupyter_path:
        sys.exit(1)

    # Step 2: Convert Jupyter to Marimo
    marimo_path = convert_jupyter_to_marimo(jupyter_path, args.output_dir)
    if not marimo_path:
        sys.exit(1)

    # Clean up intermediate Jupyter file if not keeping
    if not args.keep_jupyter:
        jupyter_path.unlink()
        print(f"⚠️  Removed intermediate Jupyter file")
    else:
        print(f"⚠️  Kept intermediate Jupyter file: {jupyter_path}")

    print()
    print("✅ Conversion complete!")
    print(f"✅ Marimo notebook: {marimo_path}")

    # Offer to open in marimo
    try:
        response = input("Open in Marimo editor? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            subprocess.run(f"marimo edit {marimo_path}", shell=True)
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()