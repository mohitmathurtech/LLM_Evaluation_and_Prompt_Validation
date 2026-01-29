"""
Prompt Template Manager for LLM Evaluation Framework.

This module manages YAML-based prompt templates and provides utilities
for loading, validating, and using prompt templates.
"""

import yaml
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class PromptTemplate:
    """Represents a prompt template."""
    name: str
    description: str
    template: str
    variables: List[str] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    expected_output_format: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    def render(self, **kwargs) -> str:
        """
        Render the template with provided variables.
        
        Args:
            **kwargs: Variable values to substitute in template
            
        Returns:
            Rendered prompt string
        """
        rendered = self.template
        for var in self.variables:
            if var in kwargs:
                rendered = rendered.replace(f"{{{var}}}", str(kwargs[var]))
        return rendered
    
    def validate_variables(self, **kwargs) -> List[str]:
        """
        Validate that all required variables are provided.
        
        Returns:
            List of missing variable names
        """
        return [var for var in self.variables if var not in kwargs]


class PromptTemplateManager:
    """
    Manages prompt templates from YAML files.
    
    This class provides functionality to load, store, and retrieve
    prompt templates defined in YAML format.
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the template manager.
        
        Args:
            template_dir: Directory containing template YAML files
        """
        self.templates: Dict[str, PromptTemplate] = {}
        self.template_dir = template_dir
        
        if template_dir:
            self.load_templates_from_directory(template_dir)
    
    def load_template_from_yaml(self, yaml_path: str) -> PromptTemplate:
        """
        Load a prompt template from a YAML file.
        
        Args:
            yaml_path: Path to the YAML file
            
        Returns:
            PromptTemplate object
        """
        with open(yaml_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
        
        template = PromptTemplate(
            name=data.get('name', 'unnamed'),
            description=data.get('description', ''),
            template=data.get('template', ''),
            variables=data.get('variables', []),
            instructions=data.get('instructions', []),
            expected_output_format=data.get('expected_output_format'),
            category=data.get('category'),
            tags=data.get('tags', [])
        )
        
        self.templates[template.name] = template
        return template
    
    def load_templates_from_directory(self, directory: str):
        """
        Load all YAML templates from a directory.
        
        Args:
            directory: Path to directory containing YAML files
        """
        template_path = Path(directory)
        if not template_path.exists():
            return
        
        for yaml_file in template_path.glob('*.yaml'):
            try:
                self.load_template_from_yaml(str(yaml_file))
            except (FileNotFoundError, yaml.YAMLError) as e:
                logger.warning(f"Error loading template from {yaml_file}: {e}")
        
        for yml_file in template_path.glob('*.yml'):
            try:
                self.load_template_from_yaml(str(yml_file))
            except (FileNotFoundError, yaml.YAMLError) as e:
                logger.warning(f"Error loading template from {yml_file}: {e}")
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        Retrieve a template by name.
        
        Args:
            name: Name of the template
            
        Returns:
            PromptTemplate object or None if not found
        """
        return self.templates.get(name)
    
    def list_templates(self, category: Optional[str] = None) -> List[str]:
        """
        List all available template names.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of template names
        """
        if category:
            return [
                name for name, template in self.templates.items()
                if template.category == category
            ]
        return list(self.templates.keys())
    
    def register_template(self, template: PromptTemplate):
        """
        Register a new template.
        
        Args:
            template: PromptTemplate object to register
        """
        self.templates[template.name] = template
    
    def save_template_to_yaml(self, template_name: str, output_path: str):
        """
        Save a template to a YAML file.
        
        Args:
            template_name: Name of the template to save
            output_path: Path where to save the YAML file
        """
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        data = {
            'name': template.name,
            'description': template.description,
            'template': template.template,
            'variables': template.variables,
            'instructions': template.instructions,
            'expected_output_format': template.expected_output_format,
            'category': template.category,
            'tags': template.tags
        }
        
        with open(output_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False, sort_keys=False)


class PromptOptimizer:
    """
    Optimizes prompts for better instruction adherence.
    
    This class provides utilities to refine and improve prompts
    to achieve better results from LLMs.
    """
    
    def __init__(self):
        self.optimization_strategies = {
            'clarity': self._improve_clarity,
            'specificity': self._improve_specificity,
            'structure': self._improve_structure,
        }
    
    def optimize_prompt(
        self,
        prompt: str,
        strategies: Optional[List[str]] = None
    ) -> str:
        """
        Optimize a prompt using specified strategies.
        
        Args:
            prompt: Original prompt text
            strategies: List of optimization strategies to apply
            
        Returns:
            Optimized prompt string
        """
        if strategies is None:
            strategies = list(self.optimization_strategies.keys())
        
        optimized = prompt
        for strategy in strategies:
            if strategy in self.optimization_strategies:
                optimized = self.optimization_strategies[strategy](optimized)
        
        return optimized
    
    def _improve_clarity(self, prompt: str) -> str:
        """Improve prompt clarity by adding explicit instructions."""
        if not prompt.strip().endswith('.'):
            prompt = prompt.strip() + '.'
        
        # Add clarity markers if not present
        clarity_markers = [
            'Please', 'Explain', 'Describe', 'Provide', 'List'
        ]
        if not any(marker in prompt for marker in clarity_markers):
            prompt = "Please " + prompt[0].lower() + prompt[1:]
        
        return prompt
    
    def _improve_specificity(self, prompt: str) -> str:
        """Improve prompt specificity by encouraging detailed responses."""
        specificity_phrases = [
            'specific', 'detailed', 'precise', 'exact', 'concrete'
        ]
        
        if not any(phrase in prompt.lower() for phrase in specificity_phrases):
            # Add specificity request
            prompt = prompt.strip()
            if prompt.endswith('.'):
                prompt = prompt[:-1]
            prompt += " Please be specific and provide detailed information."
        
        return prompt
    
    def _improve_structure(self, prompt: str) -> str:
        """Improve prompt structure by adding format requirements."""
        structure_keywords = [
            'format', 'structure', 'organize', 'step-by-step'
        ]
        
        if not any(keyword in prompt.lower() for keyword in structure_keywords):
            prompt = prompt.strip()
            if prompt.endswith('.'):
                prompt = prompt[:-1]
            prompt += " Please structure your response clearly."
        
        return prompt
    
    def add_constraints(
        self,
        prompt: str,
        constraints: List[str]
    ) -> str:
        """
        Add constraints to a prompt.
        
        Args:
            prompt: Original prompt
            constraints: List of constraint strings
            
        Returns:
            Prompt with constraints added
        """
        prompt = prompt.strip()
        
        if constraints:
            prompt += "\n\nConstraints:\n"
            for i, constraint in enumerate(constraints, 1):
                prompt += f"{i}. {constraint}\n"
        
        return prompt
    
    def add_examples(
        self,
        prompt: str,
        examples: List[Dict[str, str]]
    ) -> str:
        """
        Add examples to a prompt for few-shot learning.
        
        Args:
            prompt: Original prompt
            examples: List of example dictionaries with 'input' and 'output'
            
        Returns:
            Prompt with examples added
        """
        prompt = prompt.strip()
        
        if examples:
            prompt += "\n\nExamples:\n"
            for i, example in enumerate(examples, 1):
                prompt += f"\nExample {i}:\n"
                prompt += f"Input: {example.get('input', '')}\n"
                prompt += f"Output: {example.get('output', '')}\n"
        
        return prompt
