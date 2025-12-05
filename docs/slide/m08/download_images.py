#!/usr/bin/env python3
"""
Script to extract image URLs from markdown files and download them to a figs folder.
"""

import re
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path


def extract_image_urls(markdown_file):
    """
    Extract image URLs from a markdown file.
    Supports both markdown syntax ![](url) and HTML <img src="url">

    Args:
        markdown_file: Path to the markdown file

    Returns:
        List of image URLs found in the file
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    urls = []

    # Pattern for markdown syntax: ![alt text](url)
    markdown_pattern = r'!\[.*?\]\((https?://[^\)]+)\)'
    urls.extend(re.findall(markdown_pattern, content))

    # Pattern for HTML img tags: <img src="url">
    html_pattern = r'<img[^>]+src=["\'](https?://[^"\']+)["\']'
    urls.extend(re.findall(html_pattern, content))

    # Pattern for Quarto syntax with attributes: ![](url){attributes}
    quarto_pattern = r'!\[[^\]]*\]\((https?://[^\)]+)\)\{[^\}]*\}'
    urls.extend(re.findall(quarto_pattern, content))

    return urls


def download_image(url, output_dir):
    """
    Download an image from a URL to the output directory.

    Args:
        url: URL of the image to download
        output_dir: Directory to save the image

    Returns:
        Path to the downloaded file or None if download failed
    """
    try:
        # Parse the URL to get the filename
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename, create one from the URL hash
        if not filename or '.' not in filename:
            filename = f"image_{hash(url) % 100000}.jpg"

        output_path = os.path.join(output_dir, filename)

        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"  ⏭️  Skipping (already exists): {filename}")
            return output_path

        # Download the image
        print(f"  📥 Downloading: {filename}")
        urllib.request.urlretrieve(url, output_path)
        print(f"  ✅ Saved: {output_path}")
        return output_path

    except Exception as e:
        print(f"  ❌ Failed to download {url}: {str(e)}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python download_images.py <markdown_file> [output_dir]")
        print("\nExample:")
        print("  python download_images.py slide.qmd")
        print("  python download_images.py slide.qmd ./my_figs")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "figs"

    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Error: File '{markdown_file}' not found")
        sys.exit(1)

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir}\n")

    # Extract image URLs
    print(f"🔍 Scanning {markdown_file}...")
    urls = extract_image_urls(markdown_file)

    if not urls:
        print("No image URLs found in the markdown file")
        return

    print(f"Found {len(urls)} image URL(s)\n")

    # Download images
    successful = 0
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        if download_image(url, output_dir):
            successful += 1
        print()

    print(f"✨ Complete: {successful}/{len(urls)} images downloaded to '{output_dir}'")


if __name__ == "__main__":
    main()
