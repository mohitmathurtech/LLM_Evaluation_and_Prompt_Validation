"""
Unit tests for Prompt Template Manager module.

Tests the YAML template loading and prompt optimization functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tempfile
import yaml
from pathlib import Path
from src.prompts.template_manager import (
    PromptTemplate,
    PromptTemplateManager,
    PromptOptimizer
)


class TestPromptTemplate(unittest.TestCase):
    """Test cases for PromptTemplate class."""
    
    def test_render_template(self):
        """Test rendering a template with variables."""
        template = PromptTemplate(
            name="test",
            description="Test template",
            template="Hello {name}, you are {age} years old.",
            variables=["name", "age"]
        )
        
        rendered = template.render(name="Alice", age=25)
        
        self.assertEqual(rendered, "Hello Alice, you are 25 years old.")
    
    def test_validate_variables_complete(self):
        """Test variable validation with all variables provided."""
        template = PromptTemplate(
            name="test",
            description="Test",
            template="Test",
            variables=["var1", "var2"]
        )
        
        missing = template.validate_variables(var1="a", var2="b")
        
        self.assertEqual(len(missing), 0)
    
    def test_validate_variables_missing(self):
        """Test variable validation with missing variables."""
        template = PromptTemplate(
            name="test",
            description="Test",
            template="Test",
            variables=["var1", "var2", "var3"]
        )
        
        missing = template.validate_variables(var1="a")
        
        self.assertEqual(len(missing), 2)
        self.assertIn("var2", missing)
        self.assertIn("var3", missing)


class TestPromptTemplateManager(unittest.TestCase):
    """Test cases for PromptTemplateManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = PromptTemplateManager()
    
    def test_register_template(self):
        """Test registering a template."""
        template = PromptTemplate(
            name="test_template",
            description="Test",
            template="Test content"
        )
        
        self.manager.register_template(template)
        
        retrieved = self.manager.get_template("test_template")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "test_template")
    
    def test_get_template_nonexistent(self):
        """Test retrieving a non-existent template."""
        result = self.manager.get_template("nonexistent")
        
        self.assertIsNone(result)
    
    def test_list_templates(self):
        """Test listing all templates."""
        template1 = PromptTemplate(name="test1", description="", template="")
        template2 = PromptTemplate(name="test2", description="", template="")
        
        self.manager.register_template(template1)
        self.manager.register_template(template2)
        
        templates = self.manager.list_templates()
        
        self.assertIn("test1", templates)
        self.assertIn("test2", templates)
    
    def test_list_templates_by_category(self):
        """Test listing templates filtered by category."""
        template1 = PromptTemplate(name="t1", description="", template="", category="cat1")
        template2 = PromptTemplate(name="t2", description="", template="", category="cat2")
        template3 = PromptTemplate(name="t3", description="", template="", category="cat1")
        
        self.manager.register_template(template1)
        self.manager.register_template(template2)
        self.manager.register_template(template3)
        
        cat1_templates = self.manager.list_templates(category="cat1")
        
        self.assertEqual(len(cat1_templates), 2)
        self.assertIn("t1", cat1_templates)
        self.assertIn("t3", cat1_templates)
    
    def test_load_template_from_yaml(self):
        """Test loading a template from YAML file."""
        yaml_content = {
            'name': 'test_yaml',
            'description': 'Test YAML template',
            'template': 'Hello {name}',
            'variables': ['name'],
            'category': 'test'
        }
        
        yaml_path = os.path.join(self.temp_dir, 'test.yaml')
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_content, f)
        
        template = self.manager.load_template_from_yaml(yaml_path)
        
        self.assertEqual(template.name, 'test_yaml')
        self.assertIn('name', template.variables)
    
    def test_save_template_to_yaml(self):
        """Test saving a template to YAML file."""
        template = PromptTemplate(
            name="save_test",
            description="Test saving",
            template="Content {var}",
            variables=["var"],
            category="test"
        )
        
        self.manager.register_template(template)
        
        yaml_path = os.path.join(self.temp_dir, 'saved.yaml')
        self.manager.save_template_to_yaml("save_test", yaml_path)
        
        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(yaml_path))
        
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        self.assertEqual(data['name'], 'save_test')
        self.assertIn('var', data['variables'])


class TestPromptOptimizer(unittest.TestCase):
    """Test cases for PromptOptimizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = PromptOptimizer()
    
    def test_improve_clarity(self):
        """Test clarity improvement."""
        prompt = "explain this concept"
        
        improved = self.optimizer._improve_clarity(prompt)
        
        self.assertIn("Please", improved)
    
    def test_improve_specificity(self):
        """Test specificity improvement."""
        prompt = "Tell me about dogs"
        
        improved = self.optimizer._improve_specificity(prompt)
        
        self.assertTrue(
            any(word in improved.lower() 
                for word in ['specific', 'detailed', 'precise'])
        )
    
    def test_improve_structure(self):
        """Test structure improvement."""
        prompt = "What is machine learning"
        
        improved = self.optimizer._improve_structure(prompt)
        
        self.assertIn("structure", improved.lower())
    
    def test_optimize_prompt_all_strategies(self):
        """Test optimizing with all strategies."""
        prompt = "explain"
        
        optimized = self.optimizer.optimize_prompt(prompt)
        
        # Should have improvements from all strategies
        self.assertNotEqual(prompt, optimized)
        self.assertGreater(len(optimized), len(prompt))
    
    def test_optimize_prompt_specific_strategies(self):
        """Test optimizing with specific strategies."""
        prompt = "explain this"
        
        optimized = self.optimizer.optimize_prompt(
            prompt, 
            strategies=['clarity']
        )
        
        self.assertIn("Please", optimized)
    
    def test_add_constraints(self):
        """Test adding constraints to prompt."""
        prompt = "Write a story"
        constraints = ["Maximum 100 words", "Include a twist ending"]
        
        result = self.optimizer.add_constraints(prompt, constraints)
        
        self.assertIn("Constraints:", result)
        self.assertIn("Maximum 100 words", result)
        self.assertIn("Include a twist ending", result)
    
    def test_add_examples(self):
        """Test adding examples to prompt."""
        prompt = "Classify sentiment"
        examples = [
            {"input": "I love this!", "output": "Positive"},
            {"input": "This is terrible", "output": "Negative"}
        ]
        
        result = self.optimizer.add_examples(prompt, examples)
        
        self.assertIn("Examples:", result)
        self.assertIn("I love this!", result)
        self.assertIn("Positive", result)


if __name__ == '__main__':
    unittest.main()
