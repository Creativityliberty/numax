from __future__ import annotations

from enum import Enum


class ErrorCategory(str, Enum):
    UNDERSTANDING_ERROR = "UNDERSTANDING_ERROR"
    ROUTING_ERROR = "ROUTING_ERROR"
    SOURCE_ERROR = "SOURCE_ERROR"
    TOOL_ERROR = "TOOL_ERROR"
    PLANNING_ERROR = "PLANNING_ERROR"
    COHERENCE_ERROR = "COHERENCE_ERROR"
    BUDGET_ERROR = "BUDGET_ERROR"
    MEMORY_ERROR = "MEMORY_ERROR"
    MUTATION_ERROR = "MUTATION_ERROR"
    SUPERVISION_ERROR = "SUPERVISION_ERROR"
    SAFETY_ERROR = "SAFETY_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class NumaxError(Exception):
    category: ErrorCategory = ErrorCategory.UNKNOWN_ERROR

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UnderstandingError(NumaxError):
    category = ErrorCategory.UNDERSTANDING_ERROR


class RoutingError(NumaxError):
    category = ErrorCategory.ROUTING_ERROR


class SourceError(NumaxError):
    category = ErrorCategory.SOURCE_ERROR


class ToolError(NumaxError):
    category = ErrorCategory.TOOL_ERROR


class PlanningError(NumaxError):
    category = ErrorCategory.PLANNING_ERROR


class CoherenceError(NumaxError):
    category = ErrorCategory.COHERENCE_ERROR


class BudgetError(NumaxError):
    category = ErrorCategory.BUDGET_ERROR


class MemoryError(NumaxError):
    category = ErrorCategory.MEMORY_ERROR


class MutationError(NumaxError):
    category = ErrorCategory.MUTATION_ERROR


class SupervisionError(NumaxError):
    category = ErrorCategory.SUPERVISION_ERROR


class SafetyError(NumaxError):
    category = ErrorCategory.SAFETY_ERROR
