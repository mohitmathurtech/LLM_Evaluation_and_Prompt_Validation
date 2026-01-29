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
