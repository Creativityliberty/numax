# NUMAX — Architecture

## 1. Vision

NUMAX est un **cortex agentique gouverné**.

Son objectif n’est pas seulement de répondre à un prompt. Son objectif est de **transformer une intention en sortie structurée**, avec :

* compréhension,
* routage,
* récupération de contexte,
* planification,
* exécution,
* critique,
* mémoire,
* gouvernance,
* production d’artefacts,
* traçabilité,
* évolution contrôlée.

La thèse de NUMAX est simple :

> NUMAX ne gagne pas parce qu’il est “un meilleur modèle”. NUMAX gagne parce qu’il est **un meilleur système**.

---

## 2. Principes fondateurs

NUMAX repose sur quelques principes non négociables.

### 2.1. La cognition est gouvernée

Le système ne doit pas improviser sa propre structure de contrôle. Les priorités, les arrêts, les permissions et les transitions critiques doivent rester explicites.

### 2.2. Toute exécution est traçable

Chaque étape importante laisse une trace exploitable :

* nœud,
* phase,
* message,
* données associées.

### 2.3. La confiance conditionne l’action

NUMAX ne traite pas toutes les situations comme également fiables. La compréhension, la source, la sortie et la sécurité sont suivies séparément.

### 2.4. Le système peut échouer proprement

Le mode `DEGRADED` n’est pas un accident. C’est une capacité. NUMAX doit pouvoir ralentir, simplifier, refuser ou s’arrêter proprement.

### 2.5. La mémoire ne doit pas devenir un dépotoir

La mémoire NUMAX doit :

* promouvoir,
* condenser,
* oublier,
* consolider.

### 2.6. L’évolution doit être réversible

Toute mutation sérieuse doit pouvoir être :

* preview,
* journalisée,
* rejouée,
* validée,
* rollbackée.

---

## 3. Vue d’ensemble de l’architecture

NUMAX est organisé comme un système modulaire à couches.

### 3.1. Vue conceptuelle

```text
Intention utilisateur
    ↓
Observation / State
    ↓
Intent Router
    ↓
Planner / Retrieve / Answer
    ↓
Critic / Validation
    ↓
Artifact Production
    ↓
Memory / Trace / Diagnostics
    ↓
Governance / Runtime Controls
```

### 3.2. Nature du système

NUMAX n’est pas seulement :

* un LLM wrapper,
* un orchestrateur de tools,
* un moteur de prompts.

NUMAX est un système qui combine :

* **machine d’état**,
* **graphe exécutable**,
* **routage**,
* **budget**,
* **confiance**,
* **permissions**,
* **mémoire**,
* **artefacts**,
* **benchmark**,
* **mutation contrôlée**.

---

## 4. Le noyau d’exécution

### 4.1. `core/state.py`

Le cœur de NUMAX est le `NumaxState`.

Il contient notamment :

* `goal`
* `observation`
* `world_state`
* `memory`
* `retrieved_context`
* `plan`
* `candidate_output`
* `critique`
* `final_output`
* `runtime`
* `budget`
* `confidence`
* `trace`

C’est l’objet de vérité de la session.

### 4.2. `core/node.py`

Chaque composant actif de NUMAX est un `NumaxNode`.

Un nœud suit la discipline :

* `prep(state)`
* `exec(payload)`
* `post(state, payload, result)`

Règle importante :

* `exec()` doit rester le plus pur possible
* `post()` écrit dans l’état

### 4.3. `core/graph.py`

Le graphe exécute les nœuds et les transitions.

Il permet :

* l’enchaînement de flows,
* l’auditabilité,
* la réutilisation,
* le contrôle des transitions.

---

## 5. Les flows principaux

### 5.1. `basic_chat`

Flow minimal :

* router
* answer
* critic

Utilisé comme chemin simple.

### 5.2. `retrieval_answer`

Flow orienté contexte :

* router
* retrieve
* answer
* critic

### 5.3. `planning_execution`

Flow orienté tâche structurée :

* router
* planner
* retrieve éventuel
* answer
* critic

### 5.4. `artifact_output`

Flow orienté sortie utile :

* router
* answer
* critic
* artifact

---

## 6. Compréhension et routage

### 6.1. `router/intent.py`

Le routeur d’intention décide si la demande doit :

* aller vers une réponse directe,
* déclencher une récupération,
* passer par un flow plus structuré.

### 6.2. Routage adaptatif

Le routage peut être amélioré via `learning/router.py`.

Les feedbacks sont stockés localement en JSON. Cela permet d’ajuster :

* les mots-clés de retrieval,
* certaines préférences de routage.

---

## 7. Réponse, critique et qualité

### 7.1. `reason/answer.py`

Le nœud de réponse :

* choisit un modèle,
* appelle un provider,
* gère les tentatives,
* peut appliquer un fallback provider/modèle,
* produit la sortie candidate.

