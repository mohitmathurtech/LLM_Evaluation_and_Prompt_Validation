"""
Example usage of the LLM Evaluation Framework.

This script demonstrates the main features of the framework including
error categorization, validation, prompt management, and HITL feedback.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.evaluation.error_categorizer import ErrorCategorizer
from src.evaluation.validators import ResponseValidator
from src.evaluation.hitl_feedback import HITLFeedbackSystem, FeedbackType, QualityRating
from src.prompts.template_manager import PromptTemplateManager, PromptOptimizer


def demo_error_categorization():
    """Demonstrate error categorization functionality."""
    print("=" * 70)
    print("DEMO: Error Categorization")
    print("=" * 70)
    
    categorizer = ErrorCategorizer()
    
    # Example 1: Detect hallucination
    print("\n1. Detecting Hallucinations:")
    response1 = "I remember from my personal experience that Python was created in 1989."
    error = categorizer.detect_hallucination(response1, [])
    if error:
        print(f"   ✗ {error.error_type.value}: {error.description}")
    else:
        print("   ✓ No hallucination detected")
    
    # Example 2: Check factual accuracy
    print("\n2. Checking Factual Accuracy:")
    response2 = "The capital of France is Paris, which is a major European city."
    facts = {"capital of France": "Paris"}
    errors = categorizer.check_factual_accuracy(response2, facts)
    if errors:
        for err in errors:
            print(f"   ✗ {err.error_type.value}: {err.description}")
    else:
        print("   ✓ Factual accuracy confirmed")
    
    # Example 3: Evaluate reasoning
    print("\n3. Evaluating Reasoning Quality:")
    response3 = "We first analyze the data. Then identify patterns. Finally, draw conclusions."
    required_steps = ["analyze", "identify", "conclusions"]
    error = categorizer.evaluate_reasoning_quality(response3, required_steps)
    if error:
        print(f"   ✗ {error.error_type.value}: {error.description}")
    else:
        print("   ✓ Reasoning quality is adequate")
    
    # Show summary
    print("\n4. Error Summary:")
    summary = categorizer.get_error_summary()
    if summary:
        for error_type, count in summary.items():
            print(f"   - {error_type}: {count}")
    else:
        print("   No errors detected")


def demo_response_validation():
    """Demonstrate response validation functionality."""
    print("\n" + "=" * 70)
    print("DEMO: Response Validation")
    print("=" * 70)
    
    validator = ResponseValidator()
    
    response = """
    Quantum computing is a revolutionary technology that uses quantum mechanics principles.
    For example, it leverages superposition to process multiple states simultaneously.
    Therefore, quantum computers can solve certain problems much faster than classical computers.
    This technology has applications in cryptography, drug discovery, and optimization.
    """
    
    prompt = "Explain quantum computing"
    expected_elements = ["quantum", "technology", "applications"]
    
    print("\nValidating response...")
    result = validator.validate_response(response, prompt, expected_elements)
    
    print(f"\nValidation Status: {result.status.value}")
    print(f"Overall Score: {result.overall_score:.2f}/1.00")
    
    print("\nMetric Details:")
    for metric in result.metrics:
        status = "✓" if metric.passed else "✗"
        print(f"  {status} {metric.name}: {metric.score:.2f} (threshold: {metric.threshold})")
        print(f"     {metric.details}")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  ✗ {error}")


def demo_prompt_templates():
    """Demonstrate prompt template management."""
    print("\n" + "=" * 70)
    print("DEMO: Prompt Template Management")
    print("=" * 70)
    
    # Load templates
    examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    if os.path.exists(examples_dir):
        manager = PromptTemplateManager(template_dir=examples_dir)
        
        print("\nAvailable Templates:")
        templates = manager.list_templates()
        for template_name in templates:
            print(f"  - {template_name}")
        
        # Use a template
        if templates:
            template_name = templates[0]
            template = manager.get_template(template_name)
            print(f"\nUsing template: {template_name}")
            print(f"Description: {template.description}")
            print(f"Variables: {', '.join(template.variables)}")
    else:
        print("\nNo template directory found. Skipping template demo.")


def demo_prompt_optimization():
    """Demonstrate prompt optimization."""
    print("\n" + "=" * 70)
    print("DEMO: Prompt Optimization")
    print("=" * 70)
    
    optimizer = PromptOptimizer()
    
    original_prompt = "explain machine learning"
    
    print(f"\nOriginal Prompt:")
    print(f"  {original_prompt}")
    
    print(f"\nOptimized Prompt:")
    optimized = optimizer.optimize_prompt(original_prompt)
    print(f"  {optimized}")
    
    print(f"\nWith Constraints:")
    constrained = optimizer.add_constraints(
        original_prompt,
        ["Maximum 200 words", "Include at least 2 examples"]
    )
    print(f"  {constrained}")


def demo_hitl_feedback():
    """Demonstrate human-in-the-loop feedback system."""
    print("\n" + "=" * 70)
    print("DEMO: Human-in-the-Loop Feedback")
    print("=" * 70)
    
    hitl = HITLFeedbackSystem()
    
    # Create evaluation tasks
    print("\nCreating evaluation tasks...")
    task1 = hitl.create_evaluation_task(
        prompt="Explain quantum computing",
        response="Quantum computing uses quantum mechanics to process information..."
    )
    
    task2 = hitl.create_evaluation_task(
        prompt="What is machine learning?",
        response="Machine learning is a subset of AI that enables systems to learn..."
    )
    
    print(f"  Created task: {task1.task_id}")
    print(f"  Created task: {task2.task_id}")
    
    # Submit feedback
    print("\nSubmitting feedback...")
    hitl.submit_feedback(
        task_id=task1.task_id,
        evaluator_id="evaluator_1",
        feedback_type=FeedbackType.APPROVAL,
        quality_rating=QualityRating.EXCELLENT,
        comments="Clear and comprehensive explanation"
    )
    
    hitl.submit_feedback(
        task_id=task2.task_id,
        evaluator_id="evaluator_1",
        feedback_type=FeedbackType.MODIFICATION,
        quality_rating=QualityRating.GOOD,
        comments="Good but needs more examples",
        suggested_improvements=["Add concrete examples", "Improve clarity"]
    )
    
    # Get statistics
    print("\nFeedback Statistics:")
    stats = hitl.get_feedback_statistics()
    print(f"  Total Tasks: {stats['total_tasks']}")
    print(f"  Completed Tasks: {stats['completed_tasks']}")
    print(f"  Pending Tasks: {stats['pending_tasks']}")
    print(f"  Total Feedback: {stats['total_feedback']}")
    if stats.get('average_quality_rating'):
        print(f"  Average Quality Rating: {stats['average_quality_rating']:.2f}/5.00")
    
    print("\n  Feedback by Type:")
    for feedback_type, count in stats.get('feedback_by_type', {}).items():
        print(f"    - {feedback_type}: {count}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("LLM EVALUATION & PROMPT VALIDATION FRAMEWORK")
    print("Demonstration of Core Features")
    print("=" * 70)
    
    try:
        demo_error_categorization()
        demo_response_validation()
        demo_prompt_templates()
        demo_prompt_optimization()
        demo_hitl_feedback()
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nThe framework is ready to use!")
        print("Check the README.md for more detailed usage instructions.\n")
        
    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
