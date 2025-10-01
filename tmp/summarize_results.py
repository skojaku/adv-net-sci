import json
import glob
import os
import argparse

def summarize_quiz_results(submissions_dir):
    """
    Parses all quiz_results.json files in a given submissions directory 
    and prints a summary of the results.
    """
    output_lines = []
    search_pattern = os.path.join(submissions_dir, "*/assignment/quiz_results.json")
    output_file = f"{os.path.basename(submissions_dir)}_summary.txt"

    for results_file in sorted(glob.glob(search_pattern)):
        repo_dir = os.path.dirname(os.path.dirname(results_file))
        repo_name = os.path.basename(repo_dir)

        with open(results_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                output_lines.append(f"================================================================")
                output_lines.append(f"=== Repository: {repo_name}")
                output_lines.append(f"================================================================")
                output_lines.append("Error: Could not decode JSON.")
                output_lines.append("\n\n")
                continue

        output_lines.append(f"================================================================")
        output_lines.append(f"=== Repository: {repo_name}")
        output_lines.append(f"Overall Result: {data.get('github_classroom_result', 'N/A')}")
        output_lines.append(f"================================================================")

        for qr in data.get('question_results', []):
            question_info = qr.get('question', {})
            output_lines.append(f"----------------------------------------------------------------")
            output_lines.append(f"Question {question_info.get('number', 'N/A')}: {question_info.get('question', 'N/A')}")
            output_lines.append(f"Student's Answer: {question_info.get('answer', 'N/A')}")
            output_lines.append(f"LLM's Answer: {qr.get('llm_answer', 'N/A')}")
            output_lines.append(f"Student Won: {qr.get('student_wins', 'N/A')}")
        
        output_lines.append("\n\n")

    with open(output_file, "w") as f:
        f.write("\n".join(output_lines))

    print(f"Generated {output_file} with the summarized results.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Summarize quiz results for a given assignment.")
    parser.add_argument("submissions_dir", help="The directory containing the student submissions.")
    args = parser.parse_args()
    summarize_quiz_results(args.submissions_dir)