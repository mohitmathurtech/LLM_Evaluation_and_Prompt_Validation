"""
LLM Evaluation and Prompt Validation Framework

A framework to evaluate and improve Large Language Model (LLM) outputs.
The system reviews AI-generated prompts and responses to verify correctness,
reasoning depth, and user intent alignment.
"""

__version__ = "0.1.0"

from .yaml_loader import YAMLLoader
from .task_structure import TaskStructure
from .prompt_template import PromptTemplate
from .evaluator import LLMEvaluator
from .validator import PromptValidator

__all__ = [
    "YAMLLoader",
    "TaskStructure",
    "PromptTemplate",
    "LLMEvaluator",
    "PromptValidator",
]
