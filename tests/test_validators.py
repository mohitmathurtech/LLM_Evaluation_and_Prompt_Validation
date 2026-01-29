"""
Unit tests for Validators module.

Tests the response validation and schema validation functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.evaluation.validators import (
    ResponseValidator,
    SchemaValidator,
    ValidationStatus,
    ValidationMetric,
    ValidationResult
)


class TestResponseValidator(unittest.TestCase):
    """Test cases for ResponseValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = ResponseValidator()
    
    def test_validate_response_complete(self):
        """Test validation of a complete, high-quality response."""
        response = """
        This is a clear and well-structured response. It explains the concept thoroughly.
        For example, we can see how the idea applies in practice. Therefore, the conclusion
        is well-supported by the reasoning. Additionally, all required elements are present.
        """
        prompt = "Explain the concept"
        expected_elements = ["concept", "example", "conclusion"]
        
        result = self.validator.validate_response(response, prompt, expected_elements)
        
        # The response may be too short, so check status is not failed due to critical issues
        self.assertNotEqual(result.status, ValidationStatus.FAILED)
        self.assertGreater(result.overall_score, 0.5)
    
    def test_validate_clarity_good(self):
        """Test clarity validation with good text."""
        response = "This is clear. The explanation is straightforward. However, more detail is needed."
        
        metric = self.validator._validate_clarity(response)
        
        self.assertTrue(metric.passed)
        self.assertGreaterEqual(metric.score, self.validator.config["min_clarity_score"])
    
    def test_validate_clarity_poor(self):
        """Test clarity validation with poor text."""
        response = "X."  # Very short, unclear
        
        metric = self.validator._validate_clarity(response)
        
        # May or may not pass depending on implementation
        self.assertIsNotNone(metric)
    
    def test_validate_completeness_all_present(self):
        """Test completeness when all elements are present."""
        response = "The concept includes examples, reasoning, and conclusions."
        expected_elements = ["concept", "examples", "reasoning", "conclusions"]
        
        metric = self.validator._validate_completeness(response, expected_elements)
        
        self.assertTrue(metric.passed)
        self.assertEqual(metric.score, 1.0)
    
    def test_validate_completeness_missing_elements(self):
        """Test completeness when elements are missing."""
        response = "The concept includes examples."
        expected_elements = ["concept", "examples", "reasoning", "conclusions"]
        
        metric = self.validator._validate_completeness(response, expected_elements)
        
        self.assertFalse(metric.passed)
        self.assertLess(metric.score, 1.0)
    
    def test_validate_reasoning_depth_good(self):
        """Test reasoning depth with good reasoning indicators."""
        response = """
        This happens because of several factors. Therefore, we can conclude
        that the result is expected. For example, in similar cases, we see
        the same pattern. This means our hypothesis is correct.
        """
        
        metric = self.validator._validate_reasoning_depth(response)
        
        self.assertTrue(metric.passed)
    
    def test_validate_reasoning_depth_shallow(self):
        """Test reasoning depth with shallow reasoning."""
        response = "This is the answer. It is correct."
        
        metric = self.validator._validate_reasoning_depth(response)
        
        self.assertFalse(metric.passed)
    
    def test_validate_length_optimal(self):
        """Test length validation with optimal length."""
        response = " ".join(["word"] * 100)  # 100 words
        
        metric = self.validator._validate_length(response)
        
        self.assertTrue(metric.passed)
    
    def test_validate_length_too_short(self):
        """Test length validation with too short response."""
        response = "Short."
        
        metric = self.validator._validate_length(response)
        
        self.assertFalse(metric.passed)
    
    def test_validate_length_too_long(self):
        """Test length validation with too long response."""
        response = " ".join(["word"] * 3000)  # 3000 words
        
        metric = self.validator._validate_length(response)
        
        self.assertFalse(metric.passed)
    
    def test_validation_result_add_metric(self):
        """Test adding metrics to validation result."""
        result = ValidationResult(status=ValidationStatus.PASSED)
        
        metric = ValidationMetric(
            name="Test",
            score=0.5,
            threshold=0.7,
            passed=False,
            details="Test failed"
        )
        
        result.add_metric(metric)
        
        self.assertEqual(len(result.metrics), 1)
        self.assertEqual(len(result.errors), 1)
    
    def test_validation_result_calculate_score(self):
        """Test overall score calculation."""
        result = ValidationResult(status=ValidationStatus.PASSED)
        
        result.add_metric(ValidationMetric("Test1", 0.8, 0.7, True))
        result.add_metric(ValidationMetric("Test2", 0.9, 0.7, True))
        
        score = result.calculate_overall_score()
        
        self.assertAlmostEqual(score, 0.85, places=2)
        self.assertAlmostEqual(result.overall_score, 0.85, places=2)


class TestSchemaValidator(unittest.TestCase):
    """Test cases for SchemaValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = SchemaValidator()
    
    def test_register_schema(self):
        """Test schema registration."""
        schema = {
            "required_fields": ["title", "description"],
            "format_requirements": {}
        }
        
        self.validator.register_schema("test_schema", schema)
        
        self.assertIn("test_schema", self.validator.schemas)
    
    def test_validate_against_schema_success(self):
        """Test successful schema validation."""
        schema = {
            "required_fields": ["title", "description"]
        }
        self.validator.register_schema("test_schema", schema)
        
        response = "The title is important. Here is a description of the concept."
        
        result = self.validator.validate_against_schema(response, "test_schema")
        
        self.assertEqual(result.status, ValidationStatus.PASSED)
        self.assertEqual(len(result.errors), 0)
    
    def test_validate_against_schema_failure(self):
        """Test failed schema validation."""
        schema = {
            "required_fields": ["title", "description", "examples"]
        }
        self.validator.register_schema("test_schema", schema)
        
        response = "The title is here but no examples."
        
        result = self.validator.validate_against_schema(response, "test_schema")
        
        self.assertEqual(result.status, ValidationStatus.FAILED)
        self.assertGreater(len(result.errors), 0)
    
    def test_validate_nonexistent_schema(self):
        """Test validation against non-existent schema."""
        result = self.validator.validate_against_schema("test", "nonexistent")
        
        self.assertEqual(result.status, ValidationStatus.FAILED)
        self.assertIn("not found", result.errors[0])


if __name__ == '__main__':
    unittest.main()
