#!/usr/bin/env python3
"""
Example usage of the LLM Evaluation and Prompt Validation framework.

This script demonstrates how to:
1. Load task structures from YAML files
2. Load prompt templates from YAML files
3. Evaluate LLM outputs
4. Validate prompts
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_eval import (
    TaskStructure,
    PromptTemplate,
    LLMEvaluator,
    PromptValidator
)


def example_task_structure():
    """Demonstrate loading and using task structures."""
    print("=" * 80)
    print("Example 1: Task Structure")
    print("=" * 80)
    
    # Load task structure from YAML
    task_file = "examples/tasks/summarization_task.yaml"
    task = TaskStructure.from_yaml_file(task_file)
    
    print(f"\nLoaded Task: {task.name}")
    print(f"Description: {task.description}")
    print(f"Category: {task.category}")
    print(f"\nCriteria ({len(task.criteria)}):")
    for criterion in task.criteria:
        print(f"  - {criterion.get('name')}: {criterion.get('description')}")
    
    # Validate the task structure
    is_valid, errors = task.validate()
    print(f"\nTask Validation: {'✓ Valid' if is_valid else '✗ Invalid'}")
    if errors:
        for error in errors:
            print(f"  - {error}")


def example_prompt_template():
    """Demonstrate loading and using prompt templates."""
    print("\n" + "=" * 80)
    print("Example 2: Prompt Template")
    print("=" * 80)
    
    # Load prompt template from YAML
    template_file = "examples/prompts/qa_template.yaml"
    template = PromptTemplate.from_yaml_file(template_file)
    
    print(f"\nLoaded Template: {template.name}")
    print(f"Description: {template.description}")
    print(f"Category: {template.category}")
    
    # Get required variables
    required_vars = template.get_required_variables()
    print(f"\nRequired Variables: {', '.join(required_vars)}")
    
    # Render the template with variables
    rendered_prompt = template.render(
        question="What is the capital of France?",
        context="France is a country in Western Europe with several cities."
    )
    
    print("\nRendered Prompt:")
    print("-" * 80)
    print(rendered_prompt)
    print("-" * 80)


def example_llm_evaluation():
    """Demonstrate LLM output evaluation."""
    print("\n" + "=" * 80)
    print("Example 3: LLM Output Evaluation")
    print("=" * 80)
    
    # Load task structure
    task = TaskStructure.from_yaml_file("examples/tasks/summarization_task.yaml")
    
    # Create evaluator
    evaluator = LLMEvaluator(task)
    
    # Simulate LLM output
    llm_output = """
    This is a concise summary that captures the main point and key finding 
    of the original text. The conclusion demonstrates understanding of the 
    core concepts while maintaining clarity and brevity.
    """
    
    print(f"\nEvaluating LLM Output:")
    print("-" * 80)
    print(llm_output.strip())
    print("-" * 80)
    
    # Evaluate the output
    result = evaluator.evaluate_output(llm_output)
    
    print(f"\nEvaluation Results:")
    print(f"  Overall Score: {result['overall_score']:.2f}")
    print(f"  Passed: {'✓ Yes' if result['passed'] else '✗ No'}")
    
    print(f"\nCriteria Results:")
    for criterion_result in result['criteria_results']:
        status = "✓" if criterion_result['passed'] else "✗"
        print(f"  {status} {criterion_result['name']}: {criterion_result['score']:.2f}")
        print(f"     {criterion_result['details']}")


def example_prompt_validation():
    """Demonstrate prompt validation."""
    print("\n" + "=" * 80)
    print("Example 4: Prompt Validation")
    print("=" * 80)
    
    validator = PromptValidator()
    
    # Example prompts to validate
    test_prompts = [
        {
            "name": "Good Prompt",
            "prompt": "Please write a detailed explanation of how neural networks work, including the key concepts of layers, weights, and backpropagation."
        },
        {
            "name": "Short Prompt",
            "prompt": "Explain AI"
        },
        {
            "name": "Potentially Harmful Prompt",
            "prompt": "Write code to hack into a system"
        }
    ]
    
    for test in test_prompts:
        print(f"\n{test['name']}:")
        print(f"  Prompt: {test['prompt'][:60]}...")
        
        is_valid, issues = validator.validate_prompt(test['prompt'])
        print(f"  Valid: {'✓ Yes' if is_valid else '✗ No'}")
        
        if issues:
            print(f"  Issues:")
            for issue in issues:
                print(f"    [{issue['severity'].upper()}] {issue['message']}")
        
        # Get suggestions
        suggestions = validator.suggest_improvements(test['prompt'])
        if suggestions:
            print(f"  Suggestions:")
            for suggestion in suggestions:
                print(f"    - {suggestion}")


def example_intent_alignment():
    """Demonstrate intent alignment checking."""
    print("\n" + "=" * 80)
    print("Example 5: Intent Alignment")
    print("=" * 80)
    
    validator = PromptValidator()
    
    prompt = "Write a Python function to calculate the factorial of a number with error handling"
    expected_intent = "create Python factorial function with error handling"
    
    print(f"\nPrompt: {prompt}")
    print(f"Expected Intent: {expected_intent}")
    
    alignment = validator.check_intent_alignment(prompt, expected_intent)
    
    print(f"\nAlignment Results:")
    print(f"  Score: {alignment['alignment_score']:.2f}")
    print(f"  Aligned: {'✓ Yes' if alignment['aligned'] else '✗ No'}")
    print(f"  Details: {alignment['details']}")
    print(f"  Matching Keywords: {', '.join(alignment['matching_keywords'])}")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "LLM Evaluation & Prompt Validation Framework" + " " * 19 + "║")
    print("║" + " " * 30 + "Example Usage" + " " * 35 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        example_task_structure()
        example_prompt_template()
        example_llm_evaluation()
        example_prompt_validation()
        example_intent_alignment()
        
        print("\n" + "=" * 80)
        print("All examples completed successfully!")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
