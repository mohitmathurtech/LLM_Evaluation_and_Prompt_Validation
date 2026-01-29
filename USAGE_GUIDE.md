# LLM Evaluation Framework - Detailed Usage Guide

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Error Categorization](#error-categorization)
3. [Response Validation](#response-validation)
4. [Prompt Template Management](#prompt-template-management)
5. [Prompt Optimization](#prompt-optimization)
6. [Human-in-the-Loop Feedback](#human-in-the-loop-feedback)
7. [Best Practices](#best-practices)
8. [Advanced Usage](#advanced-usage)

## Core Concepts

### Error Types
The framework categorizes errors into the following types:
- **HALLUCINATION**: LLM generates false information not grounded in facts
- **FACTUAL_ERROR**: Incorrect factual statements
- **REASONING_GAP**: Missing logical steps in reasoning
- **INSTRUCTION_DEVIATION**: Failure to follow given instructions
- **CLARITY_ISSUE**: Poor readability or unclear expression
- **INCOMPLETE_RESPONSE**: Missing required components
- **BIAS_DETECTED**: Biased or unfair content
- **UNSAFE_CONTENT**: Potentially harmful content

### Severity Levels
- **CRITICAL**: Must be fixed immediately
- **HIGH**: Should be addressed before deployment
- **MEDIUM**: Should be improved but not blocking
- **LOW**: Nice to have improvements

## Error Categorization

### Detecting Hallucinations

```python
from src.evaluation.error_categorizer import ErrorCategorizer

categorizer = ErrorCategorizer()

# Example: Detect personal references (common hallucination indicator)
response = "I remember seeing this product last year."
error = categorizer.detect_hallucination(response, facts=[])

if error:
    print(f"Error Type: {error.error_type.value}")
    print(f"Severity: {error.severity.value}")
    print(f"Description: {error.description}")
    print(f"Suggested Fix: {error.suggested_fix}")
```

### Checking Factual Accuracy

```python
# Define reference facts
reference_facts = {
    "capital of France": "Paris",
    "population of Tokyo": "14 million"
}

response = "The capital of France is Paris and has a population of over 2 million."

errors = categorizer.check_factual_accuracy(response, reference_facts)

for error in errors:
    print(f"Factual Error: {error.description}")
    print(f"Evidence: {error.evidence}")
```

### Evaluating Reasoning Quality

```python
# Define required reasoning steps
required_steps = [
    "identify the problem",
    "analyze the data",
    "propose a solution"
]

response = """
First, we identify the problem by examining user feedback.
Next, we analyze the data to understand patterns.
Finally, we propose a solution based on our findings.
"""

error = categorizer.evaluate_reasoning_quality(response, required_steps)

if error:
    print(f"Missing steps: {error.description}")
else:
    print("All reasoning steps are present")
```

## Response Validation

### Basic Validation

```python
from src.evaluation.validators import ResponseValidator, ValidationStatus

validator = ResponseValidator()

response = "Your LLM-generated response here..."
prompt = "Your original prompt"
expected_elements = ["element1", "element2", "element3"]

result = validator.validate_response(response, prompt, expected_elements)

print(f"Status: {result.status.value}")
print(f"Overall Score: {result.overall_score:.2f}")

for metric in result.metrics:
    print(f"{metric.name}: {metric.score:.2f} ({'PASS' if metric.passed else 'FAIL'})")
```

### Custom Configuration

```python
# Create validator with custom thresholds
config = {
    "min_clarity_score": 0.8,
    "min_completeness_score": 0.9,
    "min_reasoning_depth": 0.7,
    "max_response_length": 1000,
    "min_response_length": 100,
}

validator = ResponseValidator(config=config)
```

### Schema-Based Validation

```python
from src.evaluation.validators import SchemaValidator

schema_validator = SchemaValidator()

# Register a schema
schema = {
    "required_fields": ["title", "description", "examples"],
    "format_requirements": {
        "has_code_block": r"```[\s\S]*?```",
        "has_bullet_points": r"[-*]\s+"
    }
}

schema_validator.register_schema("documentation_schema", schema)

# Validate against schema
response = "Your documentation content here..."
result = schema_validator.validate_against_schema(response, "documentation_schema")

if result.status == ValidationStatus.FAILED:
    print("Validation failed:")
    for error in result.errors:
        print(f"  - {error}")
```

## Prompt Template Management

### Creating Templates in YAML

```yaml
name: question_answering
description: Template for answering questions with context
category: qa
tags:
  - question-answering
  - factual
variables:
  - question
  - context
instructions:
  - Answer based only on context
  - Must include citations
  - Do not make assumptions
template: |
  Based on the following context, please answer the question.
  
  Context:
  {context}
  
  Question: {question}
  
  Provide a clear answer with references to the context.
expected_output_format: Answer with citations
```

### Using Templates in Python

```python
from src.prompts.template_manager import PromptTemplateManager

# Load templates from directory
manager = PromptTemplateManager(template_dir='examples')

# Get a template
template = manager.get_template('question_answering')

# Check required variables
missing = template.validate_variables(question="What is AI?")
if missing:
    print(f"Missing variables: {missing}")

# Render the template
prompt = template.render(
    question="What is machine learning?",
    context="Machine learning is a subset of AI..."
)

print(prompt)
```

### Creating Templates Programmatically

```python
from src.prompts.template_manager import PromptTemplate

template = PromptTemplate(
    name="custom_template",
    description="Custom template for specific task",
    template="Please {action} the following {item}: {content}",
    variables=["action", "item", "content"],
    instructions=["Be specific", "Must include examples"],
    category="custom"
)

# Register with manager
manager.register_template(template)

# Save to file
manager.save_template_to_yaml("custom_template", "my_template.yaml")
```

## Prompt Optimization

### Automatic Optimization

```python
from src.prompts.template_manager import PromptOptimizer

optimizer = PromptOptimizer()

# Original prompt
prompt = "explain deep learning"

# Apply all optimization strategies
optimized = optimizer.optimize_prompt(prompt)
print(f"Optimized: {optimized}")

# Apply specific strategies
optimized = optimizer.optimize_prompt(
    prompt,
    strategies=['clarity', 'specificity']
)
```

### Adding Constraints

```python
# Add constraints to guide the response
constrained_prompt = optimizer.add_constraints(
    prompt="Explain neural networks",
    constraints=[
        "Maximum 300 words",
        "Include at least 2 examples",
        "Use simple language for beginners",
        "Include a diagram description"
    ]
)
```

### Few-Shot Learning

```python
# Add examples for few-shot learning
examples = [
    {
        "input": "What is supervised learning?",
        "output": "Supervised learning is a type of machine learning where the algorithm learns from labeled training data..."
    },
    {
        "input": "What is unsupervised learning?",
        "output": "Unsupervised learning is a type of machine learning where the algorithm learns patterns from unlabeled data..."
    }
]

prompt_with_examples = optimizer.add_examples(
    prompt="What is reinforcement learning?",
    examples=examples
)
```

## Human-in-the-Loop Feedback

### Setting Up HITL System

```python
from src.evaluation.hitl_feedback import (
    HITLFeedbackSystem,
    FeedbackType,
    QualityRating
)

# Initialize the system
hitl = HITLFeedbackSystem()

# Create evaluation task
task = hitl.create_evaluation_task(
    prompt="Explain quantum computing",
    response="LLM-generated response here...",
    context={"model": "gpt-4", "temperature": 0.7},
    auto_validation_results={"score": 0.85}
)

print(f"Task created: {task.task_id}")
```

### Submitting Feedback

```python
# Approve a response
hitl.submit_feedback(
    task_id=task.task_id,
    evaluator_id="evaluator_john",
    feedback_type=FeedbackType.APPROVAL,
    quality_rating=QualityRating.EXCELLENT,
    comments="Clear and accurate explanation",
    tags=["accurate", "clear"]
)

# Request modifications
hitl.submit_feedback(
    task_id=task.task_id,
    evaluator_id="evaluator_jane",
    feedback_type=FeedbackType.MODIFICATION,
    quality_rating=QualityRating.GOOD,
    comments="Good but needs more examples",
    suggested_improvements=[
        "Add concrete examples",
        "Simplify technical jargon",
        "Include visual descriptions"
    ],
    tags=["needs-examples"]
)

# Reject a response
hitl.submit_feedback(
    task_id=task.task_id,
    evaluator_id="evaluator_bob",
    feedback_type=FeedbackType.REJECTION,
    quality_rating=QualityRating.POOR,
    comments="Contains factual errors",
    suggested_improvements=["Fix factual errors", "Cite sources"],
    tags=["factual-error"]
)
```

### Analyzing Feedback

```python
# Get statistics
stats = hitl.get_feedback_statistics()
print(f"Total tasks: {stats['total_tasks']}")
print(f"Average rating: {stats['average_quality_rating']:.2f}")

# Get pending tasks
pending = hitl.get_pending_tasks()
print(f"Tasks awaiting review: {len(pending)}")

# Generate report
report = hitl.generate_feedback_report()
print(report)

# Export data
hitl.export_feedback_data("feedback_data.json")
```

### Feedback Aggregation

```python
from src.evaluation.hitl_feedback import FeedbackAggregator

aggregator = FeedbackAggregator()

# Add feedback from multiple evaluators
for task in hitl.get_completed_tasks():
    for feedback in task.human_feedback:
        aggregator.add_feedback(feedback)

# Get common issues
common_issues = aggregator.get_common_issues(top_n=5)
print("Most common issues:")
for issue in common_issues:
    print(f"  - {issue}")

# Get consensus rating
consensus = aggregator.get_consensus_rating()
print(f"Consensus rating: {consensus:.2f}/5.00")
```

## Best Practices

### 1. Error Detection
- Run error detection immediately after LLM generation
- Log all errors for pattern analysis
- Use error severity to prioritize fixes

### 2. Response Validation
- Define clear expected elements before validation
- Use custom thresholds based on your use case
- Validate in development, not just production

### 3. Prompt Templates
- Use descriptive names and categories
- Document all variables and instructions
- Version control your YAML templates
- Test templates with various inputs

### 4. Prompt Optimization
- Start with basic prompts, then optimize
- Test optimization strategies separately
- Use constraints for complex requirements
- Include examples for consistent outputs

### 5. HITL Feedback
- Get feedback from multiple evaluators
- Track feedback trends over time
- Act on common improvement suggestions
- Export data for further analysis

## Advanced Usage

### Combining Components

```python
# Complete evaluation pipeline
def evaluate_llm_response(prompt, response):
    # 1. Error categorization
    categorizer = ErrorCategorizer()
    hallucination = categorizer.detect_hallucination(response, facts=[])
    clarity = categorizer.assess_clarity(response)
    
    # 2. Response validation
    validator = ResponseValidator()
    validation_result = validator.validate_response(
        response, prompt, expected_elements=[]
    )
    
    # 3. Create HITL task if needed
    if validation_result.overall_score < 0.8 or hallucination:
        hitl = HITLFeedbackSystem()
        task = hitl.create_evaluation_task(
            prompt=prompt,
            response=response,
            auto_validation_results={
                "score": validation_result.overall_score,
                "errors": len(categorizer.error_log)
            }
        )
        return {"status": "needs_review", "task_id": task.task_id}
    
    return {"status": "approved", "score": validation_result.overall_score}

# Usage
result = evaluate_llm_response(
    prompt="Explain quantum computing",
    response="Quantum computing uses quantum bits..."
)

print(result)
```

### Batch Processing

```python
# Process multiple responses
responses = [
    {"prompt": "What is AI?", "response": "AI is..."},
    {"prompt": "What is ML?", "response": "ML is..."},
    # ... more responses
]

validator = ResponseValidator()
results = []

for item in responses:
    result = validator.validate_response(
        item["response"],
        item["prompt"],
        expected_elements=[]
    )
    results.append({
        "prompt": item["prompt"],
        "score": result.overall_score,
        "status": result.status.value
    })

# Analyze batch results
avg_score = sum(r["score"] for r in results) / len(results)
print(f"Average score: {avg_score:.2f}")
```

## Troubleshooting

### Common Issues

1. **Template not found**: Ensure YAML files are in the correct directory
2. **Missing variables**: Check template.validate_variables() before rendering
3. **Low validation scores**: Adjust thresholds in validator config
4. **Import errors**: Ensure all __init__.py files exist in directories

### Getting Help

- Check the examples in `examples/demo_usage.py`
- Review test files in `tests/` for usage patterns
- Open an issue on GitHub for support

---

**Last Updated**: January 2026
**Version**: 1.0.0
