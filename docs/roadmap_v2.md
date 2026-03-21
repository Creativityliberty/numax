# NUMAX V2 : La Route vers un Système Supérieur

Ce document sert de référence (Nord Magnétique) pour les futures évolutions de NUMAX. Il cartographie la transition d'un "framework bien architecturé" (V1) vers un "système Agentique réellement supérieur, prouvable et durable" (V2).

---

## 🔝 Le Top 5 Stratégique (Priorité Immédiate)

Ces cinq chantiers sont les piliers qui transformeront NUMAX d'un outil d'exécution en une véritable entité cognitive évolutive.

### 1. Le Benchmark Fondateur NUMAX
NUMAX doit prouver sa supériorité par les mathématiques et la data, pas juste par le design.
- **Répertoires cibles** : `benchmarks/scenarios/`, `benchmarks/metrics.py`, `benchmarks/baselines/`
- **Missions** : Prouver la réussite sur tâches longues, mesurer finement la complétion, valider la récupération après erreur (error recovery), et auditer le coût/temps total.

### 2. La Théorie de la Victoire Documentée
Un document architectural dur (`docs/theory_of_victory.md`) qui explicite la thèse produit : 
- Contre qui NUMAX se compare ?
- Sur quels axes exacts NUMAX gagne ? 
- Quelles hypothèses doivent être vraies ?

### 3. La Couche d'Apprentissage Réel
NUMAX doit arrêter d'être purement gouverné et commencer à apprendre de ses échecs.
- **Répertoires cibles** : `learning/router.py`, `learning/retrieval_ranker.py`, `learning/critic_calibration.py`
- **Missions** : Boucle de log -> feedback -> scoring -> amélioration du routing et de la sélection des modèles.

### 4. La Hiérarchie Mémoire Complète
C'est le composant critique pour un "cerveau durable". L'agent a besoin d'oubli et de consolidation.
- **Répertoires cibles** : `memory/promotion.py`, `memory/retention.py`, `memory/forgetting.py`, `memory/consolidation.py`
- **Missions** : Promouvoir Working -> Episodic, et consolider Episodic -> Semantic. Mettre à jour les "policies" depuis l'historique FSM.

### 5. La Mutation Contrôlée de bout en bout
NUMAX doit pouvoir se mettre à jour et upgrader ses Subagents/Skills sans s'autodétruire.
- **Répertoires cibles** : `release/rollback.py`, `governance/self_change.py`, `skills/uninstall.py`
- **Missions** : Preview, Diff, Backup, Apply, Validate, Rollback.

---

## 🏗️ L'Architecture d'Ingénierie Avancée (Ensuite)

Une fois le cerveau opérationnel et validé, il faudra solidifier les fondations physiques de la plateforme.

### 6. La Frontière Déterministe / Appris
Rédiger `docs/deterministic_vs_learned.md`. Formaliser ce qui est interdit d'apprendre (lois, kill-switch, FSM core) et ce qui DOIT apprendre (routing fin, modèles).

### 7. Couche Providers Intensive
Ne plus se contenter des mocks ou des appels simples. Implémenter de manière native la gestion complexe de `OpenAI`, `Anthropic`, `Google`, `Ollama` avec health check réel, retry backoffs et config des coûts par tokens (in/out).

### 8. Sécurité et Isolation Réelle
- Injecter des guards absolus : `security/prompt_injection.py`, `security/tool_risk_classifier.py`.
- Protéger l'infrastructure avec une vraie sandbox de type container / OS level.

### 9. La Persistance Sérieuse
S'éloigner des JSON locaux pour passer sur `storage/base.py`, `storage/sqlite.py` ou `storage/redis.py` et indexer le lineage exact des sessions pour le rejeu (replay logs).

### 10. Les Tests Systèmes Durs (Chaos Testing)
Éprouver la résilience en conditions hostiles : budget overflow simulé, tool failure infini, perte de connexion provider, déni de permission par le Guardian. L'objectif est de s'assurer que NUMAX échoue avec grâce.

---

## 🚀 Vision Plateforme et Entreprise (Plus Tard)

### 11. Observabilité OTel et Dashboards
Implémenter du vrai traçage de requêtes asynchrones en arbre (spans, lineage run/task/tool), avec heatmap de la graphe NUMAX pour le debugging visuel et les calculs de coûts réels au dixième de centime.

### 12. Benchmark d'Artefacts Structurés
Aller plus loin qu'un simple prompt string. Scoring de qualité par artefact généré via `artifacts/evaluators.py` et validation de la structure avec des juges LLM dédiés.

### 13. Exécution Asynchrone & Jobs
Basculer d'une simple instance locale à `workers/` et `jobs/`. Implémenter une File d'Attente pour exécuter NUMAX de manière distribuée sur des requêtes de plusieurs heures.

### 14. RBAC & Gouvernance Multi-User
Développer `server/middleware/auth.py`. Gérer les accès aux tools et providers pour des instances simultanées de différents rôles.

### 15. Les Bundles NUMAX (Distributions)
Packager le framework en `numax-core`, `numax-dev` et `numax-enterprise` avec des manifestes officiels.
