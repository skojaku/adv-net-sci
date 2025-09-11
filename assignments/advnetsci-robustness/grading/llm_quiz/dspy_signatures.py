"""
DSPy signatures for the LLM Quiz Challenge.

This module defines structured DSPy signatures that replace complex manual
prompt engineering and JSON parsing with clean, type-safe interactions.
"""

from enum import Enum
from typing import List, Literal, Optional

import dspy


class ValidationIssue(str, Enum):
    """Types of validation issues that can occur with quiz questions."""

    HEAVY_MATH = "heavy_math"
    PROMPT_INJECTION = "prompt_injection"
    ANSWER_QUALITY = "answer_quality"
    CONTEXT_MISMATCH = (
        "context_mismatch"  # Question is completely unrelated to course topic (use sparingly - allow reasonable extensions)
    )
    WEAK_CONTEXT_ALIGNMENT = (
        "weak_context_alignment"  # Question is tangentially related but doesn't align well with context (consider if derivable from material)
    )
    VAGUE_QUESTION = "vague_question"  # Question lacks specificity or clarity
    AMBIGUOUS_WORDING = "ambiguous_wording"  # Question has multiple interpretations
    INCOMPLETE_CONTEXT = "incomplete_context"  # Question lacks sufficient context to answer clearly
    DUPLICATE_QUESTION = "duplicate_question"  # Question is very similar to another question
    OVERLAPPING_CONTENT = "overlapping_content"  # Question covers content heavily overlapping with another


class ParseQuestionAndAnswer(dspy.Signature):
    """Parse questions and answers from raw student input in various formats."""

    raw_input: str = dspy.InputField(
        desc="Student input containing questions and answers in any format"
    )

    questions: List[str] = dspy.OutputField(desc="List of extracted questions")
    answers: List[str] = dspy.OutputField(
        desc="List of corresponding answers, 'MISSING' if not provided"
    )
    has_answers: List[bool] = dspy.OutputField(desc="Whether each question has a provided answer")


class ValidateQuestion(dspy.Signature):
    """Validate a student's quiz question and their provided correct answer.

    CONTENT ALIGNMENT REQUIREMENTS:
    - Flag context_mismatch ONLY for questions about completely UNRELATED topics not covered in context
      Example: Context about Euler paths, question about spectral clustering = context_mismatch
    - DO NOT flag context_mismatch for questions that extend or apply concepts from the context
      Example: Context about node degree, question about self-loops in degree calculation = acceptable extension
    - Flag weak_context_alignment if the question is tangentially related but requires substantial external knowledge
    - Questions may explore implications, edge cases, or applications of concepts if they can be reasoned from context
    - DISTINGUISH between "different topic" (mismatch) vs "derived application" (acceptable)
    
    CLARITY AND SPECIFICITY REQUIREMENTS:
    - Flag vague_question if the question lacks specificity or is too general
    - Flag ambiguous_wording if the question has multiple valid interpretations
    - Flag incomplete_context if the question lacks sufficient context to answer clearly
    - Questions should be precise, unambiguous, and clearly worded
    
    CONTENT DEPTH REQUIREMENTS:
    - Questions should require understanding beyond simple memorization
    - Questions should connect concepts or require analysis/application of knowledge
    - Higher-level questions that explore limitations, implications, or applications of core concepts are encouraged"""

    question: str = dspy.InputField(desc="The student's quiz question to validate")
    answer: str = dspy.InputField(desc="The student's provided correct answer")
    context_content: Optional[str] = dspy.InputField(desc="Course context materials, if available")

    is_valid: bool = dspy.OutputField(desc="Whether the question is valid and acceptable")
    issues: List[ValidationIssue] = dspy.OutputField(
        desc="List of specific validation issues found (check for context_mismatch, weak_context_alignment, vague_question, ambiguous_wording, incomplete_context). STRICTLY flag context_mismatch when the question is about topics not covered in the provided context materials. Check if the question topic matches the subject matter of the provided context."
    )
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = dspy.OutputField(
        desc="Confidence in validation decision"
    )
    reason: str = dspy.OutputField(desc="Brief explanation of the validation decision")
    revision_suggestions: List[str] = dspy.OutputField(
        desc="Specific suggestions for improving the question if invalid"
    )
    difficulty_assessment: Literal["TOO_EASY", "APPROPRIATE", "TOO_HARD"] = dspy.OutputField(
        desc="Assessment of question difficulty level"
    )
    clarity_score: Literal["CLEAR", "SOMEWHAT_CLEAR", "UNCLEAR"] = dspy.OutputField(
        desc="Assessment of question clarity and specificity"
    )


