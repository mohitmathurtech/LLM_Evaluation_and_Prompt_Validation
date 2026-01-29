"""
YAML Loader Module

Handles loading and validation of YAML configuration files for
task structures and prompt templates.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Union


class YAMLLoader:
    """Load and parse YAML files for LLM evaluation framework."""
    
    @staticmethod
    def load_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load a YAML file and return its contents as a dictionary.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Dictionary containing the parsed YAML content
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the file is not valid YAML
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                return data if data is not None else {}
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")
    
    @staticmethod
    def load_string(yaml_string: str) -> Dict[str, Any]:
        """
        Load YAML content from a string.
        
        Args:
            yaml_string: YAML content as a string
            
        Returns:
            Dictionary containing the parsed YAML content
            
        Raises:
            yaml.YAMLError: If the string is not valid YAML
        """
        try:
            data = yaml.safe_load(yaml_string)
            return data if data is not None else {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML string: {e}")
    
    @staticmethod
    def save_file(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
        """
        Save a dictionary to a YAML file.
        
        Args:
            data: Dictionary to save
            file_path: Path where to save the YAML file
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
