"""
Error Categorization Module for LLM Evaluation Framework.

This module provides logic for categorizing different types of failures
in LLM-generated responses, including hallucinations, reasoning gaps,
and instruction adherence issues.
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

# Clarity assessment constant
MAX_AVG_SENTENCE_LENGTH_WORDS = 40


class ErrorType(Enum):
    """Enumeration of error types in LLM responses."""
    HALLUCINATION = "hallucination"
    FACTUAL_ERROR = "factual_error"
    REASONING_GAP = "reasoning_gap"
    INSTRUCTION_DEVIATION = "instruction_deviation"
    CLARITY_ISSUE = "clarity_issue"
    INCOMPLETE_RESPONSE = "incomplete_response"
    BIAS_DETECTED = "bias_detected"
    UNSAFE_CONTENT = "unsafe_content"


class ErrorSeverity(Enum):
    """Severity levels for detected errors."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ErrorInstance:
    """Represents a detected error in an LLM response."""
    error_type: ErrorType
    severity: ErrorSeverity
    description: str
    location: Optional[str] = None
    evidence: Optional[str] = None
    suggested_fix: Optional[str] = None


class ErrorCategorizer:
    """
    Categorizes and analyzes errors in LLM responses.
    
    This class provides methods to detect and categorize various types
    of errors in LLM-generated content.
    """
    
    def __init__(self):
        self.error_log: List[ErrorInstance] = []
    
    def detect_hallucination(
        self,
        response: str,
        facts: List[str],
        context: Optional[str] = None
    ) -> Optional[ErrorInstance]:
        """
        Detect potential hallucinations in the response.

        This implementation uses a simple, keyword-based heuristic to flag
        potentially hallucinated content. It does not currently perform any
        fact-checking or comparison against the provided ``facts`` or
        ``context`` values; those parameters are accepted for interface
        compatibility and potential future extensions.
        
        Args:
            response: The LLM-generated response.
            facts: Optional list of verified facts related to the response.
                Currently unused by this heuristic implementation.
            context: Optional context used for generation of the response.
                Currently unused by this heuristic implementation.
            
        Returns:
            ErrorInstance if a potential hallucination is detected by the
            heuristic, None otherwise.
        """
        # Simple keyword-based detection (can be enhanced with ML models)
        hallucination_indicators = [
            "I remember", "I recall", "As I saw", "From my personal experience"
        ]
        
        for indicator in hallucination_indicators:
            if indicator.lower() in response.lower():
                error = ErrorInstance(
                    error_type=ErrorType.HALLUCINATION,
                    severity=ErrorSeverity.HIGH,
                    description=f"Potential hallucination detected: '{indicator}' found in response",
                    evidence=indicator,
                    suggested_fix="Remove personal references and stick to factual information"
                )
                self.error_log.append(error)
                return error
        
        return None
    
    def check_factual_accuracy(
        self,
        response: str,
        reference_facts: Dict[str, str]
    ) -> List[ErrorInstance]:
        """
        Check factual accuracy against reference facts.
        
        Args:
            response: The LLM-generated response
            reference_facts: Dictionary of fact keys and their correct values
            
        Returns:
            List of ErrorInstance objects for detected factual errors
        """
        errors = []
        
        for fact_key, correct_value in reference_facts.items():
            if fact_key.lower() in response.lower():
                # Check if the correct value is also present
                if correct_value.lower() not in response.lower():
                    error = ErrorInstance(
                        error_type=ErrorType.FACTUAL_ERROR,
                        severity=ErrorSeverity.CRITICAL,
                        description=f"Factual error: {fact_key} mentioned but incorrect value",
                        evidence=f"Expected: {correct_value}",
                        suggested_fix=f"Replace with correct value: {correct_value}"
                    )
                    errors.append(error)
                    self.error_log.append(error)
        
        return errors
    
    def evaluate_reasoning_quality(
        self,
        response: str,
        required_steps: List[str]
    ) -> Optional[ErrorInstance]:
        """
        Evaluate the reasoning quality of the response.
        
        Args:
            response: The LLM-generated response
            required_steps: List of reasoning steps that should be present
            
        Returns:
            ErrorInstance if reasoning gaps detected, None otherwise
        """
        missing_steps = []
        
        for step in required_steps:
            if step.lower() not in response.lower():
                missing_steps.append(step)
        
        if missing_steps:
            error = ErrorInstance(
                error_type=ErrorType.REASONING_GAP,
                severity=ErrorSeverity.MEDIUM,
                description=f"Missing reasoning steps: {', '.join(missing_steps)}",
                suggested_fix="Include all required reasoning steps in the response"
            )
            self.error_log.append(error)
            return error
        
        return None
    
    def check_instruction_adherence(
        self,
        response: str,
        instructions: List[str]
    ) -> List[ErrorInstance]:
        """
        Check if the response adheres to given instructions.
        
        Args:
            response: The LLM-generated response
            instructions: List of instructions that should be followed
            
        Returns:
            List of ErrorInstance objects for instruction deviations
        """
        errors = []
        
        for instruction in instructions:
            # Simple keyword check - can be enhanced
            if "must include" in instruction.lower():
                required_term = instruction.split("must include")[-1].strip().strip('"\'')
                if required_term.lower() not in response.lower():
                    error = ErrorInstance(
                        error_type=ErrorType.INSTRUCTION_DEVIATION,
                        severity=ErrorSeverity.HIGH,
                        description=f"Required term '{required_term}' not found in response",
                        suggested_fix=f"Include '{required_term}' in the response"
                    )
                    errors.append(error)
                    self.error_log.append(error)
        
        return errors
    
    def assess_clarity(self, response: str) -> Optional[ErrorInstance]:
        """
        Assess the clarity of the response.
        
        Args:
            response: The LLM-generated response
            
        Returns:
            ErrorInstance if clarity issues detected, None otherwise
        """
        # Simple heuristics for clarity
        # Split on periods and filter out empty/whitespace-only segments so only real sentences count
        sentences = [s for s in response.split('.') if s.strip()]
        if not sentences:
            return None
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        if avg_sentence_length > MAX_AVG_SENTENCE_LENGTH_WORDS:
            error = ErrorInstance(
                error_type=ErrorType.CLARITY_ISSUE,
                severity=ErrorSeverity.LOW,
                description="Response contains overly long sentences affecting clarity",
                suggested_fix="Break down long sentences into shorter, clearer statements"
            )
            self.error_log.append(error)
            return error
        
        return None
    
    def get_error_summary(self) -> Dict[str, int]:
        """
        Get a summary of all detected errors by type.
        
        Returns:
            Dictionary mapping error types to their counts
        """
        summary = {}
        for error in self.error_log:
            error_type_name = error.error_type.value
            summary[error_type_name] = summary.get(error_type_name, 0) + 1
        return summary
    
    def clear_log(self):
        """Clear the error log."""
        self.error_log.clear()