class AnswerQuizQuestion(dspy.Signature):
    """LLM attempts to answer a student's quiz question using provided context materials."""

    question: str = dspy.InputField(desc="The student's quiz question for LLM to answer")
    context_content: Optional[str] = dspy.InputField(desc="Course context materials for reference")

    answer: str = dspy.OutputField(
        desc="Concise but thorough answer to the question (max 300 words)"
    )


class CheckContextAlignment(dspy.Signature):
    """Check if a quiz question aligns with the provided context materials.
    
    This validator determines whether a question substantially deviates from the context
    or is a reasonable extension/application of the concepts presented.
    
    ALIGNMENT CATEGORIES:
    - DIRECT: Question directly tests concepts explicitly covered in the context
    - EXTENSION: Question asks about implications, applications, or derived knowledge that can be reasoned from the context
    - TANGENTIAL: Question is loosely related but requires significant external knowledge
    - UNRELATED: Question is about completely different topics (substantial deviation)
    
    EXAMPLES OF ACCEPTABLE (DIRECT or EXTENSION):
    - Context: "Node degree is the number of edges connected to a node"
      Question: "How do you count degree when a node has a self-loop?" (EXTENSION - applies the concept)
    - Context: "PageRank measures node importance based on link structure"  
      Question: "What happens to PageRank if all nodes have equal in-degree?" (EXTENSION - explores implications)
    
    EXAMPLES OF UNACCEPTABLE (UNRELATED):
    - Context: "Euler paths visit every edge exactly once"
      Question: "How does spectral clustering partition a graph?" (UNRELATED - different topic entirely)
    - Context: "Small-world networks have short path lengths"
      Question: "What is the time complexity of Dijkstra's algorithm?" (UNRELATED - algorithm analysis vs network property)
    """
    
    question: str = dspy.InputField(desc="The quiz question to check alignment for")
    answer: str = dspy.InputField(desc="The provided answer (for additional context)")
    context_content: str = dspy.InputField(desc="The course context materials")
    
    alignment_type: Literal["DIRECT", "EXTENSION", "TANGENTIAL", "UNRELATED"] = dspy.OutputField(
        desc="Type of alignment between question and context"
    )
    is_substantial_deviation: bool = dspy.OutputField(
        desc="True if the question is UNRELATED to context topics (substantial deviation)"
    )
    reasoning: str = dspy.OutputField(
        desc="Detailed explanation of why this alignment was determined"
    )
    context_topics: List[str] = dspy.OutputField(
        desc="Main topics/concepts found in the provided context"
    )
    question_topics: List[str] = dspy.OutputField(
        desc="Main topics/concepts the question is asking about"
    )
    suggestions: List[str] = dspy.OutputField(
        desc="If misaligned, suggestions for how to better align the question with context"
    )


class ValidateQuestionSimilarity(dspy.Signature):
    """Check for similarity and overlap between multiple quiz questions.
    
    This validator checks if questions are duplicates or have significant content overlap.
    Questions should cover distinct topics and concepts to provide comprehensive assessment.
    
    SIMILARITY CRITERIA - BE LENIENT:
    - Flag duplicate_question ONLY if questions are essentially asking the exact same thing with near-identical wording
    - Flag overlapping_content ONLY if questions test the exact same specific knowledge with no meaningful distinction
    - Questions about different aspects, limitations, or applications of the same general topic should NOT be flagged as similar
    - Questions that require different reasoning or demonstrate different understanding should be allowed
    - BE GENEROUS - only flag as similar if they are genuinely redundant or nearly identical
    - Different phrasings that test distinct concepts or reasoning should NOT be flagged as duplicates"""

    questions: List[str] = dspy.InputField(desc="List of all questions to check for similarity")
    answers: List[str] = dspy.InputField(desc="List of corresponding answers for context")

    has_duplicates: bool = dspy.OutputField(desc="Whether any questions are genuine duplicates (nearly identical). Be very conservative - only flag if truly redundant.")
    has_overlaps: bool = dspy.OutputField(desc="Whether any questions test the exact same specific knowledge. Be lenient - different aspects of same topic are OK.")
    duplicate_pairs: List[str] = dspy.OutputField(desc="Pairs of question indices that are genuine duplicates (e.g., '1-2')")
    overlap_pairs: List[str] = dspy.OutputField(desc="Pairs of question indices with identical knowledge testing")
    similarity_details: List[str] = dspy.OutputField(desc="Detailed explanation of each similarity found, including why it's considered similar or why it's acceptable")
    overall_assessment: str = dspy.OutputField(desc="Overall assessment of question diversity and coverage, being generous with different aspects of same topic")


