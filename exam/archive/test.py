import csv
from typing import List, Dict

class QuizQuestion:
    def __init__(self, title: str, question_text: str, options: List[Dict[str, str]], 
                 points: int = 1, difficulty: int = 1, course_code: str = "COURSE101",
                 question_number: int = 1, image: str = None, hint: str = None, 
                 feedback: str = None):
        self.title = title
        self.question_text = question_text
        self.options = options  # List of dicts with 'text', 'points', and optional 'feedback'
        self.points = points
        self.difficulty = difficulty
        self.course_code = course_code
        self.question_number = question_number
        self.image = image
        self.hint = hint
        self.feedback = feedback

    def to_rows(self) -> List[List[str]]:
        """Convert question to CSV rows format"""
        rows = []
        
        # Start new question
        rows.append(["NewQuestion", "MC", "", "", ""])
        
        # Add ID
        rows.append(["ID", f"{self.course_code}-{self.question_number}", "", "", ""])
        
        # Add basic information
        rows.append(["Title", self.title, "", "", ""])
        rows.append(["QuestionText", self.question_text, "", "", ""])
        rows.append(["Points", str(self.points), "", "", ""])
        rows.append(["Difficulty", str(self.difficulty), "", "", ""])
        
        # Add image if present
        if self.image:
            rows.append(["Image", self.image, "", "", ""])
        
        # Add options
        for option in self.options:
            feedback = option.get('feedback', '')
            rows.append(["Option", str(option['points']), option['text'], "", feedback])
        
        # Add hint if present
        if self.hint:
            rows.append(["Hint", self.hint, "", "", ""])
        
        # Add feedback if present
        if self.feedback:
            rows.append(["Feedback", self.feedback, "", "", ""])
        
        # Add empty row for separation
        rows.append(["", "", "", "", ""])
        
        return rows

def generate_quiz_csv(questions: List[QuizQuestion], output_file: str):
    """Generate CSV file from list of questions"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header comment
        writer.writerow(['// Brightspace Quiz - Multiple Choice Questions'])
        writer.writerow(['// Please ensure this file is saved as CSV UTF-8 encoded'])
        writer.writerow([''])
        
        # Write each question
        for question in questions:
            rows = question.to_rows()
            writer.writerows(rows)

# Example usage
def main():
    # Example questions
    questions = [
        QuizQuestion(
            title="Basic Math Question",
            question_text="What is 2 + 2?",
            options=[
                {"points": 100, "text": "4", "feedback": "Correct!"},
                {"points": 0, "text": "3", "feedback": "Not quite."},
                {"points": 0, "text": "5", "feedback": "Try again."},
                {"points": 0, "text": "6", "feedback": "Incorrect."}
            ],
            course_code="MATH101",
            question_number=1,
            difficulty=1,
            hint="Think about basic addition",
            feedback="This tests your understanding of basic addition."
        ),
        QuizQuestion(
            title="Science Question",
            question_text="What is the chemical symbol for water?",
            options=[
                {"points": 100, "text": "H2O", "feedback": "Correct!"},
                {"points": 0, "text": "CO2", "feedback": "That's carbon dioxide."},
                {"points": 0, "text": "O2", "feedback": "That's oxygen."}
            ],
            course_code="CHEM101",
            question_number=1,
            difficulty=2
        )
    ]
    
    generate_quiz_csv(questions, "brightspace_quiz.csv")

if __name__ == "__main__":
    main()
