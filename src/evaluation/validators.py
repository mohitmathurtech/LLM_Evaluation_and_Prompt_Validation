"""
Validation Schemas for LLM Response Evaluation.

This module provides schemas and validators to measure response clarity,
reasoning gaps, and overall quality of LLM-generated content.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re


class ValidationStatus(Enum):
    """Status of validation result."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass
class ValidationMetric:
    """Represents a validation metric with score and threshold."""
    name: str
    score: float
    threshold: float
    passed: bool
    details: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of a validation check."""
    status: ValidationStatus
    metrics: List[ValidationMetric] = field(default_factory=list)
    overall_score: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_metric(self, metric: ValidationMetric):
        """Add a metric to the validation result."""
        self.metrics.append(metric)
        if not metric.passed:
            self.errors.append(f"{metric.name} failed: {metric.details}")
    
    def calculate_overall_score(self) -> float:
        """Calculate overall score from all metrics."""
        if not self.metrics:
            return 0.0
        self.overall_score = sum(m.score for m in self.metrics) / len(self.metrics)
        return self.overall_score


class ResponseValidator:
    """
    Validates LLM responses against defined criteria.
    
    This class measures response clarity, completeness, reasoning depth,
    and other quality metrics.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the validator with optional configuration.
        
        Args:
            config: Configuration dictionary with thresholds and settings
        """
        self.config = config or self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "min_clarity_score": 0.7,
            "min_completeness_score": 0.8,
            "min_reasoning_depth": 0.6,
            "max_response_length": 2000,
            "min_response_length": 50,
        }
    
    def validate_response(
        self,
        response: str,
        prompt: str,
        expected_elements: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        Perform comprehensive validation on a response.
        
        Args:
            response: The LLM-generated response
            prompt: The original prompt
            expected_elements: Optional list of elements that should be present
            
        Returns:
            ValidationResult object with all metrics and status
        """
        result = ValidationResult(status=ValidationStatus.PASSED)
        
        # Validate clarity
        clarity_metric = self._validate_clarity(response)
        result.add_metric(clarity_metric)
        
        # Validate completeness
        completeness_metric = self._validate_completeness(
            response, expected_elements or []
        )
        result.add_metric(completeness_metric)
        
        # Validate reasoning depth
        reasoning_metric = self._validate_reasoning_depth(response)
        result.add_metric(reasoning_metric)
        
        # Validate length
        length_metric = self._validate_length(response)
        result.add_metric(length_metric)
        
        # Calculate overall score
        result.calculate_overall_score()
        
        # Determine final status
        if any(not m.passed for m in result.metrics):
            result.status = ValidationStatus.FAILED
        elif result.overall_score < 0.75:
            result.status = ValidationStatus.WARNING
            result.warnings.append("Overall score is below recommended threshold")
        
        return result
    
    def _validate_clarity(self, response: str) -> ValidationMetric:
        """
        Validate the clarity of the response.
        
        Measures factors like sentence length, complexity, and readability.
        """
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        
        if not sentences:
            return ValidationMetric(
                name="Clarity",
                score=0.0,
                threshold=self.config["min_clarity_score"],
                passed=False,
                details="Response contains no complete sentences"
            )
        
        # Calculate average sentence length
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Score based on sentence length (optimal: 15-25 words)
        if 15 <= avg_length <= 25:
            length_score = 1.0
        elif 10 <= avg_length < 15 or 25 < avg_length <= 35:
            length_score = 0.8
        else:
            length_score = 0.5
        
        # Check for transition words (indicators of good flow)
        transition_words = ['however', 'therefore', 'moreover', 'furthermore', 
                          'additionally', 'consequently', 'thus', 'hence']
        has_transitions = any(word in response.lower() for word in transition_words)
        transition_score = 1.0 if has_transitions else 0.7
        
        # Calculate final clarity score
        clarity_score = (length_score + transition_score) / 2
        
        return ValidationMetric(
            name="Clarity",
            score=clarity_score,
            threshold=self.config["min_clarity_score"],
            passed=clarity_score >= self.config["min_clarity_score"],
            details=f"Average sentence length: {avg_length:.1f} words"
        )
    
    def _validate_completeness(
        self,
        response: str,
        expected_elements: List[str]
    ) -> ValidationMetric:
        """
        Validate the completeness of the response.
        
        Checks if all expected elements are present.
        """
        if not expected_elements:
            # If no expected elements, give a base score
            return ValidationMetric(
                name="Completeness",
                score=0.8,
                threshold=self.config["min_completeness_score"],
                passed=True,
                details="No specific elements required"
            )
        
        present_elements = sum(
            1 for elem in expected_elements 
            if elem.lower() in response.lower()
        )
        
        completeness_score = present_elements / len(expected_elements)
        missing = [e for e in expected_elements if e.lower() not in response.lower()]
        
        details = f"Found {present_elements}/{len(expected_elements)} expected elements"
        if missing:
            details += f". Missing: {', '.join(missing[:3])}"
        
        return ValidationMetric(
            name="Completeness",
            score=completeness_score,
            threshold=self.config["min_completeness_score"],
            passed=completeness_score >= self.config["min_completeness_score"],
            details=details
        )
    
    def _validate_reasoning_depth(self, response: str) -> ValidationMetric:
        """
        Validate the reasoning depth of the response.
        
        Looks for indicators of deep reasoning like explanations, examples, etc.
        """
        # Reasoning indicators
        reasoning_patterns = [
            r'\bbecause\b',
            r'\btherefore\b',
            r'\bthus\b',
            r'\bfor example\b',
            r'\bfor instance\b',
            r'\bthis means\b',
            r'\bas a result\b',
            r'\bconsequently\b',
        ]
        
        reasoning_count = sum(
            len(re.findall(pattern, response.lower()))
            for pattern in reasoning_patterns
        )
        
        # Score based on frequency (optimal: 2-5 instances)
        if 2 <= reasoning_count <= 5:
            depth_score = 1.0
        elif reasoning_count == 1:
            depth_score = 0.7
        elif reasoning_count > 5:
            depth_score = 0.85
        else:
            depth_score = 0.4
        
        return ValidationMetric(
            name="Reasoning Depth",
            score=depth_score,
            threshold=self.config["min_reasoning_depth"],
            passed=depth_score >= self.config["min_reasoning_depth"],
            details=f"Found {reasoning_count} reasoning indicators"
        )
    
    def _validate_length(self, response: str) -> ValidationMetric:
        """Validate the response length is within acceptable bounds."""
        word_count = len(response.split())
        
        min_length = self.config["min_response_length"]
        max_length = self.config["max_response_length"]
        
        if min_length <= word_count <= max_length:
            length_score = 1.0
            passed = True
            details = f"Response length ({word_count} words) is optimal"
        elif word_count < min_length:
            length_score = word_count / min_length
            passed = False
            details = f"Response too short ({word_count} words, min: {min_length})"
        else:
            length_score = max_length / word_count
            passed = False
            details = f"Response too long ({word_count} words, max: {max_length})"
        
        return ValidationMetric(
            name="Length",
            score=length_score,
            threshold=0.8,
            passed=passed,
            details=details
        )


