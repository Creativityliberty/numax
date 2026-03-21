from __future__ import annotations


def build_seccomp_policy() -> dict:
    return {
        "profile": "numax_default",
        "network": "restricted",
        "filesystem": "bounded",
    }
