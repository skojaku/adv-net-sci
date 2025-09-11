"""
Entry point for running the LLM Quiz Challenge as a module.

Usage: python -m llm_quiz --quiz-file quiz.toml --api-key sk-xxx
"""

from .cli import main

if __name__ == "__main__":
    main()