class SchemaValidator:
    """Validates responses against predefined schemas."""
    
    def __init__(self):
        self.schemas = {}
    
    def register_schema(self, name: str, schema: Dict[str, Any]):
        """Register a validation schema."""
        self.schemas[name] = schema
    
    def validate_against_schema(
        self,
        response: str,
        schema_name: str
    ) -> ValidationResult:
        """
        Validate a response against a registered schema.
        
        Args:
            response: The response to validate
            schema_name: Name of the schema to use
            
        Returns:
            ValidationResult object
        """
        if schema_name not in self.schemas:
            result = ValidationResult(status=ValidationStatus.FAILED)
            result.errors.append(f"Schema '{schema_name}' not found")
            return result
        
        schema = self.schemas[schema_name]
        result = ValidationResult(status=ValidationStatus.PASSED)
        
        # Validate required fields
        required_fields = schema.get("required_fields", [])
        for field in required_fields:
            if field.lower() not in response.lower():
                result.errors.append(f"Required field '{field}' not found")
                result.status = ValidationStatus.FAILED
        
        # Validate format requirements
        format_reqs = schema.get("format_requirements", {})
        for req_name, pattern in format_reqs.items():
            if not re.search(pattern, response):
                result.warnings.append(f"Format requirement '{req_name}' not met")
        
        return result
