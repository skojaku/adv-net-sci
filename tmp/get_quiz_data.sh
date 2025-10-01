#!/bin/bash

# This script retrieves the quiz questions (quiz.toml) and results (quiz_results.json)
# from all student submissions.

# The directory containing the student submissions
SUBMISSIONS_DIR="m02-small-world-submissions"

# The output file
OUTPUT_FILE="quiz_and_results.txt"

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Find all student repository directories
for repo_dir in "$SUBMISSIONS_DIR"/*; do
    if [ -d "$repo_dir" ]; then
        repo_name=$(basename "$repo_dir")
        quiz_file="$repo_dir/assignment/quiz.toml"
        results_file="$repo_dir/assignment/quiz_results.json"

        if [ -f "$quiz_file" ] && [ -f "$results_file" ]; then
            echo "================================================================"
            echo "=== Repository: $repo_name"
            echo "================================================================"
            echo ""

            echo "----------------------------------------------------------------"
            echo "--- Quiz Questions (quiz.toml)"
            echo "----------------------------------------------------------------"
            cat "$quiz_file"
            echo ""

            echo "----------------------------------------------------------------"
            echo "--- Quiz Results (quiz_results.json)"
            echo "----------------------------------------------------------------"
            cat "$results_file"
            echo -e "\n\n"
        fi
    fi
done

echo "Quiz questions and results have been concatenated into $OUTPUT_FILE"
