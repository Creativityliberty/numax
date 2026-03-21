# NUMAX

**NUMAX** est un cortex agentique gouverné : une architecture capable de transformer une intention en artefacts structurés via un pipeline typé, traçable, budgété, critiqué, mémorisé et extensible.

Ce projet ne cherche pas à produire un “modèle plus gros”.
Il cherche à construire un **système plus fort que le deep learning isolé**, en combinant :

- une orchestration modulaire,
- une mémoire hiérarchique,
- une couche providers/models interchangeable,
- une gouvernance explicite,
- une supervision runtime,
- une politique de confiance,
- une discipline d’évolution contrôlée.

---

## Vision

Le deep learning classique est un moteur.

NUMAX vise à être un **système complet** :
- il comprend,
- il planifie,
- il récupère du contexte,
- il choisit des outils,
- il simule des options,
- il produit,
- il critique,
- il mémorise,
- il se supervise,
- il évolue sans perdre son intégrité.

La promesse n’est pas “plus d’intelligence brute”.
La promesse est :

- plus de robustesse sur tâches longues,
- meilleure récupération après erreur,
- meilleur contrôle coût/qualité,
- meilleure continuité inter-session,
- meilleure gouvernance des mutations système.

---

## Positionnement

### Ce que NUMAX n’est pas

NUMAX n’est pas :
- un simple wrapper autour d’un LLM,
- un orchestrateur de tools sans mémoire réelle,
- un chatbot avec un peu de RAG,
- un framework de flows sans théorie interne,
- un agent “autonome” sans gouvernance.

### Ce que NUMAX est

NUMAX est :
- un **cortex agentique unifié**,
- un **runtime gouverné**,
- un **système de production d’artefacts**,
- un **framework de flows cognitifs**,
- une **plateforme extensible** via skills, recipes, subagents et providers.

---

## Principe fondateur

La cognition n’est pas traitée comme un bloc opaque.
Elle est modélisée comme une chaîne observable de transformations :

**Percevoir → Structurer → Router → Récupérer → Planifier → Construire → Critiquer → Délivrer → Mémoriser → Apprendre**

Chaque étape est :
- typée,
- traçable,
- budgétée,
- soumise à des invariants.

---

## Les inspirations fondatrices

NUMAX fusionne plusieurs traditions architecturales :

### PocketFlow
Apporte :
- le contrat de nœud `prep / exec / post / fallback`,
- les flows explicites,
- les graphes imbriqués,
- le batch et l’async.

### Ouroboros
Apporte :
- la séparation superviseur / cœur agent,
- les invariants runtime,
- le budget comme ressource de premier rang,
- la continuité d’état,
- la discipline de versioning.

### creativityliberty-num
Apporte :
- la couche providers/models,
- le routage de modèles,
- la policy runtime,
- le catalogue de modèles,
- les garde-fous coût / rate limits.

### NanoClawPulse
Apporte :
- la logique de skills,
- le replay comme vérité,
- preview/apply/rollback,
- les hooks,
- la mutation contrôlée.

### PocketManus
Apporte :
- les adapters agent/tool/workflow,
- les workflows réels de planning/validation,
- MCP,
- l’exécution sandboxée.

### block-goose
Apporte :
- les providers canonisés,
- les permissions robustes,
- les subagents bornés,
- les recipes,
- l’architecture server-first,
- les distributions produit.

### Meta Cortex
Apporte :
- les invariants,
- le FSM maître,
- les rôles internes,
- le modèle d’énergie,
- le schéma de sous-tâche,
- l’ontologie minimale.

---

## Le FSM maître

NUMAX fonctionne selon un automate d’état global :

```text
IDLE → UNDERSTAND → PLAN → BUILD → DELIVER → LEARN → IDLE
```

Transitions d’exception :
- `ANY → HALT`
- `BUILD → RETRY`
- `PLAN → REPLAN`
- `ANY → DEGRADED`
- `DELIVER → CRITIC_REVIEW`

Ce FSM garantit qu’aucune exécution ne se transforme en flux incontrôlé.

---

## Les invariants non négociables

