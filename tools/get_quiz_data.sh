#!/bin/bash

# This script clones all student repos from GitHub Classroom and retrieves
# the quiz questions (quiz.toml) and results (quiz_results.json) from each repo.
# It also checks GitHub Actions status for quiz grading.

# Usage: ./get_quiz_data.sh [ASSIGNMENT_ID] [CLONE_DIR] [OUTPUT_FILE] [CSV_FILE]
# Example: ./get_quiz_data.sh 834116 student-repos quiz_results.txt quiz_summary.csv

# Configuration - all can be overridden via command line arguments
ASSIGNMENT_ID=$1  # Default assignment ID
CLONE_DIR=$2  # Directory to clone repos into
OUTPUT_FILE="${3:-quiz_and_results.txt}"  # Detailed output file
CSV_FILE="${4:-quiz_summary.csv}"  # CSV summary file

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Install it with: brew install jq"
    exit 1
fi

# Step 1: Clone all student repositories using gh classroom (only if not already cloned)
if [ -d "$CLONE_DIR" ] && [ "$(ls -A $CLONE_DIR 2>/dev/null)" ]; then
    echo "Directory '$CLONE_DIR' already exists and contains repositories. Skipping clone."
    echo "To re-clone, delete the directory first: rm -rf $CLONE_DIR"
else
    echo "Cloning student repositories for assignment $ASSIGNMENT_ID into $CLONE_DIR..."
    gh classroom clone student-repos -a "$ASSIGNMENT_ID" -d "$CLONE_DIR"

    # Check if clone was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to clone student repositories"
        exit 1
    fi
fi

# Step 2: Clear the output files if they exist
> "$OUTPUT_FILE"

echo "Processing student repositories..."

# Step 3: Find all student repository directories and extract quiz data
# GitHub Classroom creates a nested structure: CLONE_DIR/assignment-name/student-repos
# We need to find the actual repos in the nested structure
for submissions_dir in "$CLONE_DIR"/*; do
    if [ -d "$submissions_dir" ]; then
        for repo_dir in "$submissions_dir"/*; do
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

            # Write detailed output to text file
            {
                echo "================================================================================"
                echo "Repository: $repo_name"
                echo "================================================================================"
                echo ""
                echo "SUMMARY"
                echo "-------"
                echo "  GitHub Actions:      $gh_actions_status ($gh_actions_conclusion)"
                echo "  Student Success Rate: $student_success_rate"
                echo "  Valid Questions:      $valid_questions"
                echo "  Invalid Questions:    $invalid_questions"
                echo "  Student Wins:         $student_wins"
                echo "  LLM Wins:             $llm_wins"
                echo "  Student Passes:       $student_passes"
                echo "  GitHub Result:        $github_result"
                echo ""
                echo ""

                # Parse and display each question with details
                question_count=$(jq '.question_results | length' "$results_file")
                for i in $(seq 0 $(($question_count - 1))); do
                    echo "--------------------------------------------------------------------------------"
                    echo "QUESTION $(($i + 1))"
                    echo "--------------------------------------------------------------------------------"
                    echo ""

                    question=$(jq -r ".question_results[$i].question" "$results_file")
                    correct_answer=$(jq -r ".question_results[$i].correct_answer" "$results_file")
                    llm_answer=$(jq -r ".question_results[$i].llm_answer" "$results_file")
                    is_correct=$(jq -r ".question_results[$i].is_correct" "$results_file")
                    student_wins_q=$(jq -r ".question_results[$i].student_wins" "$results_file")
                    valid=$(jq -r ".question_results[$i].validation.valid // false" "$results_file")
                    issues=$(jq -r ".question_results[$i].validation.issues // [] | join(\", \")" "$results_file")
                    explanation=$(jq -r ".question_results[$i].evaluation_explanation" "$results_file")

                    echo "Question:"
                    echo "  $question"
                    echo ""
                    echo "Student's Correct Answer:"
                    echo "  $correct_answer"
                    echo ""
                    echo "LLM's Answer:"
                    echo "  $llm_answer"
                    echo ""
                    echo "Result:"
                    echo "  Is Correct:    $is_correct"
                    echo "  Student Wins:  $student_wins_q"
                    echo "  Valid:         $valid"
                    if [ "$issues" != "" ]; then
                        echo "  Issues:        $issues"
                    fi
                    echo ""
                    echo "AI Evaluation:"
                    echo "  $explanation"
                    echo ""
                done

                echo "================================================================================"
                echo ""
                echo ""
            } >> "$OUTPUT_FILE"
                else
                    echo "  Warning: Quiz results file not found in $repo_name"
                fi
            fi
        done
    fi
done

echo ""
echo "Done! Results saved to: $OUTPUT_FILE"
