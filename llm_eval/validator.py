"""
Prompt Validator Module

Validates prompt templates and LLM prompts for correctness and quality.
"""

from typing import Dict, Any, List, Optional, Tuple
from .prompt_template import PromptTemplate


class PromptValidator:
    """
    Validates prompts to ensure they meet quality standards and
    align with user intent.
    """
    
    def __init__(self):
        """Initialize the prompt validator."""
        self.validation_rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[Dict[str, Any]]:
        """
        Initialize validation rules.
        
        Returns:
            List of validation rules
        """
        return [
            {
                'name': 'min_length',
                'description': 'Prompt must have minimum length',
                'min_value': 10,
                'severity': 'warning'
            },
            {
                'name': 'max_length',
                'description': 'Prompt should not be too long',
                'max_value': 5000,
                'severity': 'warning'
            },
            {
                'name': 'clear_instruction',
                'description': 'Prompt should contain clear instructions',
                'keywords': ['please', 'generate', 'create', 'write', 'explain', 'describe', 'analyze'],
                'severity': 'info'
            },
            {
                'name': 'no_harmful_content',
                'description': 'Prompt should not contain harmful content',
                'forbidden_patterns': ['hack', 'exploit', 'illegal'],
                'severity': 'error'
            }
        ]
    
    def validate_prompt(self, prompt: str) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Validate a prompt string.
        
        Args:
            prompt: The prompt string to validate
            
        Returns:
            Tuple of (is_valid, list of validation issues)
        """
        issues = []
        
        # Check minimum length
        if len(prompt) < 10:
            issues.append({
                'rule': 'min_length',
                'severity': 'warning',
                'message': f"Prompt is too short ({len(prompt)} characters). Minimum recommended: 10"
            })
        
        # Check maximum length
        if len(prompt) > 5000:
            issues.append({
                'rule': 'max_length',
                'severity': 'warning',
                'message': f"Prompt is very long ({len(prompt)} characters). Consider breaking it down."
            })
        
        # Check for clear instructions
        instruction_keywords = ['please', 'generate', 'create', 'write', 'explain', 'describe', 'analyze']
        has_instruction = any(kw in prompt.lower() for kw in instruction_keywords)
        
        if not has_instruction:
            issues.append({
                'rule': 'clear_instruction',
                'severity': 'info',
                'message': "Prompt may benefit from clearer instructions or action verbs"
            })
        
        # Check for potentially harmful content
        forbidden_patterns = ['hack', 'exploit', 'illegal']
        found_harmful = [pattern for pattern in forbidden_patterns if pattern in prompt.lower()]
        
        if found_harmful:
            issues.append({
                'rule': 'no_harmful_content',
                'severity': 'error',
                'message': f"Prompt contains potentially harmful patterns: {', '.join(found_harmful)}"
            })
        
        # Determine if prompt is valid (no errors)
        has_errors = any(issue['severity'] == 'error' for issue in issues)
        is_valid = not has_errors
        
        return is_valid, issues
    
    def validate_template(self, template: PromptTemplate) -> Tuple[bool, List[str]]:
        """
        Validate a prompt template.
        
        Args:
            template: PromptTemplate to validate
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        # First validate the template structure
        is_valid, errors = template.validate()
        
        if not is_valid:
            return False, errors
        
        # Validate the template content
        prompt_valid, issues = self.validate_prompt(template.user_template)
        
        # Add issues as errors if they are severe
        for issue in issues:
            if issue['severity'] == 'error':
                errors.append(issue['message'])
        
        return len(errors) == 0, errors
    
    def check_intent_alignment(self, prompt: str, expected_intent: str) -> Dict[str, Any]:
        """
        Check if a prompt aligns with expected user intent.
        
        Args:
            prompt: The prompt to check
            expected_intent: Description of expected intent
            
        Returns:
            Dictionary containing alignment analysis
        """
        # Simple keyword-based intent matching
        intent_keywords = expected_intent.lower().split()
        prompt_lower = prompt.lower()
        
        matching_keywords = [kw for kw in intent_keywords if kw in prompt_lower]
        alignment_score = len(matching_keywords) / len(intent_keywords) if intent_keywords else 0.0
        
        return {
            'expected_intent': expected_intent,
            'alignment_score': alignment_score,
            'aligned': alignment_score >= 0.5,
            'matching_keywords': matching_keywords,
            'details': f"Found {len(matching_keywords)}/{len(intent_keywords)} intent keywords in prompt"
        }
    
    def suggest_improvements(self, prompt: str) -> List[str]:
        """
        Suggest improvements for a prompt.
        
        Args:
            prompt: The prompt to analyze
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Check prompt length
        if len(prompt) < 20:
            suggestions.append("Consider adding more context and details to the prompt")
        
        # Check for specificity
        vague_terms = ['something', 'anything', 'maybe', 'kind of', 'sort of']
        if any(term in prompt.lower() for term in vague_terms):
            suggestions.append("Replace vague terms with specific instructions")
        
        # Check for output format specification
        format_keywords = ['format', 'structure', 'json', 'markdown', 'list', 'table']
        if not any(kw in prompt.lower() for kw in format_keywords):
            suggestions.append("Consider specifying the desired output format")
        
        # Check for examples
        if 'example' not in prompt.lower():
            suggestions.append("Consider adding examples to clarify expectations")
        
        return suggestions
