#!/bin/bash

# This script clones all student repos from GitHub Classroom and retrieves
# the quiz questions (quiz.toml) and results (quiz_results.json) from each repo.
# It also checks GitHub Actions status for quiz grading.

# Usage: ./get_quiz_data.sh [ASSIGNMENT_ID] [CLONE_DIR] [OUTPUT_FILE] [CSV_FILE]
# Example: ./get_quiz_data.sh 834116 student-repos quiz_results.txt quiz_summary.csv

# Configuration - all can be overridden via command line arguments
ASSIGNMENT_ID="${1:-834116}"  # Default assignment ID
CLONE_DIR="${2:-student-repos}"  # Directory to clone repos into
OUTPUT_FILE="${3:-quiz_and_results.txt}"  # Detailed output file
CSV_FILE="${4:-quiz_summary.csv}"  # CSV summary file

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Install it with: brew install jq"
    exit 1
fi

# Step 1: Clone all student repositories using gh classroom
echo "Cloning student repositories for assignment $ASSIGNMENT_ID..."
gh classroom clone student-repos -a "$ASSIGNMENT_ID"

# Check if clone was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone student repositories"
    exit 1
fi

# Step 2: Clear the output files if they exist
> "$OUTPUT_FILE"
> "$CSV_FILE"

# Write CSV header
echo "Repository,Student_Success_Rate,Valid_Questions,Invalid_Questions,Student_Wins,LLM_Wins,Passes,GitHub_Result,Actions_Status,Actions_Conclusion" >> "$CSV_FILE"

echo "Processing student repositories..."

# Step 3: Find all student repository directories and extract quiz data
for repo_dir in "$CLONE_DIR"/*; do
    if [ -d "$repo_dir" ]; then
        repo_name=$(basename "$repo_dir")
        echo "Processing: $repo_name"

        quiz_file="$repo_dir/assignment/quiz.toml"
        results_file="$repo_dir/assignment/quiz_results.json"

        if [ -f "$results_file" ]; then
            # Parse JSON and extract key fields
            student_success_rate=$(jq -r '.student_success_rate // "N/A"' "$results_file")
            valid_questions=$(jq -r '.valid_questions // 0' "$results_file")
            invalid_questions=$(jq -r '.invalid_questions // 0' "$results_file")
            student_wins=$(jq -r '.student_wins // 0' "$results_file")
            llm_wins=$(jq -r '.llm_wins // 0' "$results_file")
            student_passes=$(jq -r '.student_passes // false' "$results_file")
            github_result=$(jq -r '.github_classroom_result // "N/A"' "$results_file")

            # Get GitHub Actions status for quiz workflow
            cd "$repo_dir"
            gh_actions_status=$(gh run list --workflow=quiz.yml --limit 1 --json status,conclusion --jq '.[0].status // "N/A"' 2>/dev/null || echo "N/A")
            gh_actions_conclusion=$(gh run list --workflow=quiz.yml --limit 1 --json status,conclusion --jq '.[0].conclusion // "N/A"' 2>/dev/null || echo "N/A")
            cd - > /dev/null

            # Write to CSV
            echo "$repo_name,$student_success_rate,$valid_questions,$invalid_questions,$student_wins,$llm_wins,$student_passes,$github_result,$gh_actions_status,$gh_actions_conclusion" >> "$CSV_FILE"

            # Write detailed output to text file
            {
                echo "================================================================"
                echo "=== Repository: $repo_name"
                echo "================================================================"
                echo ""
                echo "GitHub Actions Status: $gh_actions_status ($gh_actions_conclusion)"
                echo ""
                echo "--- Summary ---"
                echo "Student Success Rate: $student_success_rate"
                echo "Valid Questions: $valid_questions"
                echo "Invalid Questions: $invalid_questions"
                echo "Student Wins: $student_wins"
                echo "LLM Wins: $llm_wins"
                echo "Student Passes: $student_passes"
                echo "GitHub Result: $github_result"
                echo ""

                if [ -f "$quiz_file" ]; then
                    echo "----------------------------------------------------------------"
                    echo "--- Quiz Questions (quiz.toml)"
                    echo "----------------------------------------------------------------"
                    cat "$quiz_file"
                    echo ""
                fi

                echo "----------------------------------------------------------------"
                echo "--- Question Results (Parsed from quiz_results.json)"
                echo "----------------------------------------------------------------"
                jq -r '.question_results[] | "Question \(.question_number): \(.question)\nCorrect Answer: \(.correct_answer)\nLLM Answer: \(.llm_answer)\nStudent Wins: \(.student_wins)\nIs Correct: \(.is_correct)\nValidation: \(.validation.valid // false) (Issues: \(.validation.issues // [] | join(", ")))\nExplanation: \(.evaluation_explanation)\n"' "$results_file"

                echo -e "\n\n"
            } >> "$OUTPUT_FILE"
        else
            echo "  Warning: Quiz results file not found in $repo_name"
            echo "$repo_name,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A" >> "$CSV_FILE"
        fi
    fi
done

echo ""
echo "Done! Results saved to:"
echo "  - Detailed output: $OUTPUT_FILE"
echo "  - CSV summary: $CSV_FILE"
