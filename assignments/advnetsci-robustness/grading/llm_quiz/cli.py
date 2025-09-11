"""
Command Line Interface for LLM Quiz Challenge.

This module provides the CLI for running quiz challenges where students
try to stump AI models.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib  # Python 3.11+ built-in TOML parser
except ImportError:
    import tomli as tomllib  # Fallback for Python < 3.11

import colorama
from colorama import Back, Fore, Style

from .dspy_core import DSPyQuizChallenge, QuizResult, QuizResults

# Initialize colorama for cross-platform color support
colorama.init()

logger = logging.getLogger(__name__)


class Colors:
    """Color definitions for terminal output."""

    # Headers and labels
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT

    # Content
    QUESTION = Fore.MAGENTA
    ANSWER = Fore.WHITE + Style.BRIGHT
    AI_RESPONSE = Fore.LIGHTBLUE_EX
    EVALUATION = Fore.YELLOW

    # Status indicators
    WIN = Fore.GREEN + Style.BRIGHT
    LOSE = Fore.RED + Style.BRIGHT
    INVALID = Fore.YELLOW + Style.BRIGHT

    # Reset
    RESET = Style.RESET_ALL


def load_config(config_file: Path) -> Dict[str, Any]:
    """Load configuration from TOML file.

    Args:
        config_file: Path to TOML configuration file

    Returns:
        Dictionary with configuration parameters
    """
    try:
        with open(config_file, "rb") as f:
            config = tomllib.load(f)

        logger.info(f"Loaded configuration from {config_file}")
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {config_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration file {config_file}: {e}")
        sys.exit(1)


def merge_config_with_args(args, config: Dict[str, Any]) -> None:
    """Merge configuration file values with command line arguments.

    Command line arguments take precedence over config file values.

    Args:
        args: Parsed command line arguments
        config: Configuration dictionary from TOML file
    """
    # API configuration
    api_config = config.get("api", {})
    if args.base_url == "https://openrouter.ai/api/v1" and "base_url" in api_config:
        args.base_url = api_config["base_url"]

    # Model configuration
    models_config = config.get("models", {})
    if not hasattr(args, "quiz_model") or args.quiz_model == "gpt-4o-mini":
        args.quiz_model = models_config.get("quiz_model", "gpt-4o-mini")
    if not hasattr(args, "evaluator_model") or args.evaluator_model == "gpt-4o":
        args.evaluator_model = models_config.get("evaluator_model", "gpt-4o")

    # Context configuration
    context_config = config.get("context", {})
    if not hasattr(args, "context_strictness") or args.context_strictness == "normal":
        args.context_strictness = context_config.get("strictness", "normal")
    if not args.context_urls and "urls" in context_config:
        # Convert URLs list to temporary file for compatibility
        urls = context_config["urls"]
        if urls:
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                for url in urls:
                    f.write(f"{url}\n")
                args.context_urls = f.name
                args._temp_context_file = f.name  # Track for cleanup

    # Output configuration
    output_config = config.get("output", {})
    if not args.output and "results_file" in output_config:
        args.output = Path(output_config["results_file"])
    if not args.verbose and output_config.get("verbose", False):
        args.verbose = True


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    if verbose:
        level = logging.DEBUG
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    else:
        # Hide all log messages by setting level to CRITICAL
        logging.basicConfig(level=logging.CRITICAL, handlers=[logging.NullHandler()])


def format_revision_guidance(results: QuizResults) -> str:
    """Format concise revision guidance for display to the student."""
    if not results.question_results:
        return ""

    # Only show guidance for questions that need improvement (lost to AI or invalid)
    needs_improvement = []
    for result in results.question_results:
        if not result.is_valid or not result.student_wins:
            needs_improvement.append(result)

    if not needs_improvement:
        return f"\n{Colors.SUCCESS}✨ All your questions successfully stumped the AI! No revisions needed.{Colors.RESET}"

    guidance_sections = []
    guidance_sections.append("\n" + "=" * 60)
    guidance_sections.append(f"{Colors.WARNING}💡 HOW TO IMPROVE YOUR QUESTIONS{Colors.RESET}")
    guidance_sections.append("=" * 60)

    for result in needs_improvement:
        guidance_sections.append(
            f"\n{Colors.HEADER}Question {result.question.number}:{Colors.RESET}"
        )
        guidance_sections.append(f'   {Colors.QUESTION}"{result.question.question}"{Colors.RESET}')

        if not result.is_valid:
            guidance_sections.append(
                f"   {Colors.HEADER}Status:{Colors.RESET} {Colors.ERROR}❌ Invalid question{Colors.RESET}"
            )
            guidance_sections.append(
                f"   {Colors.HEADER}Issue:{Colors.RESET} {Colors.ERROR}{result.error}{Colors.RESET}"
            )
        else:
            guidance_sections.append(
                f"   {Colors.HEADER}Status:{Colors.RESET} {Colors.LOSE}❌ AI answered correctly{Colors.RESET}"
            )

        if result.revision_guidance:
            guidance = result.revision_guidance
            if guidance.concrete_suggestions:
                guidance_sections.append(f"   {Colors.HEADER}Suggestions:{Colors.RESET}")
                for suggestion in guidance.concrete_suggestions[:3]:  # Limit to top 3
                    guidance_sections.append(f"   {Colors.INFO}• {suggestion}{Colors.RESET}")

    guidance_sections.append("\n" + "=" * 60)

    return "\n".join(guidance_sections)


def validate_arguments(args) -> bool:
    """Validate command line arguments."""
    # Check quiz file exists
    if not args.quiz_file.exists():
        print(f"Error: Quiz file not found: {args.quiz_file}")
        return False

    # Check API key is provided
    if not args.api_key or not args.api_key.strip():
        print("Error: API key is required (use --api-key or environment variable)")
        return False

    # Check base URL is provided
    if not args.base_url:
        print("Error: Base URL is required (use --base-url)")
        return False

    return True


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="LLM Quiz Challenge - Students create questions to stump AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default OpenRouter settings
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-or-v1-xxx

  # Run with custom Ollama instance
  python -m llm_quiz.cli --quiz-file quiz.toml --base-url http://localhost:11434/v1 --api-key dummy

  # Run with custom models
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --quiz-model gpt-4o-mini --evaluator-model gpt-4o

  # Load context from URLs file
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --context-urls context_urls.txt

  # Save results and show verbose output
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --output results.json --verbose

  # Use configuration file for parameters and context
  python -m llm_quiz.cli --quiz-file quiz.toml --api-key sk-xxx --config config.toml

GitHub Classroom Integration:
  - Exit code 0: Student passes (100% win rate on valid questions)
  - Exit code 1: Student fails (less than 100% win rate or no valid questions)
  - Results include STUDENTS_QUIZ_KEIKO_WIN/LOSE markers for automated grading
        """,
    )

    # Required arguments
    parser.add_argument(
        "--quiz-file",
        type=Path,
        required=True,
        help="Path to TOML quiz file containing student's questions and their correct answers",
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to TOML configuration file with parameters and context URLs",
    )

    parser.add_argument(
        "--api-key",
        required=True,
        help="API key for LLM endpoint (or set via environment variable)",
    )

    # API configuration
    parser.add_argument(
        "--base-url",
        default="https://openrouter.ai/api/v1",
        help="Base URL for LLM API endpoint (default: OpenRouter)",
    )

    # Model configuration
    parser.add_argument(
        "--quiz-model",
        default="gpt-4o-mini",
        help="Model for LLM to answer student's questions (based on lightlm). For OpenRouter users, use 'openrouter/' prefix. For Ollama users, specify model name directly (default: gpt-4o-mini)",
    )

    parser.add_argument(
        "--evaluator-model",
        default="gpt-4o",
        help="Model for evaluating LLM's answers against student's correct answers (based on lightlm). For OpenRouter users, use 'openrouter/' prefix. For Ollama users, specify model name directly (default: gpt-4o)",
    )

    # Context configuration
    parser.add_argument(
        "--context-urls", help="File containing URLs to fetch for context (one URL per line)"
    )

    # Output configuration
    parser.add_argument("--output", type=Path, help="Output JSON file for detailed results")

    # Behavior options
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging output")

    parser.add_argument(
        "--exit-on-fail",
        action="store_true",
        default=True,
        help="Exit with error code if students don't pass (default: True)",
    )
    
    parser.add_argument(
        "--context-strictness",
        choices=["strict", "normal", "lenient"],
        default="normal",
        help="How strictly to check context alignment: 'strict' (only direct matches), 'normal' (direct + extensions), 'lenient' (also allows tangential) (default: normal)",
    )
    
    parser.add_argument(
        "--verify-answers",
        action="store_true",
        default=True,
        help="Enable fact-checking of student answers to ensure correctness (default: True)",
    )
    
    parser.add_argument(
        "--no-verify-answers",
        dest="verify_answers",
        action="store_false",
        help="Disable fact-checking of student answers (trust student answers as ground truth)",
    )

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Load configuration file if provided
    if args.config:
        config = load_config(args.config)
        merge_config_with_args(args, config)

    # Set up logging
    setup_logging(args.verbose)

    # Validate arguments
    if not validate_arguments(args):
        sys.exit(1)

    try:
        # Initialize DSPy LLM Quiz Challenge with progress indicators
        print(f"{Colors.INFO}🔧 Initializing quiz system...{Colors.RESET}")
        logger.info("Initializing DSPy LLM Quiz Challenge...")
        logger.info(f"Base URL: {args.base_url}")
        logger.info(f"Quiz Model: {args.quiz_model}")
        logger.info(f"Evaluator Model: {args.evaluator_model}")
        if args.context_urls:
            logger.info(f"Context URLs file: {args.context_urls}")
            print(f"{Colors.INFO}📥 Loading context materials...{Colors.RESET}")

        challenge = DSPyQuizChallenge(
            api_key=args.api_key,
            base_url=args.base_url,
            quiz_model=args.quiz_model,
            evaluator_model=args.evaluator_model,
            context_urls_file=args.context_urls,
            context_strictness=args.context_strictness,
            verify_student_answers=args.verify_answers,
        )

        # Load and run quiz
        print(f"{Colors.INFO}📋 Loading quiz questions...{Colors.RESET}")
        questions = challenge.load_quiz_from_file(args.quiz_file)
        print(
            f"{Colors.INFO}🚀 Starting quiz challenge with {len(questions)} questions...{Colors.RESET}"
        )
        results = challenge.run_quiz_challenge(questions)

        # Display clear pass/fail result first
        print("=" * 80)
        if results.student_passes:
            print(
                f"{Colors.SUCCESS}🎉 RESULT: PASS - You successfully stumped the AI!{Colors.RESET}"
            )
        else:
            print(
                f"{Colors.ERROR}❌ RESULT: FAIL - The AI answered too many questions correctly{Colors.RESET}"
            )
        print("=" * 80)

        # Display summary statistics
        print(
            f"{Colors.INFO}📊 Summary:{Colors.RESET} {results.student_wins}/{results.valid_questions} questions stumped the AI"
        )
        print(f"{Colors.INFO}Success Rate:{Colors.RESET} {results.success_rate:.1%}")
        print()

        # Display detailed results for each question
        for result in results.question_results:
            if result.is_valid:
                # Determine status based on student answer correctness and win status
                if hasattr(result, 'student_answer_correctness') and result.student_answer_correctness == 'INCORRECT':
                    status_text = f"{Colors.ERROR}❌ Your answer is incorrect{Colors.RESET}"
                elif result.student_wins:
                    status_text = f"{Colors.WIN}✅ You win!{Colors.RESET}"
                else:
                    status_text = f"{Colors.LOSE}❌ AI wins{Colors.RESET}"

                print(
                    f"{Colors.HEADER}Question {result.question.number}:{Colors.RESET} {status_text}"
                )
                print(
                    f"  {Colors.HEADER}Your question:{Colors.RESET} {Colors.QUESTION}{result.question.question}{Colors.RESET}"
                )
                print(
                    f"  {Colors.HEADER}Your answer:{Colors.RESET} {Colors.ANSWER}{result.question.answer}{Colors.RESET}"
                )
                
                # Show if student answer has issues
                if hasattr(result, 'student_answer_correctness') and result.student_answer_correctness != 'CORRECT':
                    print(
                        f"  {Colors.ERROR}Answer Status: {result.student_answer_correctness}{Colors.RESET}"
                    )
                    if hasattr(result, 'factual_issues') and result.factual_issues:
                        print(
                            f"  {Colors.ERROR}Factual Issues: {', '.join(result.factual_issues)}{Colors.RESET}"
                        )
                
                print(
                    f"  {Colors.HEADER}AI's answer:{Colors.RESET} {Colors.AI_RESPONSE}{result.llm_answer}{Colors.RESET}"
                )
                print(
                    f"  {Colors.HEADER}Evaluation:{Colors.RESET} {Colors.EVALUATION}{result.evaluation_explanation}{Colors.RESET}"
                )
            else:
                print(
                    f"{Colors.HEADER}Question {result.question.number}:{Colors.RESET} {Colors.INVALID}⚠️ Invalid{Colors.RESET}"
                )
                print(
                    f"  {Colors.HEADER}Your question:{Colors.RESET} {Colors.QUESTION}{result.question.question}{Colors.RESET}"
                )
                print(
                    f"  {Colors.HEADER}Issue:{Colors.RESET} {Colors.ERROR}{result.error}{Colors.RESET}"
                )
            print()

        # Display concise revision guidance only if questions need improvement
        revision_guidance = format_revision_guidance(results)
        if revision_guidance:
            print(revision_guidance)

        # Save results
        if args.output:
            challenge.save_results(results, args.output)
            logger.info(f"Detailed results saved to {args.output}")

        # Exit with appropriate code for GitHub Classroom
        if args.exit_on_fail and not results.student_passes:
            logger.info("Student did not pass grading criteria")
            exit_code = 1
        else:
            logger.info("Quiz challenge completed successfully")
            exit_code = 0

    except KeyboardInterrupt:
        logger.info("Quiz challenge interrupted by user")
        exit_code = 1
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        exit_code = 1
    finally:
        # Clean up temporary context file if created
        if hasattr(args, "_temp_context_file"):
            try:
                import os

                os.unlink(args._temp_context_file)
                logger.debug(f"Cleaned up temporary context file: {args._temp_context_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {e}")

        sys.exit(exit_code)


if __name__ == "__main__":
    main()
