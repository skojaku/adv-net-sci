#!/usr/bin/env python3
"""Test script for the enhanced fact-checking evaluation feature."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_quiz.dspy_core import DSPyQuizChallenge, QuizQuestion


def test_fact_checking():
    """Test the fact-checking feature with the Watts-Strogatz example."""
    
    # Test questions including the problematic Watts-Strogatz one
    test_questions = [
        QuizQuestion(
            question="The Watts-Strogatz model creates a small-world network only when the rewiring probability is greater than 0 but less than 1. True/False and describe the reason.",
            answer="False. The Watts-Strogatz model in fact creates small-world networks when the network size is small. This is because the path length can be short.",
            number=1
        ),
        QuizQuestion(
            question="What is the capital of France?",
            answer="London",  # Intentionally wrong
            number=2
        ),
        QuizQuestion(
            question="What is 2 + 2?",
            answer="4",  # Correct answer
            number=3
        )
    ]
    
    # Initialize the challenge system with fact-checking enabled
    print("Initializing DSPyQuizChallenge with fact-checking enabled...")
    
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key")
    
    challenge = DSPyQuizChallenge(
        base_url="https://api.openai.com/v1",
        api_key=api_key,
        quiz_model="gpt-4o-mini",
        evaluator_model="gpt-4o-mini",
        verify_student_answers=True  # Enable fact-checking
    )
    
    print("\nRunning quiz challenge with fact-checking:")
    print("=" * 60)
    
    # Run the quiz
    results = challenge.run_quiz_challenge(test_questions, "Fact-Checking Test")
    
    print("\nResults Summary:")
    print("-" * 60)
    
    for result in results.question_results:
        print(f"\nQuestion {result.question.number}: {result.question.question[:50]}...")
        print(f"  Student Answer: {result.question.answer[:50]}...")
        
        if hasattr(result, 'student_answer_correctness'):
            print(f"  Student Answer Correctness: {result.student_answer_correctness}")
            
            if result.student_answer_correctness != 'CORRECT':
                print(f"    ⚠️  Student's answer is factually incorrect!")
                if hasattr(result, 'factual_issues') and result.factual_issues:
                    print(f"    Issues: {', '.join(result.factual_issues)}")
        
        print(f"  LLM Answer Verdict: {'CORRECT' if not result.student_wins else 'INCORRECT'}")
        print(f"  Student Wins: {result.student_wins}")
        print(f"  Explanation: {result.evaluation_explanation[:100]}...")
    
    print("\n" + "=" * 60)
    print("Overall Results:")
    print(f"  Total Questions: {results.total_questions}")
    print(f"  Valid Questions: {results.valid_questions}")
    print(f"  Student Wins: {results.student_wins}")
    print(f"  LLM Wins: {results.llm_wins}")
    print(f"  Pass Status: {'PASS' if results.student_passes else 'FAIL'}")
    print(f"  Feedback: {results.feedback_summary}")
    
    # Test with fact-checking disabled for comparison
    print("\n\n" + "=" * 60)
    print("Running same quiz with fact-checking DISABLED for comparison:")
    print("=" * 60)
    
    challenge_no_check = DSPyQuizChallenge(
        base_url="https://api.openai.com/v1",
        api_key=api_key,
        quiz_model="gpt-4o-mini",
        evaluator_model="gpt-4o-mini",
        verify_student_answers=False  # Disable fact-checking
    )
    
    results_no_check = challenge_no_check.run_quiz_challenge(test_questions, "No Fact-Checking Test")
    
    print("\nComparison Results (No Fact-Checking):")
    print("-" * 60)
    for result in results_no_check.question_results:
        print(f"Question {result.question.number}: Student Wins = {result.student_wins}")
    
    print(f"\nTotal Student Wins (with fact-checking): {results.student_wins}")
    print(f"Total Student Wins (without fact-checking): {results_no_check.student_wins}")


if __name__ == "__main__":
    print("=" * 60)
    print("Fact-Checking Evaluation Feature Test")
    print("=" * 60)
    print("\nThis test demonstrates how the system now fact-checks student answers")
    print("to ensure they are correct before allowing the student to 'win'.\n")
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set in environment")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print("Or modify the script to use your preferred LLM endpoint\n")
    
    try:
        test_fact_checking()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()