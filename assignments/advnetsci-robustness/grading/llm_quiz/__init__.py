"""
LLM Quiz Challenge Library

A library for creating and evaluating quiz challenges where students try to stump AI models.
Simplified implementation using DSPy structured output.
"""

# Main interface using DSPy
from .dspy_core import DSPyQuizChallenge as LLMQuizChallenge
from .dspy_core import QuizQuestion, QuizResult, QuizResults

# DSPy signatures for advanced usage
from .dspy_signatures import (
    AnswerQuizQuestion,
    EvaluateAnswer,
    GenerateFeedback,
    ParseQuestionAndAnswer,
    ValidateQuestion,
    ValidationIssue,
)

__version__ = "3.0.0"
__all__ = [
    # Main interface
    "LLMQuizChallenge",
    # Core data structures
    "QuizQuestion",
    "QuizResult",
    "QuizResults",
    # DSPy signatures
    "ParseQuestionAndAnswer",
    "ValidateQuestion",
    "AnswerQuizQuestion",
    "EvaluateAnswer",
    "GenerateFeedback",
    "ValidationIssue",
]
