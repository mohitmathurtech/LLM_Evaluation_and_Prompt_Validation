# LLM Evaluation and Prompt Validation Framework

A framework to evaluate and improve Large Language Model (LLM) outputs. The system reviews AI-generated prompts and responses to verify correctness, reasoning depth, and user intent alignment.

## Overview

This framework provides tools for:
- **Task Structure Definition**: Define evaluation tasks using YAML configuration files
- **Prompt Template Management**: Create reusable prompt templates with variable substitution
- **LLM Output Evaluation**: Assess LLM outputs against defined criteria and metrics
- **Prompt Validation**: Validate prompts for quality, clarity, and safety
- **Intent Alignment**: Check if prompts align with expected user intent

## Technical Stack

- **Python 3.7+**
- **YAML**: For defining task structures and prompt templates
- **PyYAML**: YAML parsing library
- **JSONSchema**: For validation support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mohitmathurtech/LLM_Evaluation_and_Prompt_Validation.git
cd LLM_Evaluation_and_Prompt_Validation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Task Structures

Define evaluation tasks in YAML format:

```yaml
# examples/tasks/summarization_task.yaml
task_id: task_001
name: Text Summarization Quality
description: Evaluate the quality of text summarization outputs
category: summarization

criteria:
  - name: conciseness
    type: length
    min_length: 50
    max_length: 300
    weight: 0.3
    description: Summary should be concise and within length limits

metrics:
  - name: word_count
    description: Number of words in the summary
```

Load and use task structures in Python:

```python
from llm_eval import TaskStructure

# Load from YAML file
task = TaskStructure.from_yaml_file("examples/tasks/summarization_task.yaml")

# Validate the task structure
is_valid, errors = task.validate()
print(f"Task is valid: {is_valid}")
```

### 2. Prompt Templates

Create reusable prompt templates in YAML:

```yaml
# examples/prompts/qa_template.yaml
template_id: template_001
name: Question Answering Template
description: Template for generating question-answering prompts
category: qa

system_prompt: |
  You are a helpful AI assistant that provides accurate answers.

user_template: |
  Please answer the following question:
  
  Question: {question}
  Context: {context}

variables:
  - name: question
    type: string
    required: true
  - name: context
    type: string
    required: true
```

Use prompt templates in Python:

```python
from llm_eval import PromptTemplate

# Load template from YAML
template = PromptTemplate.from_yaml_file("examples/prompts/qa_template.yaml")

# Render the template with variables
prompt = template.render(
    question="What is machine learning?",
    context="Machine learning is a subset of AI..."
)
```

### 3. Evaluate LLM Outputs

Evaluate LLM-generated content against task criteria:

```python
from llm_eval import TaskStructure, LLMEvaluator

# Load task structure
task = TaskStructure.from_yaml_file("examples/tasks/summarization_task.yaml")

# Create evaluator
evaluator = LLMEvaluator(task)

# Evaluate LLM output
llm_output = "This is a concise summary capturing the main points..."
result = evaluator.evaluate_output(llm_output)

print(f"Score: {result['overall_score']:.2f}")
print(f"Passed: {result['passed']}")
```

### 4. Validate Prompts

Validate prompts for quality and safety:

```python
from llm_eval import PromptValidator

# Create validator
validator = PromptValidator()

# Validate a prompt
prompt = "Please explain how neural networks work"
is_valid, issues = validator.validate_prompt(prompt)

# Get improvement suggestions
suggestions = validator.suggest_improvements(prompt)
```

### 5. Check Intent Alignment

Verify if prompts align with expected user intent:

```python
validator = PromptValidator()

prompt = "Write a Python function to calculate factorial"
expected_intent = "create Python factorial function"

alignment = validator.check_intent_alignment(prompt, expected_intent)
print(f"Alignment score: {alignment['alignment_score']:.2f}")
```

## Running Examples

Run the comprehensive example script:

```bash
cd examples
python usage_example.py
```

This will demonstrate:
- Loading task structures from YAML
- Loading and rendering prompt templates
- Evaluating LLM outputs
- Validating prompts
- Checking intent alignment

## Project Structure

```
LLM_Evaluation_and_Prompt_Validation/
├── llm_eval/                    # Core framework modules
│   ├── __init__.py
│   ├── yaml_loader.py          # YAML file handling
│   ├── task_structure.py       # Task structure definitions
│   ├── prompt_template.py      # Prompt template management
│   ├── evaluator.py            # LLM output evaluation
│   └── validator.py            # Prompt validation
├── examples/                    # Example files and usage
│   ├── tasks/                  # Example task YAML files
│   │   ├── summarization_task.yaml
│   │   └── code_generation_task.yaml
│   ├── prompts/                # Example prompt templates
│   │   ├── qa_template.yaml
│   │   ├── code_review_template.yaml
│   │   └── summarization_template.yaml
│   └── usage_example.py        # Comprehensive usage examples
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Key Features

### YAML-Based Configuration
All task structures and prompt templates are defined in YAML format, making them:
- Easy to read and write
- Version-controllable
- Shareable across teams
- Independent of code changes

### Flexible Evaluation
The framework supports multiple evaluation criteria types:
- **Length-based**: Check output length constraints
- **Keyword-based**: Verify presence of required terms
- **Manual**: Placeholder for human evaluation

### Prompt Quality Checks
The validator performs multiple checks:
- Minimum and maximum length validation
- Clear instruction detection
- Harmful content screening
- Improvement suggestions

### Intent Alignment
Check if prompts align with expected user intent using keyword matching and semantic analysis.

## Use Cases

1. **QA Testing**: Validate LLM responses for accuracy and completeness
2. **Prompt Engineering**: Design and test effective prompts
3. **Content Moderation**: Screen prompts for harmful content
4. **Quality Assurance**: Ensure LLM outputs meet quality standards
5. **Template Standardization**: Create reusable prompt templates

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source and available under the MIT License.

## Author

Mohit Mathur

## Project Status

This framework is under active development. Current version: 0.1.0
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
└── data/                             # Evaluation datasets (e.g., benchmark_dataset.yaml)
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
# LLM Evaluation & Prompt Validation

## 📌 Overview
This project focuses on evaluating and improving Large Language Model (LLM) outputs by reviewing AI-generated prompts and responses for correctness, reasoning depth, and alignment with user intent.

The goal is to enhance model reliability through structured feedback and human-in-the-loop evaluation techniques.

## 🎯 Objectives
- Improve factual accuracy and reasoning quality of LLM responses
- Identify hallucinations and logical gaps
- Refine prompts for better instruction adherence

## 🧠 Key Features
- Prompt quality assessment
- Response correctness validation
- Error categorization and tagging
- Structured feedback for model improvement

## 🛠️ Tech Stack
- Generative AI (LLMs)
- Prompt Engineering
- Model Evaluation Frameworks
- Human-in-the-loop AI
- YAML-based task structuring

## 📈 Outcomes
- Improved response clarity and correctness
- Reusable prompt improvement strategies
- Evaluation-ready datasets for benchmarking

## 🚀 Use Cases
- AI model training
- Prompt optimization
- LLM benchmarking
- AI quality assurance
