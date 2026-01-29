"""
Unit tests for HITL Feedback System module.

Tests the human-in-the-loop feedback functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tempfile
from src.evaluation.hitl_feedback import (
    HITLFeedbackSystem,
    FeedbackAggregator,
    HumanFeedback,
    FeedbackType,
    QualityRating,
    EvaluationTask
)


class TestEvaluationTask(unittest.TestCase):
    """Test cases for EvaluationTask class."""
    
    def test_add_feedback(self):
        """Test adding feedback to a task."""
        task = EvaluationTask(
            task_id="test_1",
            prompt="Test prompt",
            response="Test response"
        )
        
        feedback = HumanFeedback(
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.GOOD
        )
        
        task.add_feedback(feedback)
        
        self.assertEqual(len(task.human_feedback), 1)
        self.assertEqual(task.status, "completed")
    
    def test_add_rejection_feedback(self):
        """Test adding rejection feedback."""
        task = EvaluationTask(
            task_id="test_1",
            prompt="Test",
            response="Test"
        )
        
        feedback = HumanFeedback(
            evaluator_id="eval_1",
            feedback_type=FeedbackType.REJECTION
        )
        
        task.add_feedback(feedback)
        
        self.assertEqual(task.status, "rejected")
    
    def test_get_average_rating(self):
        """Test calculating average rating."""
        task = EvaluationTask(
            task_id="test_1",
            prompt="Test",
            response="Test"
        )
        
        task.add_feedback(HumanFeedback(
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.GOOD
        ))
        
        task.add_feedback(HumanFeedback(
            evaluator_id="eval_2",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.EXCELLENT
        ))
        
        avg = task.get_average_rating()
        
        self.assertEqual(avg, 4.5)  # (4 + 5) / 2


class TestHITLFeedbackSystem(unittest.TestCase):
    """Test cases for HITLFeedbackSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = HITLFeedbackSystem()
    
    def test_create_evaluation_task(self):
        """Test creating an evaluation task."""
        task = self.system.create_evaluation_task(
            prompt="Test prompt",
            response="Test response"
        )
        
        self.assertIsNotNone(task.task_id)
        self.assertEqual(task.prompt, "Test prompt")
        self.assertEqual(task.status, "pending")
    
    def test_submit_feedback(self):
        """Test submitting feedback for a task."""
        task = self.system.create_evaluation_task(
            prompt="Test",
            response="Test"
        )
        
        success = self.system.submit_feedback(
            task_id=task.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.GOOD,
            comments="Good work"
        )
        
        self.assertTrue(success)
        self.assertEqual(len(task.human_feedback), 1)
    
    def test_submit_feedback_invalid_task(self):
        """Test submitting feedback for non-existent task."""
        success = self.system.submit_feedback(
            task_id="invalid_id",
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL
        )
        
        self.assertFalse(success)
    
    def test_get_pending_tasks(self):
        """Test retrieving pending tasks."""
        task1 = self.system.create_evaluation_task("Test 1", "Response 1")
        task2 = self.system.create_evaluation_task("Test 2", "Response 2")
        
        # Approve task1
        self.system.submit_feedback(
            task_id=task1.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL
        )
        
        pending = self.system.get_pending_tasks()
        
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].task_id, task2.task_id)
    
    def test_get_completed_tasks(self):
        """Test retrieving completed tasks."""
        task = self.system.create_evaluation_task("Test", "Response")
        
        self.system.submit_feedback(
            task_id=task.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL
        )
        
        completed = self.system.get_completed_tasks()
        
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].task_id, task.task_id)
    
    def test_get_feedback_statistics(self):
        """Test getting feedback statistics."""
        task1 = self.system.create_evaluation_task("Test 1", "Response 1")
        task2 = self.system.create_evaluation_task("Test 2", "Response 2")
        
        self.system.submit_feedback(
            task_id=task1.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.EXCELLENT
        )
        
        self.system.submit_feedback(
            task_id=task2.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.REJECTION,
            quality_rating=QualityRating.POOR
        )
        
        stats = self.system.get_feedback_statistics()
        
        self.assertEqual(stats["total_feedback"], 2)
        self.assertEqual(stats["total_tasks"], 2)
        self.assertIn("approval", stats["feedback_by_type"])
        self.assertIn("rejection", stats["feedback_by_type"])
    
    def test_export_feedback_data(self):
        """Test exporting feedback data to JSON."""
        task = self.system.create_evaluation_task("Test", "Response")
        self.system.submit_feedback(
            task_id=task.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            comments="Good"
        )
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        temp_file.close()
        
        self.system.export_feedback_data(temp_file.name)
        
        self.assertTrue(os.path.exists(temp_file.name))
        
        # Clean up
        os.unlink(temp_file.name)
    
    def test_generate_feedback_report(self):
        """Test generating a feedback report."""
        task = self.system.create_evaluation_task("Test", "Response")
        self.system.submit_feedback(
            task_id=task.task_id,
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.GOOD
        )
        
        report = self.system.generate_feedback_report()
        
        self.assertIn("FEEDBACK REPORT", report)
        self.assertIn("Total Tasks", report)
        self.assertIn("approval", report)


class TestFeedbackAggregator(unittest.TestCase):
    """Test cases for FeedbackAggregator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aggregator = FeedbackAggregator()
    
    def test_add_feedback(self):
        """Test adding feedback to aggregator."""
        feedback = HumanFeedback(
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.GOOD
        )
        
        self.aggregator.add_feedback(feedback)
        
        self.assertEqual(len(self.aggregator.feedback_data), 1)
    
    def test_get_common_issues(self):
        """Test identifying common issues."""
        feedback1 = HumanFeedback(
            evaluator_id="eval_1",
            feedback_type=FeedbackType.MODIFICATION,
            suggested_improvements=["Improve clarity", "Add examples"]
        )
        
        feedback2 = HumanFeedback(
            evaluator_id="eval_2",
            feedback_type=FeedbackType.MODIFICATION,
            suggested_improvements=["Improve clarity", "Fix grammar"]
        )
        
        self.aggregator.add_feedback(feedback1)
        self.aggregator.add_feedback(feedback2)
        
        common_issues = self.aggregator.get_common_issues(top_n=3)
        
        self.assertEqual(common_issues[0], "Improve clarity")
    
    def test_get_consensus_rating(self):
        """Test calculating consensus rating."""
        feedback1 = HumanFeedback(
            evaluator_id="eval_1",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.GOOD
        )
        
        feedback2 = HumanFeedback(
            evaluator_id="eval_2",
            feedback_type=FeedbackType.APPROVAL,
            quality_rating=QualityRating.EXCELLENT
        )
        
        self.aggregator.add_feedback(feedback1)
        self.aggregator.add_feedback(feedback2)
        
        rating = self.aggregator.get_consensus_rating()
        
        self.assertEqual(rating, 4.5)


if __name__ == '__main__':
    unittest.main()
