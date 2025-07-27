import re
import json

def parse_quiz(text):
    # Split text into individual questions
    questions = re.split(r'\n---\n', text)
    quiz_data = []
    
    for question in questions:
        if not question.strip():
            continue
            
        question_dict = {}
        
        # Extract question text
        q_match = re.search(r'(.*?)\n\nA\)', question, re.DOTALL)
        if q_match:
            question_dict['question'] = q_match.group(1).strip()
        
        # Extract options
        options = {}
        option_matches = re.findall(r'([A-D]\)) (.*?)(?=\n[A-D]\)|\n<correct|$)', question, re.DOTALL)
        for opt_letter, opt_text in option_matches:
            options[opt_letter[0]] = opt_text.strip()
        question_dict['options'] = options
        
        # Extract correct answer
        correct_match = re.search(r'<correct_answer>(.*?)</correct_answer>', question)
        if correct_match:
            question_dict['correct_answer'] = correct_match.group(1).strip()
            
        if question_dict.get('question') and question_dict.get('options'):
            quiz_data.append(question_dict)
    
    return quiz_data

def main():
    # Read input from file
    with open('quiz_input.txt', 'r') as f:
        text = f.read()
    
    # Parse the quiz
    quiz_data = parse_quiz(text)
    
    # Write to JSON file
    with open('quiz_output.json', 'w') as f:
        json.dump(quiz_data, f, indent=2)
        
    print(f"Successfully processed {len(quiz_data)} questions into quiz_output.json")

if __name__ == "__main__":
    main()