1. Tout objet possède un **type** et un **statut**.
2. Tout morphisme est **traçable** et **coûté**.
3. Tout flux émet un **événement**.
4. Toute décision est **mémorisée**.
5. Toute transition respecte le **FSM**.
6. Toute tâche possède un **owner unique**.
7. Toute sortie passe par une **critique minimale**.
8. Tout dépassement budget déclenche une **garde**.
9. Toute mutation est **testable, replayable ou rollbackable**.
10. Le système peut entrer en **mode DEGRADED**.
11. La **confiance conditionne l’action**.
12. Aucun self-change n’est permis hors gouvernance.

---

## Les rôles internes

NUMAX ne repose pas sur un “agent unique omnipotent”.
Il distribue les responsabilités entre rôles logiques :

- **CLARIFIER** : comprend et reformule le besoin
- **ARCHITECT** : planifie
- **EXECUTOR** : exécute
- **CRITIC** : valide
- **GUARDIAN** : protège
- **INTEGRATOR** : assemble et délivre
- **REFLECTOR** : apprend
- **OBSERVER** : mesure et trace

Ces rôles peuvent être implémentés comme modules, nœuds ou sous-agents, selon le niveau de sophistication.

---

## Objet central : `TaskMorsel`

NUMAX décompose le travail en unités canoniques :

```json
{
  "id": "...",
  "objective": "...",
  "inputs": [],
  "outputs": [],
  "morphism": "...",
  "dependencies": [],
  "energy_cost": 0.0,
  "confidence": 0.0,
  "status": "proposed"
}
```

Le `TaskMorsel` est l’unité minimale de planification, d’exécution, d’audit et d’apprentissage.

---

## Architecture globale

```text
INPUT
  ↓
PERCEPTION
  ↓
WORLD STATE
  ↓
ROUTER
  ├─ RETRIEVE
  ├─ PLAN
  ├─ REASON
  ├─ SIMULATE
  ├─ ACT
  └─ CRITIC
  ↓
DELIVER
  ↓
MEMORY
  ↓
LEARN / REFLECT
  ↓
SUPERVISOR / GOVERNANCE / HEALTH / RELEASE
```

---

## Les grandes couches

### 1. Meta Layer
Formalise :
- invariants,
- univers,
- énergie,
- FSM,
- rôles,
- schémas de tâches.

### 2. Core Execution Layer
Fournit :
- état typé,
- nœuds,
- graphes,
- batch,
- async,
- branching.

### 3. Runtime Layer
Gère :
- retry,
- budget,
- économie interne,
- rate limits,
- ownership,
- fallback,
- recovery.

### 4. Perception / World State
Construit une compréhension exploitable de la situation.

### 5. Router Layer
Décide :
- quel flow,
- quel outil,
- quel modèle,
- quel niveau de critic,
- quel mode d’autonomie.

### 6. Retrieval Layer
RAG, chunking, rerank, citations, provenance.

### 7. Planning Layer
Décompose les objectifs en `TaskMorsels`.

### 8. Reasoning Layer
Produit :
- réponses,
- synthèses,
- comparaisons,
- transformations.

### 9. Simulation Layer
Évalue des alternatives et des contrefactuels.

### 10. Action Layer
Exécute des outils et produit des artefacts.

### 11. Critic Layer
Mesure :
- factualité,
- logique,
- sécurité,
- style,
- confiance.

### 12. Memory Layer
Maintient :
- working memory,
- mémoire épisodique,
- mémoire sémantique,
- continuité,
- tool history,
- compaction de contexte.

### 13. Providers / Models Layer
Normalise :
- providers,
- modèles,
- rôles,
- coût,
- fallback,
- capacités.

### 14. Tools / Skills / Recipes / Subagents
Permet l’extension et la composition :
- tools atomiques,
- skills installables,
- recipes réutilisables,
- subagents bornés,
- summon unifié.

### 15. Guardian / Security / Sandbox
Applique :
- permissions,
- inspection de risque,
- confirmation tool,
- sandboxing,
- adversary checks,
- kill switch.

### 16. Supervisor / Session / Identity
Maintient :
- queue,
- workers,
- lifecycle,
- diagnostics,
- session resume,
- identité runtime.

