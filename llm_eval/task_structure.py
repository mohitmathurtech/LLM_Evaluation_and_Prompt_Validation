"""
Task Structure Module

Defines and manages task structures loaded from YAML files.
Tasks represent evaluation scenarios for LLM outputs.
"""

from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from .yaml_loader import YAMLLoader


class TaskStructure:
    """
    Represents a task structure for LLM evaluation.
    
    Task structures are defined in YAML and contain:
    - Task metadata (id, name, description)
    - Expected output criteria
    - Evaluation metrics
    - Test cases
    """
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a task structure from a dictionary.
        
        Args:
            data: Dictionary containing task structure data
        """
        self.task_id = data.get('task_id', '')
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.category = data.get('category', 'general')
        self.criteria = data.get('criteria', [])
        self.metrics = data.get('metrics', [])
        self.test_cases = data.get('test_cases', [])
        self._raw_data = data
    
    @classmethod
    def from_yaml_file(cls, file_path: str) -> 'TaskStructure':
        """
        Load a task structure from a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            TaskStructure instance
        """
        data = YAMLLoader.load_file(file_path)
        return cls(data)
    
    @classmethod
    def from_yaml_string(cls, yaml_string: str) -> 'TaskStructure':
        """
        Load a task structure from a YAML string.
        
        Args:
            yaml_string: YAML content as a string
            
        Returns:
            TaskStructure instance
        """
        data = YAMLLoader.load_string(yaml_string)
        return cls(data)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the task structure.
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        if not self.task_id:
            errors.append("Task ID is required")
        
        if not self.name:
            errors.append("Task name is required")
        
        if not self.description:
            errors.append("Task description is required")
        
        if not self.criteria:
            errors.append("At least one criterion is required")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task structure to a dictionary.
        
        Returns:
            Dictionary representation of the task structure
        """
        return {
            'task_id': self.task_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'criteria': self.criteria,
            'metrics': self.metrics,
            'test_cases': self.test_cases
        }
    
    def save_to_yaml(self, file_path: str) -> None:
        """
        Save the task structure to a YAML file.
        
        Args:
            file_path: Path where to save the YAML file
        """
        YAMLLoader.save_file(self.to_dict(), file_path)
