"""
Prompt Template Module

Manages prompt templates loaded from YAML files.
Templates define reusable prompt structures for LLM interactions.
"""

from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from .yaml_loader import YAMLLoader


class PromptTemplate:
    """
    Represents a prompt template for LLM interactions.
    
    Prompt templates are defined in YAML and contain:
    - Template metadata (id, name, description)
    - Template structure (system, user, assistant messages)
    - Variables for customization
    - Usage examples
    """
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a prompt template from a dictionary.
        
        Args:
            data: Dictionary containing prompt template data
        """
        self.template_id = data.get('template_id', '')
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.category = data.get('category', 'general')
        self.system_prompt = data.get('system_prompt', '')
        self.user_template = data.get('user_template', '')
        self.variables = data.get('variables', [])
        self.examples = data.get('examples', [])
        self._raw_data = data
    
    @classmethod
    def from_yaml_file(cls, file_path: str) -> 'PromptTemplate':
        """
        Load a prompt template from a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            PromptTemplate instance
        """
        data = YAMLLoader.load_file(file_path)
        return cls(data)
    
    @classmethod
    def from_yaml_string(cls, yaml_string: str) -> 'PromptTemplate':
        """
        Load a prompt template from a YAML string.
        
        Args:
            yaml_string: YAML content as a string
            
        Returns:
            PromptTemplate instance
        """
        data = YAMLLoader.load_string(yaml_string)
        return cls(data)
    
    def render(self, **kwargs) -> str:
        """
        Render the user template with provided variables.
        
        Args:
            **kwargs: Variable values to substitute in the template
            
        Returns:
            Rendered prompt string
        """
        try:
            return self.user_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {e}")
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the prompt template.
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        if not self.template_id:
            errors.append("Template ID is required")
        
        if not self.name:
            errors.append("Template name is required")
        
        if not self.description:
            errors.append("Template description is required")
        
        if not self.user_template:
            errors.append("User template is required")
        
        return len(errors) == 0, errors
    
    def get_required_variables(self) -> List[str]:
        """
        Extract required variables from the user template.
        
        Returns:
            List of variable names
        """
        import re
        pattern = r'\{(\w+)\}'
        return list(set(re.findall(pattern, self.user_template)))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the prompt template to a dictionary.
        
        Returns:
            Dictionary representation of the prompt template
        """
        return {
            'template_id': self.template_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'system_prompt': self.system_prompt,
            'user_template': self.user_template,
            'variables': self.variables,
            'examples': self.examples
        }
    
    def save_to_yaml(self, file_path: str) -> None:
        """
        Save the prompt template to a YAML file.
        
        Args:
            file_path: Path where to save the YAML file
        """
        YAMLLoader.save_file(self.to_dict(), file_path)
