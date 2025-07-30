#!/bin/bash

# Quarto to Marimo converter script
# Usage: ./convert_quarto_to_marimo.sh input.qmd [output_dir] [--keep-jupyter]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() { echo -e "${RED}✗ $1${NC}" >&2; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    if ! command_exists quarto; then
        missing+=("quarto")
    fi
    
    if ! command_exists jupyter; then
        missing+=("jupyter")
    fi
    
    if ! command_exists marimo; then
        missing+=("marimo")
    fi
    
    if [ ${#missing[@]} -gt 0 ]; then
        print_error "Missing dependencies: ${missing[*]}"
        echo ""
        echo "Install with:"
        for dep in "${missing[@]}"; do
            case $dep in
                quarto)
                    echo "  - Quarto: https://quarto.org/docs/get-started/"
                    ;;
                jupyter)
                    echo "  - Jupyter: pip install jupyter"
                    ;;
                marimo)
                    echo "  - Marimo: pip install marimo"
                    ;;
            esac
        done
        return 1
    fi
    return 0
}

# Function to clean Quarto file for better Jupyter conversion
clean_quarto_file() {
    local input_file="$1"
    local temp_file="$2"
    
    # Use sed to clean Quarto-specific syntax
    sed -E '
        # Convert #| comments to regular comments
        s/^#\|/# /
        
        # Remove or comment problematic Quarto directives
        /^:::/s/^/<!-- /
        /^:::$/s/$/-->/
    ' "$input_file" > "$temp_file"
}

# Main conversion function
convert_quarto_to_marimo() {
    local input_file="$1"
    local output_dir="$2"
    local keep_jupyter="$3"
    
    # Validate input
    if [[ ! -f "$input_file" ]]; then
        print_error "Input file not found: $input_file"
        return 1
    fi
    
    if [[ "$input_file" != *.qmd ]]; then
        print_error "Input file must be a Quarto markdown file (.qmd)"
        return 1
    fi
    
    # Get base name without extension
    local basename=$(basename "$input_file" .qmd)
    local input_dir=$(dirname "$input_file")
    
    # Set output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="$input_dir"
    else
        mkdir -p "$output_dir"
    fi
    
    # Create temporary cleaned file
    local temp_qmd=$(mktemp -t "quarto_clean_XXXXXX").qmd
    clean_quarto_file "$input_file" "$temp_qmd"
    
    # Define output paths
    local jupyter_file="$output_dir/${basename}.ipynb"
    local marimo_file="$output_dir/${basename}.py"
    
    echo "Converting: $input_file"
    echo "Output directory: $output_dir"
    echo ""
    
    # Step 1: Convert Quarto to Jupyter
    print_warning "Step 1: Converting Quarto to Jupyter..."
    echo "Running: quarto convert $temp_qmd --output $jupyter_file"
    if quarto convert "$temp_qmd" --output "$jupyter_file"; then
        print_success "Created Jupyter notebook: $jupyter_file"
    else
        print_error "Failed to convert Quarto to Jupyter"
        rm -f "$temp_qmd"
        return 1
    fi
    
    # Clean up temporary file
    rm -f "$temp_qmd"
    
    # Step 2: Convert Jupyter to Marimo
    print_warning "Step 2: Converting Jupyter to Marimo..."
    if marimo convert "$jupyter_file" > "$marimo_file"; then
        print_success "Created Marimo notebook: $marimo_file"
    else
        print_error "Failed to convert Jupyter to Marimo"
        return 1
    fi
    
    # Clean up intermediate Jupyter file if not keeping
    if [[ "$keep_jupyter" != "true" ]]; then
        rm -f "$jupyter_file"
        print_warning "Removed intermediate Jupyter file"
    else
        print_warning "Kept intermediate Jupyter file: $jupyter_file"
    fi
    
    echo ""
    print_success "Conversion complete!"
    print_success "Marimo notebook: $marimo_file"
    
    # Offer to open in marimo
    read -p "Open in Marimo editor? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        marimo edit "$marimo_file"
    fi
}

# Show usage
show_usage() {
    echo "Usage: $0 <input.qmd> [output_dir] [--keep-jupyter]"
    echo ""
    echo "Arguments:"
    echo "  input.qmd      Input Quarto markdown file"
    echo "  output_dir     Output directory (optional, defaults to input file directory)"
    echo "  --keep-jupyter Keep intermediate Jupyter notebook file"
    echo ""
    echo "Examples:"
    echo "  $0 my_notebook.qmd"
    echo "  $0 my_notebook.qmd ./output/"
    echo "  $0 my_notebook.qmd ./output/ --keep-jupyter"
}

# Parse arguments
if [[ $# -lt 1 ]]; then
    show_usage
    exit 1
fi

input_file="$1"
output_dir="$2"
keep_jupyter="false"

# Check for --keep-jupyter flag
for arg in "$@"; do
    if [[ "$arg" == "--keep-jupyter" ]]; then
        keep_jupyter="true"
        break
    fi
done

# Check dependencies
if ! check_dependencies; then
    exit 1
fi

# Run conversion
convert_quarto_to_marimo "$input_file" "$output_dir" "$keep_jupyter"
