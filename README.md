# LLM Evaluation & Prompt Validation Framework

A comprehensive framework for evaluating Large Language Model (LLM) outputs and validating prompts to ensure high-quality, reliable AI-generated content.

## 🎯 Overview

This framework provides tools and methodologies to:
- **Detect hallucinations and factual errors** in LLM responses
- **Validate response quality** using structured schemas
- **Optimize prompts** for better instruction adherence
- **Implement human-in-the-loop (HITL)** evaluation workflows
- **Categorize errors** for systematic improvement
- **Manage prompt templates** using YAML-based configurations

## 🚀 Features

### 1. Error Categorization
- Automatic detection of hallucinations, factual errors, and reasoning gaps
- Severity-based classification (Critical, High, Medium, Low)
- Comprehensive error logging and reporting

### 2. Response Validation
- Multi-metric validation (clarity, completeness, reasoning depth, length)
- Customizable validation thresholds
- Schema-based validation for structured requirements

### 3. Prompt Template Management
- YAML-based template definitions
- Variable substitution and rendering
- Template categorization and tagging
- Easy template reuse across projects

### 4. Prompt Optimization
- Automatic prompt refinement strategies
- Clarity, specificity, and structure improvements
- Support for constraints and few-shot examples

### 5. Human-in-the-Loop Feedback
- Structured evaluation tasks
- Quality ratings and feedback collection
- Feedback aggregation and analytics
- Export capabilities for further analysis

## 📁 Project Structure

```
LLM_Evaluation_and_Prompt_Validation/
├── src/
│   ├── evaluation/
│   │   ├── error_categorizer.py    # Error detection and categorization
│   │   ├── validators.py            # Response validation schemas
│   │   └── hitl_feedback.py         # Human-in-the-loop system
│   ├── prompts/
│   │   └── template_manager.py      # YAML template management
│   └── utils/                        # Utility functions (future)
├── tests/
│   ├── test_error_categorizer.py
│   ├── test_validators.py
│   ├── test_template_manager.py
│   └── test_hitl_feedback.py
├── examples/
│   ├── summarization_prompt.yaml
│   ├── code_explanation_prompt.yaml
│   └── factual_qa_prompt.yaml
└── data/                             # Evaluation datasets (future)
```

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/mohitmathurtech/LLM_Evaluation_and_Prompt_Validation.git
cd LLM_Evaluation_and_Prompt_Validation

# Install dependencies
pip install pyyaml
```

## 📖 Quick Start

### Error Categorization

```python
from src.evaluation.error_categorizer import ErrorCategorizer

# Initialize the categorizer
categorizer = ErrorCategorizer()

# Detect hallucinations
response = "I remember seeing this in a previous conversation."
error = categorizer.detect_hallucination(response, facts=[])

# Check factual accuracy
response = "The capital of France is Paris."
reference_facts = {"capital of France": "Paris"}
errors = categorizer.check_factual_accuracy(response, reference_facts)

# Get error summary
summary = categorizer.get_error_summary()
print(summary)
```

### Response Validation

```python
from src.evaluation.validators import ResponseValidator

# Initialize validator
validator = ResponseValidator()

# Validate a response
response = "This is a clear explanation. For example, we can see..."
prompt = "Explain the concept"
expected_elements = ["explanation", "example"]

result = validator.validate_response(response, prompt, expected_elements)
print(f"Status: {result.status.value}")
print(f"Overall Score: {result.overall_score:.2f}")
```

### Prompt Template Management

```python
from src.prompts.template_manager import PromptTemplateManager

# Load templates from directory
manager = PromptTemplateManager(template_dir='examples')

# Get a template
template = manager.get_template('summarization_prompt')

# Render with variables
prompt = template.render(
    text="Long article text here...",
    max_length=100
)
print(prompt)
```

### Prompt Optimization

```python
from src.prompts.template_manager import PromptOptimizer

optimizer = PromptOptimizer()

# Optimize a prompt
original = "explain machine learning"
optimized = optimizer.optimize_prompt(original)
print(optimized)

# Add constraints
constrained = optimizer.add_constraints(
    original,
    ["Maximum 200 words", "Include examples"]
)
```

### Human-in-the-Loop Feedback

```python
from src.evaluation.hitl_feedback import HITLFeedbackSystem, FeedbackType, QualityRating

# Initialize HITL system
hitl = HITLFeedbackSystem()

# Create evaluation task
task = hitl.create_evaluation_task(
    prompt="Explain quantum computing",
    response="Quantum computing uses quantum mechanics..."
)

# Submit feedback
hitl.submit_feedback(
    task_id=task.task_id,
    evaluator_id="evaluator_1",
    feedback_type=FeedbackType.APPROVAL,
    quality_rating=QualityRating.GOOD,
    comments="Clear explanation"
)

# Get statistics
stats = hitl.get_feedback_statistics()
print(stats)

# Generate report
report = hitl.generate_feedback_report()
print(report)
```

## 🧪 Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_error_categorizer
python -m unittest tests.test_validators
python -m unittest tests.test_template_manager
python -m unittest tests.test_hitl_feedback
```

## 📝 YAML Template Format

Create prompt templates in YAML format:

```yaml
name: my_prompt_template
description: Description of what this prompt does
category: category_name
tags:
  - tag1
  - tag2
variables:
  - variable1
  - variable2
instructions:
  - Instruction 1
  - Must include specific requirement
template: |
  Your prompt text with {variable1} and {variable2}.
  
  Additional instructions here.
expected_output_format: Description of expected output
```

## 🎓 Use Cases

### 1. Content Quality Assurance
Validate AI-generated content for blogs, documentation, or reports.

### 2. Chatbot Response Evaluation
Ensure chatbot responses are accurate, clear, and helpful.

### 3. Code Generation Validation
Verify that AI-generated code explanations are correct and complete.

### 4. Educational Content Creation
Validate educational materials for accuracy and pedagogical quality.

### 5. Research and Development
Benchmark different prompts and models for optimal performance.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open-source. Please check the LICENSE file for details.

## 🔗 Links

- **Repository**: https://github.com/mohitmathurtech/LLM_Evaluation_and_Prompt_Validation
- **Issues**: https://github.com/mohitmathurtech/LLM_Evaluation_and_Prompt_Validation/issues

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for the AI Engineering community**