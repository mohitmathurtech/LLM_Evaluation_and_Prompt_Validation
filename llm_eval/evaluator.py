"""
LLM Evaluator Module

Evaluates LLM outputs against defined criteria and metrics.
"""

from typing import Dict, Any, List, Optional
from .task_structure import TaskStructure


class LLMEvaluator:
    """
    Evaluates LLM outputs to verify correctness, reasoning depth,
    and user intent alignment.
    """
    
    def __init__(self, task: TaskStructure):
        """
        Initialize the evaluator with a task structure.
        
        Args:
            task: TaskStructure defining evaluation criteria
        """
        self.task = task
        self.results = []
    
    def evaluate_output(self, output: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Evaluate an LLM output against the task criteria.
        
        Args:
            output: The LLM-generated output to evaluate
            context: Optional context information for evaluation
            
        Returns:
            Dictionary containing evaluation results
        """
        context = context or {}
        evaluation = {
            'task_id': self.task.task_id,
            'output': output,
            'criteria_results': [],
            'overall_score': 0.0,
            'passed': False
        }
        
        # Evaluate each criterion
        total_score = 0.0
        total_weight = 0.0
        for criterion in self.task.criteria:
            result = self._evaluate_criterion(output, criterion, context)
            evaluation['criteria_results'].append(result)
            weight = criterion.get('weight', 1.0)
            total_score += result['score'] * weight
            total_weight += weight
        
        # Calculate overall score
        if self.task.criteria and total_weight > 0:
            evaluation['overall_score'] = total_score / total_weight
            evaluation['passed'] = evaluation['overall_score'] >= 0.7  # 70% threshold
        
        self.results.append(evaluation)
        return evaluation
    
    def _evaluate_criterion(self, output: str, criterion: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a single criterion.
        
        Args:
            output: The LLM output
            criterion: Criterion definition
            context: Evaluation context
            
        Returns:
            Dictionary containing criterion evaluation result
        """
        criterion_name = criterion.get('name', 'unknown')
        criterion_type = criterion.get('type', 'manual')
        
        result = {
            'name': criterion_name,
            'type': criterion_type,
            'score': 0.0,
            'passed': False,
            'details': ''
        }
        
        # Basic evaluation logic
        if criterion_type == 'length':
            min_length = criterion.get('min_length', 0)
            max_length = criterion.get('max_length', float('inf'))
            output_length = len(output)
            
            if min_length <= output_length <= max_length:
                result['score'] = 1.0
                result['passed'] = True
                result['details'] = f"Output length {output_length} is within range [{min_length}, {max_length}]"
            else:
                result['details'] = f"Output length {output_length} is outside range [{min_length}, {max_length}]"
        
        elif criterion_type == 'keyword_presence':
            required_keywords = criterion.get('keywords', [])
            if required_keywords:
                found_keywords = [kw for kw in required_keywords if kw.lower() in output.lower()]
                
                if found_keywords:
                    result['score'] = len(found_keywords) / len(required_keywords)
                    result['passed'] = result['score'] >= 0.7
                    result['details'] = f"Found {len(found_keywords)}/{len(required_keywords)} required keywords"
                else:
                    result['details'] = "No required keywords found"
            else:
                result['details'] = "No keywords defined for evaluation"
        
        elif criterion_type == 'manual':
            # Manual evaluation placeholder
            result['details'] = "Manual evaluation required"
            result['score'] = 0.5  # Neutral score for manual evaluation
        
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all evaluations performed.
        
        Returns:
            Dictionary containing evaluation summary
        """
        if not self.results:
            return {'total': 0, 'passed': 0, 'failed': 0, 'average_score': 0.0}
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed
        average_score = sum(r['overall_score'] for r in self.results) / total
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'average_score': average_score,
            'pass_rate': passed / total if total > 0 else 0.0
        }
