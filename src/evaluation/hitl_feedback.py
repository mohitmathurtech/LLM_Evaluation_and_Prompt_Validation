"""
Human-in-the-Loop (HITL) Feedback System for LLM Evaluation.

This module implements a structured feedback loop that allows human
evaluators to review, annotate, and provide feedback on LLM responses.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class FeedbackType(Enum):
    """Types of feedback that can be provided."""
    APPROVAL = "approval"
    REJECTION = "rejection"
    MODIFICATION = "modification"
    CLARIFICATION = "clarification"


class QualityRating(Enum):
    """Quality ratings for responses."""
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    UNACCEPTABLE = 1


@dataclass
class HumanFeedback:
    """Represents feedback from a human evaluator."""
    evaluator_id: str
    feedback_type: FeedbackType
    quality_rating: Optional[QualityRating] = None
    comments: str = ""
    suggested_improvements: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)


@dataclass
class EvaluationTask:
    """Represents an evaluation task for human review."""
    task_id: str
    prompt: str
    response: str
    context: Optional[Dict[str, Any]] = None
    auto_validation_results: Optional[Dict[str, Any]] = None
    human_feedback: List[HumanFeedback] = field(default_factory=list)
    status: str = "pending"  # pending, in_review, completed, rejected
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    def add_feedback(self, feedback: HumanFeedback):
        """Add human feedback to this task."""
        self.human_feedback.append(feedback)
        
        # Update status based on feedback
        if feedback.feedback_type == FeedbackType.APPROVAL:
            self.status = "completed"
            self.completed_at = datetime.now().isoformat()
        elif feedback.feedback_type == FeedbackType.REJECTION:
            self.status = "rejected"
            self.completed_at = datetime.now().isoformat()
    
    def get_average_rating(self) -> Optional[float]:
        """Calculate average quality rating from all feedback."""
        ratings = [
            f.quality_rating.value 
            for f in self.human_feedback 
            if f.quality_rating
        ]
        return sum(ratings) / len(ratings) if ratings else None


class HITLFeedbackSystem:
    """
    Manages human-in-the-loop feedback for LLM evaluation.
    
    This system coordinates the review process, tracks feedback,
    and maintains evaluation history.
    """
    
    def __init__(self):
        self.tasks: Dict[str, EvaluationTask] = {}
        self.feedback_history: List[HumanFeedback] = []
        self.task_counter = 0
    
    def create_evaluation_task(
        self,
        prompt: str,
        response: str,
        context: Optional[Dict[str, Any]] = None,
        auto_validation_results: Optional[Dict[str, Any]] = None
    ) -> EvaluationTask:
        """
        Create a new evaluation task for human review.
        
        Args:
            prompt: The original prompt
            response: The LLM-generated response
            context: Optional context information
            auto_validation_results: Results from automated validation
            
        Returns:
            EvaluationTask object
        """
        self.task_counter += 1
        task_id = f"task_{self.task_counter:06d}"
        
        task = EvaluationTask(
            task_id=task_id,
            prompt=prompt,
            response=response,
            context=context,
            auto_validation_results=auto_validation_results
        )
        
        self.tasks[task_id] = task
        return task
    
    def submit_feedback(
        self,
        task_id: str,
        evaluator_id: str,
        feedback_type: FeedbackType,
        quality_rating: Optional[QualityRating] = None,
        comments: str = "",
        suggested_improvements: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Submit feedback for an evaluation task.
        
        Args:
            task_id: ID of the task being evaluated
            evaluator_id: ID of the human evaluator
            feedback_type: Type of feedback
            quality_rating: Optional quality rating
            comments: Evaluator comments
            suggested_improvements: List of suggested improvements
            tags: Optional tags for categorization
            
        Returns:
            True if feedback was submitted successfully
        """
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        feedback = HumanFeedback(
            evaluator_id=evaluator_id,
            feedback_type=feedback_type,
            quality_rating=quality_rating,
            comments=comments,
            suggested_improvements=suggested_improvements or [],
            tags=tags or []
        )
        
        task.add_feedback(feedback)
        self.feedback_history.append(feedback)
        
        return True
    
    def get_task(self, task_id: str) -> Optional[EvaluationTask]:
        """Retrieve a task by ID."""
        return self.tasks.get(task_id)
    
    def get_pending_tasks(self) -> List[EvaluationTask]:
        """Get all tasks pending human review."""
        return [
            task for task in self.tasks.values()
            if task.status == "pending"
        ]
    
    def get_completed_tasks(self) -> List[EvaluationTask]:
        """Get all completed evaluation tasks."""
        return [
            task for task in self.tasks.values()
            if task.status == "completed"
        ]
    
    def get_feedback_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about feedback received.
        
        Returns:
            Dictionary with feedback statistics
        """

        feedback_types = {}
        quality_ratings = []
        
        for feedback in self.feedback_history:
            # Count feedback types
            feedback_type = feedback.feedback_type.value
            feedback_types[feedback_type] = feedback_types.get(feedback_type, 0) + 1
            
            # Collect quality ratings
            if feedback.quality_rating:
                quality_ratings.append(feedback.quality_rating.value)
        
        stats = {
            "total_feedback": len(self.feedback_history),
            "feedback_by_type": feedback_types,
            "average_quality_rating": (
                sum(quality_ratings) / len(quality_ratings)
                if quality_ratings else None
            ),
            "total_tasks": len(self.tasks),
            "pending_tasks": len(self.get_pending_tasks()),
            "completed_tasks": len(self.get_completed_tasks()),
        }
        
        return stats
    
    def export_feedback_data(self, filepath: str):
        """
        Export feedback data to a JSON file.
        
        Args:
            filepath: Path to save the JSON file
        """
        data = {
            "tasks": [
                {
                    "task_id": task.task_id,
                    "prompt": task.prompt,
                    "response": task.response,
                    "status": task.status,
                    "created_at": task.created_at,
                    "completed_at": task.completed_at,
                    "feedback": [
                        {
                            "evaluator_id": f.evaluator_id,
                            "feedback_type": f.feedback_type.value,
                            "quality_rating": f.quality_rating.value if f.quality_rating else None,
                            "comments": f.comments,
                            "suggested_improvements": f.suggested_improvements,
                            "timestamp": f.timestamp,
                            "tags": f.tags
                        }
                        for f in task.human_feedback
                    ]
                }
                for task in self.tasks.values()
            ],
            "statistics": self.get_feedback_statistics()
        }
        
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, indent=2)
    
    def generate_feedback_report(self) -> str:
        """
        Generate a human-readable feedback report.
        
        Returns:
            Formatted report string
        """
        stats = self.get_feedback_statistics()
        
        report = "=" * 60 + "\n"
        report += "HUMAN-IN-THE-LOOP FEEDBACK REPORT\n"
        report += "=" * 60 + "\n\n"
        
        report += f"Total Tasks: {stats.get('total_tasks', 0)}\n"
        report += f"Pending Tasks: {stats.get('pending_tasks', 0)}\n"
        report += f"Completed Tasks: {stats.get('completed_tasks', 0)}\n"
        report += f"Total Feedback Received: {stats.get('total_feedback', 0)}\n\n"
        
        if stats.get('average_quality_rating'):
            report += f"Average Quality Rating: {stats['average_quality_rating']:.2f}/5.0\n\n"
        
        report += "Feedback Distribution:\n"
        for feedback_type, count in stats.get('feedback_by_type', {}).items():
            report += f"  - {feedback_type}: {count}\n"
        
        report += "\n" + "=" * 60 + "\n"
        
        return report


class FeedbackAggregator:
    """
    Aggregates and analyzes feedback from multiple evaluators.
    
    This class provides utilities to identify patterns in feedback
    and generate insights for prompt improvement.
    """
    
    def __init__(self):
        self.feedback_data: List[HumanFeedback] = []
    
    def add_feedback(self, feedback: HumanFeedback):
        """Add feedback to the aggregator."""
        self.feedback_data.append(feedback)
    
    def get_common_issues(self, top_n: int = 5) -> List[str]:
        """
        Identify the most common issues from feedback.
        
        Args:
            top_n: Number of top issues to return
            
        Returns:
            List of common issue descriptions
        """
        issue_counts: Dict[str, int] = {}
        
        for feedback in self.feedback_data:
            for improvement in feedback.suggested_improvements:
                issue_counts[improvement] = issue_counts.get(improvement, 0) + 1
        
        # Sort by frequency and return top N
        sorted_issues = sorted(
            issue_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [issue for issue, _ in sorted_issues[:top_n]]
    
    def get_consensus_rating(self) -> Optional[float]:
        """
        Calculate consensus quality rating.
        
        Returns:
            Average quality rating across all feedback
        """
        ratings = [
            f.quality_rating.value
            for f in self.feedback_data
            if f.quality_rating
        ]
        
        return sum(ratings) / len(ratings) if ratings else None
