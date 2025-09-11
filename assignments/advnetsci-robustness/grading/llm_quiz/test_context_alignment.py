#!/usr/bin/env python3
"""Test script for the enhanced context alignment feature."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_quiz.dspy_core import DSPyQuizChallenge, QuizQuestion


def test_context_alignment():
    """Test the context alignment checker with different scenarios."""
    
    # Sample context about Euler paths
    context_content = """
    # Graph Theory: Euler Paths and Circuits
    
    An Euler path is a path in a graph that visits every edge exactly once. 
    An Euler circuit is an Euler path that starts and ends at the same vertex.
    
    Key conditions for Euler paths:
    - A connected graph has an Euler path if and only if it has exactly 0 or 2 vertices of odd degree
    - A connected graph has an Euler circuit if and only if every vertex has even degree
    
    The degree of a vertex is the number of edges connected to it.
    Self-loops count as 2 towards the degree of a vertex.
    """
    
    # Test questions with different alignment levels
    test_cases = [
        {
            "question": "What is the condition for a graph to have an Euler circuit?",
            "answer": "All vertices must have even degree",
            "expected_alignment": "DIRECT",
            "description": "Direct question about content"
        },
        {
            "question": "If a vertex has a self-loop and 3 other edges, what is its degree?",
            "answer": "The degree is 5 (self-loop counts as 2, plus 3 other edges)",
            "expected_alignment": "EXTENSION",
            "description": "Extension - applies degree counting rules to specific case"
        },
        {
            "question": "How does spectral clustering partition a graph into communities?",
            "answer": "Spectral clustering uses eigenvalues and eigenvectors of the graph Laplacian",
            "expected_alignment": "UNRELATED",
            "description": "Unrelated - completely different graph theory topic"
        },
        {
            "question": "What is the time complexity of finding an Euler path using Hierholzer's algorithm?",
            "answer": "O(E) where E is the number of edges",
            "expected_alignment": "TANGENTIAL",
            "description": "Tangential - about Euler paths but focuses on algorithm complexity not covered"
        }
    ]
    
    # Initialize the challenge system
    print("Initializing DSPyQuizChallenge...")
    
    # You'll need to set these environment variables or pass them directly
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key")
    
    challenge = DSPyQuizChallenge(
        base_url="https://api.openai.com/v1",
        api_key=api_key,
        quiz_model="gpt-4o-mini",
        evaluator_model="gpt-4o-mini",
        context_content=context_content,
        context_strictness="normal"  # Test with normal strictness
    )
    
    print("\nTesting context alignment checker:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        question = QuizQuestion(
            question=test_case["question"],
            answer=test_case["answer"],
            number=i
        )
        
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Question: {test_case['question']}")
        print(f"Expected alignment: {test_case['expected_alignment']}")
        
        # Check alignment
        alignment_result = challenge._check_context_alignment(question)
        
        if alignment_result:
            print(f"Actual alignment: {alignment_result['alignment_type']}")
            print(f"Should flag mismatch: {alignment_result['should_flag_mismatch']}")
            print(f"Should flag weak: {alignment_result['should_flag_weak_alignment']}")
            print(f"Reasoning: {alignment_result['reasoning'][:200]}...")
            
            # Check if result matches expectation
            if alignment_result['alignment_type'] == test_case['expected_alignment']:
                print("✅ PASS: Alignment matches expected")
            else:
                print(f"⚠️  WARN: Expected {test_case['expected_alignment']}, got {alignment_result['alignment_type']}")
        else:
            print("❌ ERROR: No alignment result returned")
        
        print("-" * 60)
    
    print("\n\nTesting different strictness levels:")
    print("=" * 60)
    
    # Test with EXTENSION question under different strictness
    extension_question = QuizQuestion(
        question="If a vertex has a self-loop and 3 other edges, what is its degree?",
        answer="The degree is 5",
        number=1
    )
    
    for strictness in ["strict", "normal", "lenient"]:
        challenge.context_strictness = strictness
        alignment = challenge._check_context_alignment(extension_question)
        
        if alignment:
            print(f"\nStrictness: {strictness}")
            print(f"  Alignment type: {alignment['alignment_type']}")
            print(f"  Flags mismatch: {alignment['should_flag_mismatch']}")
            print(f"  Flags weak: {alignment['should_flag_weak_alignment']}")


if __name__ == "__main__":
    print("=" * 60)
    print("Context Alignment Feature Test")
    print("=" * 60)
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set in environment")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print("Or modify the script to use your preferred LLM endpoint\n")
    
    try:
        test_context_alignment()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()