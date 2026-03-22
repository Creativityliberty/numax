from __future__ import annotations

from numax.teams.specs import TeamMemberSpec, TeamSpec


def build_product_squad() -> TeamSpec:
    return TeamSpec(
        team_id="product_squad",
        name="Product Squad",
        purpose="Clarify intent, produce specs, and structure missions.",
        default_flow="specification_loop",
        supported_missions=["specification", "blueprint", "planning"],
        members=[
            TeamMemberSpec(
                member_id="product_lead",
                role="lead",
                capabilities=["spec_run", "planning", "handover"],
            ),
            TeamMemberSpec(
                member_id="product_researcher",
                role="researcher",
                capabilities=["clarification", "assumption_mapping"],
            ),
        ],
    )


def build_engineering_squad() -> TeamSpec:
    return TeamSpec(
        team_id="engineering_squad",
        name="Engineering Squad",
        purpose="Inspect repo, propose changes, test, and iterate.",
        default_flow="repo_repair",
        supported_missions=["repo_change", "repair", "implementation"],
        members=[
            TeamMemberSpec(
                member_id="eng_lead",
                role="lead",
                capabilities=["task_split", "review_patch_scope"],
            ),
            TeamMemberSpec(
                member_id="eng_operator",
                role="operator",
                capabilities=["workspace_ops", "search_code", "run_tests"],
            ),
            TeamMemberSpec(
                member_id="eng_coder",
                role="coder",
                capabilities=["patch_proposal", "patch_refinement"],
                external_subagent_id="mock_repo_worker",
            ),
        ],
    )


def build_qa_squad() -> TeamSpec:
    return TeamSpec(
        team_id="qa_squad",
        name="QA Squad",
        purpose="Validate changes, score outputs, and decide accept/revise/revert.",
        default_flow="subagent_review",
        supported_missions=["review", "qa_validation", "artifact_scoring"],
        members=[
            TeamMemberSpec(
                member_id="qa_lead",
                role="lead",
                capabilities=["review_decision", "risk_assessment"],
            ),
            TeamMemberSpec(
                member_id="qa_reviewer",
                role="reviewer",
                capabilities=["code_review", "artifact_review"],
            ),
            TeamMemberSpec(
                member_id="qa_auditor",
                role="qa",
                capabilities=["acceptance_check", "scorecard"],
            ),
        ],
    )
