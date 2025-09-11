"""
Test script for DSPy implementation of LLM Quiz Challenge.

This script tests the basic functionality without requiring real API keys.
"""

import logging
import os
import sys
from pathlib import Path

# Import our modules
sys.path.insert(0, os.path.dirname(__file__))

from dspy_core import DSPyQuizChallenge, QuizQuestion
from dspy_signatures import (
    AnswerQuizQuestion,
    EvaluateAnswer,
    ParseQuestionAndAnswer,
    ValidateQuestion,
    ValidateQuestionSimilarity,
)

# Set up basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_signatures():
    """Test that DSPy signatures are properly defined."""
    logger.info("Testing DSPy signatures...")

    # Test ParseQuestionAndAnswer signature
    assert hasattr(ParseQuestionAndAnswer, "__annotations__")
    logger.info("✓ ParseQuestionAndAnswer signature defined")

    # Test ValidateQuestion signature
    assert hasattr(ValidateQuestion, "__annotations__")
    logger.info("✓ ValidateQuestion signature defined")

    # Test AnswerQuizQuestion signature
    assert hasattr(AnswerQuizQuestion, "__annotations__")
    logger.info("✓ AnswerQuizQuestion signature defined")

    # Test EvaluateAnswer signature
    assert hasattr(EvaluateAnswer, "__annotations__")
    logger.info("✓ EvaluateAnswer signature defined")

    # Test ValidateQuestionSimilarity signature
    assert hasattr(ValidateQuestionSimilarity, "__annotations__")
    logger.info("✓ ValidateQuestionSimilarity signature defined")


def test_quiz_loading():
    """Test quiz loading functionality."""
    logger.info("Testing quiz loading...")

    # This will fail without real API credentials, but we can test the initialization
    try:
        challenge = DSPyQuizChallenge(
            base_url="http://dummy.com",
            api_key="dummy_key",
            quiz_model="dummy_model",
            evaluator_model="dummy_evaluator",
        )
        logger.info("✓ DSPyQuizChallenge initialized (without real API)")
    except Exception as e:
        logger.info(f"ℹ DSPyQuizChallenge initialization failed as expected: {e}")

    # Test quiz file loading (this should work without API)
    test_quiz_file = Path("test_quiz.toml")
    if test_quiz_file.exists():
        try:
            # Create a minimal challenge instance to test file loading
            challenge = DSPyQuizChallenge(
                base_url="http://dummy.com",
                api_key="dummy_key",
                quiz_model="dummy_model",
                evaluator_model="dummy_evaluator",
            )
            questions = challenge.load_quiz_from_file(test_quiz_file)
            logger.info(f"✓ Loaded {len(questions)} questions from test quiz")

            for i, q in enumerate(questions, 1):
                logger.info(f"  Question {i}: {q.question}")
                logger.info(f"  Answer {i}: {q.answer}")
        except Exception as e:
            logger.error(f"✗ Failed to load quiz file: {e}")
    else:
        logger.warning("! Test quiz file not found")


def test_data_structures():
    """Test data structure functionality."""
    logger.info("Testing data structures...")

    # Test QuizQuestion creation
    question = QuizQuestion(question="What is 2 + 2?", answer="4", number=1)
    assert question.question == "What is 2 + 2?"
    assert question.answer == "4"
    assert question.number == 1
    logger.info("✓ QuizQuestion dataclass working")


def main():
    """Run all tests."""
    logger.info("Starting DSPy implementation tests...")
    logger.info("=" * 50)

    try:
        test_signatures()
        logger.info("")

        test_data_structures()
        logger.info("")

        test_quiz_loading()
        logger.info("")

        logger.info("=" * 50)
        logger.info("✓ All basic tests passed!")
        logger.info("")
        logger.info("Note: Full functionality requires valid API credentials.")
        logger.info("Use the CLI with valid credentials to test with real APIs.")

    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