### 17. Observability Layer
Trace :
- events,
- spans,
- coût,
- lineage,
- tools,
- modèles,
- sessions.

### 18. Governance / Release Layer
Contrôle :
- constitution,
- priorités,
- self-change,
- migrations,
- semver,
- rollback,
- release invariants.

### 19. Server / MCP / ACP / IDE Layer
Expose NUMAX vers :
- API,
- IDE,
- UI,
- agents externes,
- outils externes.

### 20. Distributions Layer
Permet des variantes produit :
- `numax-core`
- `numax-dev`
- `numax-research`
- `numax-enterprise`
- `numax-local`

---

## Providers et modèles

NUMAX sépare strictement :
- le **cortex**,
- les **providers**,
- les **modèles**.

Un modèle est décrit par une forme canonique :

```json
{
  "id": "anthropic:claude-sonnet-x",
  "provider": "anthropic",
  "model_name": "claude-sonnet-x",
  "roles": ["primary", "critic"],
  "capabilities": ["chat", "json", "tools"],
  "supports_json": true,
  "supports_tools": true,
  "supports_vision": false,
  "status": "enabled"
}
```

NUMAX doit supporter :
- providers codés,
- providers déclaratifs,
- providers locaux,
- auto-détection d’environnement,
- runtime policy par rôle.

---

## Système de confiance

NUMAX ne doit pas utiliser une confiance vague.
Il distingue au minimum :

- `understanding_confidence`
- `source_confidence`
- `plan_confidence`
- `execution_confidence`
- `output_confidence`
- `safety_confidence`

La confiance globale n’autorise jamais une action si la composante sécurité est insuffisante.

---

## Modèle d’erreur

NUMAX classe explicitement les erreurs :

- compréhension
- routage
- source
- outil
- planification
- cohérence
- budget
- mémoire
- mutation
- supervision
- sécurité

Chaque classe d’erreur possède une politique dédiée :
- retry,
- fallback,
- replan,
- degrade,
- rollback,
- escalate,
- halt.

---

## Économie interne

NUMAX suit explicitement :
- coût token,
- coût outil,
- coût review,
- coût simulation,
- coût critic multi-modèle,
- coût mémoire,
- coût mutation.

Modes de dépense recommandés :
- `cheap`
- `balanced`
- `high_assurance`

Le système ne dépense plus par habitude, mais selon enjeu, risque, confiance et criticité.

---

## Mémoire hiérarchique

NUMAX distingue :
- **working memory** : contexte actif,
- **episodic memory** : journal des décisions et événements saillants,
- **semantic memory** : patterns consolidés,
- **tool history** : usages, succès, échecs, latences,
- **continuity memory** : reprise, identité, compatibilité.

Règle clé :
la mémoire n’est pas un stockage passif.
Elle implique :
- promotion,
- consolidation,
- compaction,
- oubli,
- archivage.

---

## Autonomie

NUMAX doit fonctionner selon des modes explicites :

- `ASSISTED`
- `SEMI_AUTONOMOUS`
- `BOUNDED_AUTONOMOUS`
- `SUPERVISED_AUTONOMOUS`

Et pour les mutations :
- `MUTATION_FORBIDDEN`
- `MUTATION_PREVIEW_ONLY`
- `MUTATION_APPROVED`

Aucune autonomie n’est implicite.

---

## Skills, recipes, subagents

### Skill
Capacité atomique installable.

### Recipe
Orchestration réutilisable.

### Mode
Politique de fonctionnement.

### Subagent
Agent borné, traçable, jetable, délégable.

### Summon
Couche d’unification qui permet :
- charger,
- déléguer,
- combiner.

---

## Mutation contrôlée

NUMAX ne doit jamais muter par simple impulsion.

Pipeline de mutation :

```text
preview → diff → backup → apply → replay → test → validate → commit
```

En cas d’échec :

```text
rollback → restore → mark_failed
```

---

## Vérification d’identité système

NUMAX doit vérifier qu’il est bien lui-même, dans un état cohérent.

Contrôles requis :
- signature d’état,
- version runtime,
- version mémoire,
- hash de configuration,
- hash des skills,
- hash du registre providers/models,
- compatibilité de constitution.

