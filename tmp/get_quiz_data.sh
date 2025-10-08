#!/bin/bash

# This script clones all student repos from GitHub Classroom and retrieves
# the quiz questions (quiz.toml) and results (quiz_results.json) from each repo.

# Configuration
ASSIGNMENT_ID="${1:-834116}"  # Default assignment ID, can be overridden
CLONE_DIR="student-repos"
OUTPUT_FILE="quiz_and_results.txt"

# Step 1: Clone all student repositories using gh classroom
echo "Cloning student repositories for assignment $ASSIGNMENT_ID..."
gh classroom clone student-repos -a "$ASSIGNMENT_ID"

# Check if clone was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone student repositories"
    exit 1
fi

# Step 2: Clear the output file if it exists
> "$OUTPUT_FILE"

echo "Processing student repositories..."

# Step 3: Find all student repository directories and extract quiz data
for repo_dir in "$CLONE_DIR"/*; do
    if [ -d "$repo_dir" ]; then
        repo_name=$(basename "$repo_dir")
        echo "Processing: $repo_name"

        quiz_file="$repo_dir/assignment/quiz.toml"
        results_file="$repo_dir/assignment/quiz_results.json"

        if [ -f "$quiz_file" ] && [ -f "$results_file" ]; then
            {
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
            } >> "$OUTPUT_FILE"
        else
            echo "  Warning: Quiz files not found in $repo_name"
        fi
    fi
done

echo "Done! Quiz questions and results have been saved to $OUTPUT_FILE"