### 7.2. `critic/basic.py`

Le critic vérifie :

* qu’une sortie existe,
* que la sécurité reste suffisante,
* que la confiance agrégée n’est pas trop basse.

### 7.3. Calibration du critic

Via `learning/critic_calibration.py`, NUMAX peut ajuster légèrement sa calibration de confiance selon l’expérience passée.

---

## 8. Providers et modèles

### 8.1. Registre providers

`providers/registry.py` contient les providers activés.

### 8.2. Catalogue modèles

`models/catalog.py` décrit les modèles disponibles :

* provider,
* rôle,
* capacités,
* support JSON,
* support tools.

### 8.3. Résolution des modèles

`models/resolver.py` et `learning/model_selector.py` permettent de :

* choisir un modèle selon un rôle,
* utiliser des fallbacks,
* éviter certains modèles,
* apprendre des préférences simples.

### 8.4. Providers réels

NUMAX peut brancher :

* Mock
* OpenAI
* Anthropic
* Google
* Ollama

Le système reste compatible avec un mode purement local / mock.

---

## 9. Retrieval

### 9.1. `retrieve/engine.py`

Le moteur de retrieval v0.1 est simple et local.

### 9.2. `retrieve/node.py`

Le nœud de retrieval :

* exécute la recherche,
* met à jour `retrieved_context`,
* met à jour `source_confidence`.

### 9.3. Reranking adaptatif

`learning/retrieval_ranker.py` permet de reranker légèrement les résultats via feedback JSON local.

---

## 10. Planification

### 10.1. `planner/task.py`

Le planner produit un plan minimal de type :

* retrieve
* answer
* critic

### 10.2. Limite actuelle

Le planner v0.1 reste intentionnellement simple. Son rôle principal est d’introduire :

* la structure,
* la visibilité,
* l’extensibilité.

---

## 11. Budget et confiance

### 11.1. `runtime/budget.py`

NUMAX suit :

* tokens utilisés,
* coût estimé,
* limites budget.

Le budget est une vraie contrainte du runtime.

### 11.2. `critic/confidence.py`

NUMAX distingue plusieurs confiances :

* compréhension,
* source,
* sortie,
* sécurité.

La confiance agrégée sert à :

* valider,
* dégrader,
* arrêter.

---

## 12. Gouvernance

### 12.1. Constitution

`governance/constitution.py` formalise les règles prioritaires.

### 12.2. Priorités

`governance/priorities.py` définit l’ordre :

* safety
* governance
* user fidelity
* quality
* continuity
* cost
* speed

### 12.3. Résolution de conflits

`governance/conflict_resolver.py` arbitre les conflits entre objectifs.

### 12.4. Kill switch

`guardian/kill_switch.py` incarne le principe d’arrêt souverain.

NUMAX doit savoir :

* s’arrêter,
* dégrader,
* escalader,
* refuser.

---

## 13. Permissions, outils, sandbox

### 13.1. `tools/registry.py`

Les outils sont enregistrés avec :

* nom,
* description,
* niveau de risque,
* confirmation requise.

### 13.2. `guardian/permission_judge.py`

Le système décide si un outil est :

* autorisé,
* refusé,
* à confirmer.

### 13.3. `hooks/pre_tool_use.py`

Avant usage d’un outil, NUMAX combine :

* permission,
* sandbox,
* décision finale.

### 13.4. `sandbox/manager.py`

La sandbox v0.1 est logique, pas encore OS/container-native. Mais la structure est là pour évoluer.

---

## 14. Mémoire

### 14.1. Structure mémoire

NUMAX gère plusieurs couches :

* `working`
* `episodic`
* `semantic`
* `continuity`

### 14.2. Continuité

`memory/continuity.py` permet de sauvegarder et restaurer l’état utile entre sessions.

### 14.3. Promotion mémoire

`memory/promotion.py` fait remonter :

* working → episodic
* episodic → semantic

### 14.4. Rétention et oubli

`memory/retention.py` et `memory/forgetting.py` évitent l’accumulation brute.

### 14.5. Consolidation

`memory/consolidation.py` fusionne les patterns récurrents.

### 14.6. Mise à jour de politique

`memory/policy_update.py` permet de dériver une politique mémoire depuis l’historique.

---

## 15. Artefacts

### 15.1. Pourquoi les artefacts sont centraux

NUMAX ne vise pas seulement une réponse textuelle. Il vise une **production structurée**.

### 15.2. `artifacts/schema.py`

Définit la forme d’un artefact :

* type,
* titre,
* contenu,
* quality,
* trace,
* statut.

### 15.3. `artifacts/validators.py`

Valide un artefact minimalement.

### 15.4. `artifacts/renderers.py`

Permet un rendu texte/markdown.

### 15.5. `action/artifacts.py`

Construit un artefact depuis l’état final.

---

## 16. Observabilité

### 16.1. Traces

