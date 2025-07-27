import json

def update_quiz_ids(input_file: str, output_file: str):
    """
    Read quiz questions from JSON file, update IDs to be consecutive,
    and save to a new JSON file
    """
    # Read the existing quiz file
    with open(input_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # Sort questions by current ID to maintain relative order
    questions.sort(key=lambda x: x['id'])
    
    # Update IDs to be consecutive
    for i, question in enumerate(questions, 1):
        question['id'] = i
    
    # Write the updated questions to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=3)
    
    print(f"Updated {len(questions)} questions with consecutive IDs")
    print(f"New file saved as: {output_file}")

if __name__ == "__main__":
    input_file = "quiz.json"
    output_file = "quiz_updated.json"
    update_quiz_ids(input_file, output_file)
