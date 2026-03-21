# Plan d'Exécution NUMAX V2 — Bloc "MAINTENANT"

Ce document détaille l'architecture, les livrables et l'ordre d'implémentation exact pour les 5 chantiers prioritaires du passage à NUMAX V2.

---

## 1. Le Benchmark Fondateur
**But** : Prouver que NUMAX est meilleur qu'un simple LLM, LLM + tools, ou LLM + tools + mémoire légère.

**Arborescence à construire** :
```text
benchmarks/
  scenarios/
    long_task/
    retrieval_failure/
    provider_failure/
    budget_overflow/
    continuity_resume/
    mutation_rollback/
  baselines/
    llm_only.py
    llm_tools.py
    llm_tools_memory.py
  metrics.py
  runner.py
  report.py
```

**Métriques définies dans `metrics.py`** :
- `task_success_rate`
- `artifact_validity_rate`
- `recovery_success_rate`
- `continuity_resume_score`
- `budget_efficiency_score`
- `average_runtime_seconds`
- `mutation_safety_score`

**Livrables attendus** : `runner.py`, `report.py`, et le premier document `benchmark_results.md`.

---

## 2. La Théorie de la Victoire (Theory of Victory)
**But** : Écrire noir sur blanc pourquoi NUMAX gagne, de manière courte, brutale et falsifiable.

**Fichier** : `docs/theory_of_victory.md`

**Structure recommandée** :
- **A. Thèse** : NUMAX gagne par sa gouvernance, sa continuité, la gestion des coûts et des artefacts.
- **B. Adversaires** : LLM seul, LLM + tools, LLM + tools + mémoire simple.
- **C. 5 promesses testables** : Robustesse (tâches longues), récupération d'erreurs, contrôle des coûts, continuité inter-session, et mutations sûres.
- **D. Conditions de défaite** : Ce qui invaliderait le framework (ex: coût de gouvernance trop lourd).
- **E. Axe principal** : NUMAX n'est pas un meilleur modèle, c'est un meilleur système.

---

## 3. La Frontière Déterministe / Appris
**But** : Empêcher NUMAX de devenir flou, en séparant la logique infaillible de la logique apprenante.

**Fichier** : `docs/deterministic_vs_learned.md`

**Déterministe (en dur)** : Invariants, FSM, Kill Switch, Constitution, Priorités, Versioning, Rollback, Permission gates.
**Apprenable (plus tard)** : Routing, Ranking retrieval, Model selection, Critic calibration, Memory promotion.

---

## 4. La Mémoire Complète
**But** : Passer d'une mémoire "présente" à une mémoire "gouvernée" (trie, condense, oublie, apprend).

**Arborescence à créer** :
```text
numax/memory/
  promotion.py
  retention.py
  forgetting.py
  consolidation.py
  policy_update.py
```

**Logique minimale** :
- `promote_working_to_episodic(state)` : si décision importante, erreur ou interaction marquante.
- `promote_episodic_to_semantic(memory_store)` : si répétition d'un motif, utilité prouvée.
- `forget_low_value_items(memory_store)` : nettoyage du bruit et vieux contextes inutiles.
- `consolidate_patterns(memory_store)` : fusionner les épisodes en préférences stables.
- `update_memory_policy_from_history(memory_store)` : adapter les requêtes LLM selon les échecs récents.

---

## 5. La Mutation Contrôlée
**But** : Permettre à NUMAX d'évoluer (Skills, Subagents) sans se désintégrer.

**Arborescence à créer** :
```text
numax/skills/
  apply.py
  uninstall.py
  replay.py

numax/release/
  rollback.py
  migrations.py

numax/governance/
  self_change.py
```

**Pipeline strict** : `preview` → `diff` → `backup` → `apply` → `replay` → `validate` → `commit`. (Si échec → `rollback`).

---

## 📅 Ordre d'Implémentation Recommandé

### Semaine 1 : Théorie & Fondations Benchmark
- [ ] `docs/theory_of_victory.md`
- [ ] `docs/deterministic_vs_learned.md`
- [ ] Structure `benchmarks/` et premiers scénarios de benchmark

### Semaine 2 : Le Cerveau Profond (Memory)
- [ ] `numax/memory/promotion.py`
- [ ] `numax/memory/retention.py`
- [ ] `numax/memory/forgetting.py`
- [ ] `numax/memory/consolidation.py`

### Semaine 3 : Le Système Évolutif (Mutation)
- [ ] `numax/skills/apply.py`
- [ ] `numax/skills/replay.py`
- [ ] `numax/release/rollback.py`
- [ ] `numax/governance/self_change.py`

### Semaine 4 : Validation & Couverture Systémique
- [ ] `benchmarks/runner.py` complet
- [ ] `benchmarks/report.py`
- [ ] Mutation tests
- [ ] Continuity tests avec mémoire consolidée