`obs/traces.py` persiste les traces d’un run en JSONL.

### 16.2. Logs

`obs/logs.py` fournit un logger simple et réutilisable.

### 16.3. Diagnostics

`session/diagnostics.py` synthétise :

* état FSM,
* budget,
* confiance,
* critique,
* sortie,
* nombre de traces.

### 16.4. Identité runtime

`identity/runtime_identity.py` fournit une identité exécutable de NUMAX.

### 16.5. Startup checks

`health/startup_checks.py` vérifie que le runtime démarre dans un état cohérent.

---

## 17. Mutation contrôlée

### 17.1. Skills

NUMAX traite certaines évolutions comme des skills.

### 17.2. Journal JSON

`skills/journal.py` garde une trace locale :

* apply,
* uninstall,
* last known good.

### 17.3. Replay

`skills/replay.py` permet de rejouer un état cohérent.

### 17.4. Rollback

`release/rollback.py` permet un retour vers le dernier état sain connu.

### 17.5. Self change

`governance/self_change.py` décide si une mutation est autorisée.

---

## 18. Apprentissage léger

NUMAX ne repose pas encore sur un apprentissage lourd en ligne. Il utilise un **apprentissage léger JSON/local** sur quelques surfaces :

* routing,
* sélection de modèles,
* ranking retrieval,
* calibration du critic.

Les feedbacks sont stockés localement dans `data/state/`.

Cela garde le système :

* simple,
* traçable,
* gouvernable,
* réversible.

---

## 19. Benchmark

### 19.1. Rôle du benchmark

Le benchmark est essentiel pour tester la thèse NUMAX.

### 19.2. Scénarios

Le benchmark teste déjà des axes comme :

* tâche longue,
* échec retrieval,
* panne provider,
* budget overflow,
* reprise de continuité,
* mutation rollback.

### 19.3. Baselines

NUMAX se compare à :

* `llm_only`
* `llm_tools`
* `llm_tools_memory`

### 19.4. Victory score

Le benchmark calcule un score de victoire agrégé fondé sur :

* réussite tâche,
* récupération,
* continuité,
* sécurité mutation,
* validité artefact.

---

## 20. API et interfaces

### 20.1. CLI

`app.py` expose les commandes principales :

* run
* serve
* providers-list
* models-list
* tools-list
* config-show
* learning-show
* benchmark-run

### 20.2. FastAPI

Le serveur expose des routes pour :

* models
* providers
* recipes
* sessions

### 20.3. MCP minimal

`mcp/server.py` expose une capacité tools/list et tools/call minimale.

---

## 21. Frontière déterministe / appris

### 21.1. Déterministe

Doivent rester durs :

* FSM
* kill switch
* constitution
* priorités
* permission gates
* rollback discipline
* identité runtime

### 21.2. Adaptatif / appris léger

Peuvent évoluer :

* router
* model selector
* retrieval ranker
* critic calibration
* certaines politiques mémoire

### 21.3. Règle de discipline

L’optimisation ne doit jamais dissoudre la gouvernance.

---

## 22. Limites actuelles

NUMAX v0.1 / v1 reste encore limité sur plusieurs plans.

### 22.1. Sandbox réelle

La sandbox n’est pas encore un runtime isolé OS/container.

### 22.2. Providers avancés

Les providers réels sont branchables mais encore fins :

* pas toute la surface tools,
* pas tout le JSON strict,
* pas tous les cas de fallback complexes.

### 22.3. Planner simple

Le planner est encore minimal.

### 22.4. Learning léger

Le système apprend légèrement via JSON local, pas encore via boucle d’apprentissage avancée.

### 22.5. Storage

La persistance reste locale et JSON-based.

---

## 23. Pourquoi cette architecture est intéressante

Parce qu’elle permet déjà de combiner :

* exécution réelle,
* gouvernance,
* observabilité,
* mémoire,
* benchmarking,
* mutation contrôlée,
* production d’artefacts.

Autrement dit : NUMAX commence déjà à se comporter comme un **système cognitif logiciel**, pas seulement comme une chaîne d’appels LLM.

---

## 24. Objectif à moyen terme

Le prochain niveau de NUMAX consiste à renforcer :

* les baselines benchmark,
* les providers réels,
* les fallbacks,
* la mémoire profonde,
* la sécurité réelle,
* la mutation outillée,
* les tests de résilience,
* la preuve expérimentale de la Theory of Victory.

---

## 25. Résumé final

NUMAX est un système qui cherche à unifier :

* perception de la demande,
* raisonnement opérationnel,
* exécution gouvernée,
* continuité mémoire,
* critique,
* sortie structurée,
* évolution contrôlée.

Sa promesse centrale est la suivante :

> produire de meilleures trajectoires d’exécution que les systèmes LLM naïfs, avec plus de robustesse, plus de continuité, plus de contrôle, et une meilleure capacité à survivre au réel.