Sans cela, la continuité n’est qu’un vœu pieux.

---

## Théorie de l’artefact

Le but de NUMAX n’est pas seulement de “répondre”.
Le but est de **produire des artefacts structurés**.

Un artefact possède :
- un type,
- un schéma,
- des critères qualité,
- une traçabilité de fabrication,
- un statut de validation.

Types d’artefacts initiaux recommandés :
- spec
- report
- brief
- plan
- summary
- workflow bundle
- code scaffold

---

## Sécurité

NUMAX distingue trois niveaux d’exécution :

### Anneau 1
Lecture seule / faible risque.

### Anneau 2
Modification sandboxée.

### Anneau 3
Action à risque élevé → confirmation, refus ou confinement strict.

Le Guardian décide selon :
- le risque de l’outil,
- le mode d’autonomie,
- le permission mode,
- la confiance,
- les politiques de gouvernance.

---

## API et intégration

NUMAX doit être pilotable via :
- API HTTP
- MCP server
- MCP client
- ACP bridge
- IDE integration
- UI server-first

Exemples d’endpoints :
- `/cortex/instantiate`
- `/cortex/run`
- `/cortex/state`
- `/models/list`
- `/providers/list`
- `/skills/index`
- `/skills/invoke`
- `/sessions/*`

---

## Observabilité

Chaque run NUMAX doit produire :
- `session_id`
- `run_id`
- `task_lineage`
- `tool_lineage`
- `model_lineage`
- `cost_lineage`
- `trace spans`
- `events`
- `critic results`

Un système non observable n’est pas gouvernable.

---

## Ce qui rend NUMAX supérieur à un LLM + tools simple

NUMAX vise à gagner sur 5 axes mesurables :

1. **Robustesse sur tâches longues**
2. **Récupération après erreur**
3. **Contrôle coût/qualité**
4. **Continuité inter-session**
5. **Gouvernance des mutations**

Autrement dit :
NUMAX n’est pas censé être “juste plus intelligent”.
Il doit être **plus stable, plus gouverné, plus récupérable et plus mesurable**.

---

## Ce qui doit rester déterministe

Doit rester en dur :
- invariants,
- gouvernance,
- versioning,
- ownership,
- budget guards,
- rollback,
- transitions critiques,
- seuils sécurité.

---

## Ce qui peut apprendre

Peut être appris progressivement :
- router fin,
- ranking retrieval,
- plan selection,
- model selector,
- critic calibration,
- memory promotion heuristics,
- strategy adaptation,
- simulation scoring.

Le système ne doit jamais confondre apprentissage et abandon de contrôle.

---

## Roadmap de départ

### V0.1
- core
- runtime minimal
- router
- retrieve
- reason
- critic basic
- memory working + continuity
- traces

### V0.2
- providers/models
- runtime policy
- budget economy
- benchmark minimal
- confidence system
- error taxonomy

### V0.3
- planner
- skills
- recipes
- subagents bornés
- guardian permissions
- sandbox

### V0.4
- supervisor
- server-first API
- MCP
- session resume
- identity verification
- release invariants

### V0.5
- world model fast/slow
- counterfactuals
- learning ciblé
- distributions produit
- background reflection

---

## Arborescence cible

```text
numax/
  meta/
  core/
  runtime/
  perception/
  state/
  router/
  retrieve/
  planner/
  reason/
  sim/
  action/
  critic/
  memory/
  providers/
  models/
  tools/
  skills/
  recipes/
  modes/
  summon/
  subagents/
  guardian/
  hooks/
  sandbox/
  security/
  supervisor/
  session/
  identity/
  governance/
  health/
  obs/
  mcp/
  acp/
  server/
  background/
  release/
  distributions/
  flows/
```

---

## Phrase manifeste

NUMAX n’est pas un modèle plus gros.

C’est un **cortex agentique gouverné** : un système typé, traçable, budgété, critiqué, mémorisé, extensible et capable d’évolution contrôlée.

Son ambition n’est pas de remplacer le deep learning.
Son ambition est de **l’intégrer dans une machine cognitive plus large, plus disciplinée et plus utile**.

