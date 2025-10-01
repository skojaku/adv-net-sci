#!/bin/bash

# This script concatenates all quiz.toml files from student submissions
# into a single file for review.

# The directory containing the student submissions
SUBMISSIONS_DIR="m02-small-world-submissions"

# The output file
OUTPUT_FILE="all_quizzes.toml"

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Find all quiz.toml files and process them
find "$SUBMISSIONS_DIR" -type f -path "*/assignment/quiz.toml" | while read -r quiz_file; do
    # Get the repository name from the file path
    repo_dir=$(dirname "$(dirname "$quiz_file")")
    repo_name=$(basename "$repo_dir")

    # Append a header and the file content to the output file
    echo "################################################################" >> "$OUTPUT_FILE"
    echo "### Quiz from repository: $repo_name" >> "$OUTPUT_FILE"
    echo "################################################################" >> "$OUTPUT_FILE"
    cat "$quiz_file" >> "$OUTPUT_FILE"
    echo -e "

" >> "$OUTPUT_FILE"
done

echo "All quiz.toml files have been concatenated into $OUTPUT_FILE"
