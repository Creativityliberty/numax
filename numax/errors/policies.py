from __future__ import annotations

from dataclasses import dataclass

from numax.errors.taxonomy import ErrorCategory


@dataclass
class ErrorPolicyDecision:
    action: str
    note: str


def decide_error_policy(category: ErrorCategory) -> ErrorPolicyDecision:
    """
    Minimal NUMAX v0.1 error policy.
    """

    if category == ErrorCategory.UNDERSTANDING_ERROR:
        return ErrorPolicyDecision(
            action="simplify_or_reask",
            note="Try a simpler interpretation or a clarification path.",
        )

    if category == ErrorCategory.ROUTING_ERROR:
        return ErrorPolicyDecision(
            action="reroute",
            note="Retry with a fallback route.",
        )

    if category == ErrorCategory.SOURCE_ERROR:
        return ErrorPolicyDecision(
            action="retrieve_again_or_degrade",
            note="Retry retrieval or lower source confidence.",
        )

    if category == ErrorCategory.TOOL_ERROR:
        return ErrorPolicyDecision(
            action="retry_or_fallback_tool",
            note="Retry the tool or use a fallback tool if available.",
        )

    if category == ErrorCategory.PLANNING_ERROR:
        return ErrorPolicyDecision(
            action="replan",
            note="Discard current plan and generate a smaller one.",
        )

    if category == ErrorCategory.COHERENCE_ERROR:
        return ErrorPolicyDecision(
            action="critic_rewrite",
            note="Send candidate output through critic/rewrite path.",
        )

    if category == ErrorCategory.BUDGET_ERROR:
        return ErrorPolicyDecision(
            action="degrade",
            note="Reduce depth, compress context, use lighter models.",
        )

    if category == ErrorCategory.MEMORY_ERROR:
        return ErrorPolicyDecision(
            action="reset_memory_slice",
            note="Reset or isolate failing memory state.",
        )

    if category == ErrorCategory.MUTATION_ERROR:
        return ErrorPolicyDecision(
            action="rollback",
            note="Rollback mutation and restore previous state.",
        )

    if category == ErrorCategory.SUPERVISION_ERROR:
        return ErrorPolicyDecision(
            action="halt_or_supervisor_recover",
            note="Escalate to supervisor recovery path.",
        )

    if category == ErrorCategory.SAFETY_ERROR:
        return ErrorPolicyDecision(
            action="halt",
            note="Stop execution immediately.",
        )

    return ErrorPolicyDecision(
        action="degrade",
        note="Unknown error category: enter safe degraded mode.",
    )