class EvaluateAnswer(dspy.Signature):
    """Evaluate an LLM's answer against the student's provided answer, while fact-checking both.
    
    IMPORTANT EVALUATION CRITERIA:
    1. First, verify if the student's provided answer is factually correct
    2. Then, evaluate if the LLM's answer is factually correct
    3. Student wins ONLY if their answer is correct AND the LLM's answer is incorrect
    4. If student's answer is factually wrong, they cannot win regardless of LLM's answer
    
    FACT-CHECKING GUIDELINES:
    - Verify factual accuracy based on established knowledge
    - Check for logical consistency in the reasoning
    - Identify misconceptions or errors in understanding
    - Consider if there might be multiple valid perspectives
    
    EXAMPLES:
    - If student says "False" to a true statement, their answer is incorrect
    - If student provides wrong reasoning (e.g., "depends on network size" when it actually depends on rewiring probability), mark as incorrect
    - If both answers are correct but approach differently, both are correct"""

    question: str = dspy.InputField(desc="The student's quiz question")
    correct_answer: str = dspy.InputField(desc="The student's provided correct answer")
    llm_answer: str = dspy.InputField(desc="The LLM's attempt at answering the student's question")

    verdict: Literal["CORRECT", "INCORRECT"] = dspy.OutputField(
        desc="Whether the LLM's answer is factually correct"
    )
    student_answer_correctness: Literal["CORRECT", "INCORRECT", "PARTIALLY_CORRECT"] = dspy.OutputField(
        desc="Whether the student's provided answer is factually correct"
    )
    student_wins: bool = dspy.OutputField(
        desc="True if student wins (student correct AND LLM wrong), False otherwise"
    )
    explanation: str = dspy.OutputField(
        desc="Detailed explanation including fact-checking of both answers"
    )
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = dspy.OutputField(
        desc="Confidence level in the evaluation"
    )
    factual_issues: List[str] = dspy.OutputField(
        desc="List of factual errors found in either answer"
    )
    improvement_suggestions: List[str] = dspy.OutputField(
        desc="Suggestions for improving the question or correcting misconceptions"
    )


class GenerateRevisionGuidance(dspy.Signature):
    """Generate detailed revision guidance for student's quiz questions that need improvement.
    
    Focus especially on clarity and specificity issues:
    - Provide specific guidance for making vague questions more precise
    - Suggest ways to eliminate ambiguous wording
    - Recommend adding context when questions are incomplete
    - Give concrete examples of clearer question formulations"""

    question: str = dspy.InputField(desc="The student's quiz question")
    answer: str = dspy.InputField(desc="The student's provided correct answer")
    validation_issues: List[str] = dspy.InputField(desc="Issues found during validation")
    llm_response: Optional[str] = dspy.InputField(
        desc="LLM's attempt at answering if question was processed"
    )
    evaluation_result: Optional[str] = dspy.InputField(
        desc="Evaluation result if question was processed"
    )
    context_topics: List[str] = dspy.InputField(desc="Main topics covered in the context materials")

    revision_priority: Literal["HIGH", "MEDIUM", "LOW"] = dspy.OutputField(
        desc="Priority level for revising this question"
    )
    specific_issues: List[str] = dspy.OutputField(
        desc="Detailed list of specific problems with the question"
    )
    concrete_suggestions: List[str] = dspy.OutputField(
        desc="Step-by-step suggestions for improvement, focusing on clarity and specificity"
    )
    example_improvements: List[str] = dspy.OutputField(
        desc="Concrete examples of how to rewrite parts of the question for better clarity"
    )
    difficulty_adjustment: str = dspy.OutputField(
        desc="How to adjust difficulty level appropriately"
    )
    context_alignment: str = dspy.OutputField(
        desc="How to better align question with provided context materials"
    )
    clarity_improvements: List[str] = dspy.OutputField(
        desc="Specific suggestions for making the question clearer and more precise"
    )


class GenerateFeedback(dspy.Signature):
    """Generate comprehensive feedback for students based on quiz results."""

    total_questions: int = dspy.InputField(desc="Total number of questions submitted")
    valid_questions: int = dspy.InputField(desc="Number of valid questions")
    invalid_questions: int = dspy.InputField(desc="Number of invalid questions")
    student_wins: int = dspy.InputField(desc="Number of questions where student won")
    llm_wins: int = dspy.InputField(desc="Number of questions where LLM won")
    validation_issues: List[str] = dspy.InputField(desc="List of validation issues encountered")
    success_rate: float = dspy.InputField(desc="Student success rate (0.0 to 1.0)")

    feedback_summary: str = dspy.OutputField(desc="Comprehensive feedback summary for the student")
    pass_result: Literal["PASS", "FAIL"] = dspy.OutputField(
        desc="Whether the student passed the challenge"
    )
    github_classroom_marker: str = dspy.OutputField(desc="GitHub Classroom result marker")
    improvement_tips: List[str] = dspy.OutputField(desc="Specific tips for improvement")
