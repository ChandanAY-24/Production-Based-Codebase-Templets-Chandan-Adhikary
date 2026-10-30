"""
Super-TDD Unit Tests for TaskService and AgentTask.
Reference: skills/super-tdd.md & docs/SPEC.md
Uses standard library unittest for zero-dependency execution.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import AgentTask, TaskStatus
from src.services import TaskService

class TestTaskService(unittest.TestCase):
    def test_task_creation_valid(self):
        service = TaskService()
        task = service.create_task(
            title="Test Invariant Enforcement",
            spec_ref="docs/SPEC.md#L10",
            invariants=["No unbounded mutations"]
        )
        self.assertEqual(task.title, "Test Invariant Enforcement")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(len(task.invariants), 1)

    def test_task_creation_missing_invariants_raises(self):
        service = TaskService()
        with self.assertRaises(ValueError):
            service.create_task(
                title="Invalid Task",
                spec_ref="docs/SPEC.md",
                invariants=[]
            )

    def test_task_state_transition(self):
        task = AgentTask(
            title="Sample",
            spec_reference="docs/SPEC.md",
            invariants=["Rule 1"]
        )
        self.assertEqual(task.status, TaskStatus.PENDING)

        task.advance_status(TaskStatus.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

        task.advance_status(TaskStatus.REVIEW)
        self.assertEqual(task.status, TaskStatus.REVIEW)

        task.advance_status(TaskStatus.VERIFIED)
        self.assertEqual(task.status, TaskStatus.VERIFIED)

    def test_invalid_state_transition_raises(self):
        task = AgentTask(
            title="Sample",
            spec_reference="docs/SPEC.md",
            invariants=["Rule 1"]
        )
        with self.assertRaises(ValueError):
            task.advance_status(TaskStatus.VERIFIED)

if __name__ == "__main__":
    unittest.main()
