# Quiz Data Collection Tool

This tool clones student repositories from GitHub Classroom and extracts quiz questions, results, and AI evaluations into a formatted text report.

## Prerequisites

- **gh CLI** - GitHub CLI tool ([installation guide](https://cli.github.com/))
- **jq** - JSON processor
  ```bash
  brew install jq
  ```
- **gh classroom extension** - GitHub Classroom CLI extension
  ```bash
  gh extension install github/gh-classroom
  ```

## Usage

```bash
./get_quiz_data.sh [ASSIGNMENT_ID] [CLONE_DIR] [OUTPUT_FILE]
```

### Parameters

1. **ASSIGNMENT_ID** (optional, default: `834116`)
   - The GitHub Classroom assignment ID
   - Find this in your GitHub Classroom assignment URL

2. **CLONE_DIR** (optional, default: `student-repos`)
   - Directory where student repositories will be cloned
   - If directory already exists, cloning is skipped

3. **OUTPUT_FILE** (optional, default: `quiz_and_results.txt`)
   - Path to the output text file

### Examples

**Use all defaults:**
```bash
./get_quiz_data.sh
```

**Specify assignment ID:**
```bash
./get_quiz_data.sh 999999
```

**Use existing cloned repositories:**
```bash
./get_quiz_data.sh 834116 m03-network-robustness-submissions
```

**Specify all parameters:**
```bash
./get_quiz_data.sh 999999 my-repos my_output.txt
```

## Output Format

The tool generates a formatted text file with:

### Per Student Repository:
- **Summary section:**
  - GitHub Actions status and conclusion
  - Student success rate
  - Valid/invalid question counts
  - Student wins vs LLM wins
  - Pass/fail status
  - GitHub Classroom result

- **Detailed question breakdown:**
  - Question text
  - Student's correct answer
  - LLM's answer attempt
  - Validation status and issues
  - AI evaluation explanation

### Example Output:

```
================================================================================
Repository: m03-network-robustness-student1
================================================================================

SUMMARY
-------
  GitHub Actions:       completed (success)
  Student Success Rate: 0.75
  Valid Questions:      3
  Invalid Questions:    1
  Student Wins:         3
  LLM Wins:             1
  Student Passes:       true
  GitHub Result:        STUDENTS_QUIZ_KEIKO_WIN


--------------------------------------------------------------------------------
QUESTION 1
--------------------------------------------------------------------------------

Question:
  What is the main difference between random and targeted attacks on networks?

Student's Correct Answer:
  Random attacks remove nodes uniformly at random, while targeted attacks
  remove high-degree nodes first, which is more effective at fragmenting
  scale-free networks.

LLM's Answer:
  Random attacks affect nodes randomly while targeted attacks focus on
  specific vulnerable nodes.

Result:
  Is Correct:    false
  Student Wins:  true
  Valid:         true

AI Evaluation:
  The student's answer is more comprehensive and specifically mentions
  scale-free networks and high-degree nodes, which is the key concept.
  The LLM's answer is too generic.

...
```

## Notes

- If the clone directory already exists and contains files, the script will skip cloning and process existing repositories
- To force re-cloning, delete the clone directory first: `rm -rf student-repos`
- The script checks GitHub Actions status for the `quiz.yml` workflow in each repository
- Missing quiz files in a repository will generate a warning but won't stop processing
