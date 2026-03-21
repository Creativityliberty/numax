# NUMAX — README technique v0.1

## Objectif

Ce document sert de base de repo pour démarrer NUMAX comme projet réel.

Il couvre :
- l’installation,
- l’arborescence minimale,
- la configuration,
- les conventions de code,
- les flows de départ,
- les commandes de développement,
- la trajectoire vers une v1 exploitable.

---

## Stack recommandée

### Langage
- Python 3.11+

### Outils
- `uv` ou `pip`
- `pytest`
- `ruff`
- `mypy`
- `pydantic`
- `fastapi`
- `typer`
- `httpx`
- `rich`

### Optionnel
- `docker`
- `langfuse` ou OpenTelemetry
- `sqlite` pour persistance locale simple
- `redis` plus tard si queue/runtime distribué

---

## Installation

### 1. Cloner le repo

```bash
git clone <repo-url> numax
cd numax
```

### 2. Créer l’environnement

Avec `uv` :

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

Avec `pip` :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Installer les dépendances dev

```bash
pip install -r requirements-dev.txt
```

---

## Variables d’environnement

Créer un fichier `.env` à partir de `.env.example`.

Exemple minimal :

```env
NUMAX_ENV=dev
NUMAX_LOG_LEVEL=INFO
NUMAX_DATA_DIR=./data
NUMAX_AUTONOMY_MODE=ASSISTED

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
OPENROUTER_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Arborescence minimale v0.1

```text
numax/
├── README.md
├── VERSION
├── pyproject.toml
├── .env.example
├── configs/
│   ├── base.yaml
│   ├── providers.yaml
│   ├── routing.yaml
│   ├── budget.yaml
│   └── governance.yaml
├── numax/
│   ├── __init__.py
│   ├── app.py
│   ├── bootstrap.py
│   ├── core/
│   │   ├── state.py
│   │   ├── node.py
│   │   └── graph.py
│   ├── runtime/
│   │   ├── retry.py
│   │   ├── budget.py
│   │   └── stop_conditions.py
│   ├── router/
│   │   └── intent.py
│   ├── reason/
│   │   └── answer.py
│   ├── retrieve/
│   │   └── engine.py
│   ├── critic/
│   │   ├── basic.py
│   │   └── confidence.py
│   ├── memory/
│   │   ├── working.py
│   │   └── continuity.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── registry.py
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   └── google.py
│   ├── models/
│   │   ├── catalog.py
│   │   └── resolver.py
│   ├── tools/
│   │   ├── registry.py
│   │   └── schemas.py
│   ├── obs/
│   │   ├── traces.py
│   │   └── logs.py
│   └── flows/
│       ├── basic_chat.py
│       └── retrieval_answer.py
├── tests/
│   ├── unit/
│   └── integration/
└── data/
    ├── memory/
    ├── state/
    ├── traces/
    └── artifacts/
```

---

## Fichiers de configuration

### `configs/base.yaml`

```yaml
app:
  name: numax
  env: dev
  log_level: INFO

runtime:
  autonomy_mode: ASSISTED
  degraded_mode_enabled: true
  max_retries: 2

memory:
  persistence: sqlite
  compact_context_threshold: 0.8
```

### `configs/providers.yaml`

```yaml
providers:
  openai:
    enabled: true
  anthropic:
    enabled: true
  google:
    enabled: true
  ollama:
    enabled: false
```

### `configs/routing.yaml`

```yaml
models:
  primary: anthropic:claude-sonnet
  light: google:gemini-fast
  critic: openai:gpt-4.1
  fallbacks:
    - openai:gpt-4.1
    - google:gemini-fast
```

### `configs/budget.yaml`

```yaml
budget:
  mode: balanced
  max_cost_usd: 2.0
  max_tokens_total: 80000
  max_critic_cost_usd: 0.4
```

### `configs/governance.yaml`

```yaml
governance:
  min_execution_confidence: 0.6
  min_validation_confidence: 0.8
  mutation_mode: MUTATION_FORBIDDEN
  tool_confirmation_required: true
```

---

## Contrat de nœud

Tous les nœuds NUMAX suivent le même contrat.

```python
class NumaxNode:
    name: str = "unnamed"

    def prep(self, state):
        return {}

    def exec(self, payload):
        raise NotImplementedError

    def exec_fallback(self, state, payload, exc):
        raise exc

    def post(self, state, payload, result):
        return "default"
```

### Règles
- `prep()` lit dans l’état
- `exec()` ne dépend que du payload
- `post()` écrit dans l’état et retourne la transition
- `exec_fallback()` doit être explicite

---

## Modèle d’état minimal

```python
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class NumaxState(BaseModel):
    goal: Dict[str, Any] = Field(default_factory=dict)
    observation: Dict[str, Any] = Field(default_factory=dict)
    world_state: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    retrieved_context: List[Dict[str, Any]] = Field(default_factory=list)
    plan: Optional[Dict[str, Any]] = None
    candidate_output: Optional[Any] = None
    critique: Optional[Dict[str, Any]] = None
    final_output: Optional[Any] = None
    runtime: Dict[str, Any] = Field(default_factory=dict)
    budget: Dict[str, Any] = Field(default_factory=dict)
    trace: List[Dict[str, Any]] = Field(default_factory=list)
```

---

## Premier flow conseillé

### `flows/basic_chat.py`

But :
- comprendre une demande simple,
- produire une réponse,
- la critiquer légèrement,
- sortir proprement.

Ordre :

```text
Input → IntentRouter → AnswerNode → BasicCritic → Output
```

### `flows/retrieval_answer.py`

But :
- détecter besoin de contexte,
- récupérer,
- répondre,
- critiquer factualité minimum.

Ordre :

```text
Input → IntentRouter → RetrieveNode → AnswerNode → FactCritic → Output
```

---

## Commandes de développement

### Lancer les tests

```bash
pytest
```

### Lancer les tests unitaires seulement

```bash
pytest tests/unit -q
```

### Lancer le lint

```bash
ruff check .
```

### Formater

```bash
ruff format .
```

### Vérifier les types

```bash
mypy numax
```

### Lancer un flow local

```bash
python -m numax.app run --flow basic_chat
```

### Lancer le flow RAG

```bash
python -m numax.app run --flow retrieval_answer
```

---

## Interface CLI minimale

NUMAX devrait exposer une CLI simple via `typer`.

Exemples de commandes :

```bash
numax run --flow basic_chat
numax run --flow retrieval_answer
numax models list
numax providers list
numax skills list
numax config show
numax trace show <run_id>
```

---

## Providers et modèles

### Objectif v0.1
Avoir un registre simple avec :
- providers activés par config,
- modèles configurés par rôle,
- fallback chain minimale.

### Fonctions à exposer
- `list_providers()`
- `list_models()`
- `resolve_model(role="primary")`
- `get_provider_health()`

---

## Politique de confiance minimale

À implémenter dès le début :
- `understanding_confidence`
- `source_confidence`
- `output_confidence`
- `safety_confidence`

### Politique simple
- si `safety_confidence < threshold` → stop
- si `source_confidence` bas → réponse avec réserve
- si `understanding_confidence` bas → simplifier ou re-router

---

## Politique d’erreur minimale

Créer une taxonomie simple :
- `UNDERSTANDING_ERROR`
- `SOURCE_ERROR`
- `TOOL_ERROR`
- `BUDGET_ERROR`
- `SAFETY_ERROR`

Et une policy simple :
- retry
- fallback
- degrade
- halt

---

## Observabilité minimale

Chaque run doit stocker :
- `run_id`
- `flow_name`
- `nodes_visited`
- `tool_calls`
- `model_calls`
- `total_cost`
- `errors`
- `final_status`

Stockage v0.1 : JSONL local dans `data/traces/`.

---

## Tests prioritaires

### Unitaires
- état valide
- transition de nœud
- routeur simple
- budget guard
- confidence policy

### Intégration
- basic chat flow
- retrieval flow
- fallback flow
- degraded mode entry

---

## Ordre d’implémentation recommandé

### Phase 1
- `core/state.py`
- `core/node.py`
- `core/graph.py`
- `router/intent.py`
- `reason/answer.py`
- `critic/basic.py`
- `obs/traces.py`

### Phase 2
- `retrieve/engine.py`
- `providers/base.py`
- `providers/registry.py`
- `models/catalog.py`
- `models/resolver.py`
- `runtime/budget.py`

### Phase 3
- `critic/confidence.py`
- `runtime/stop_conditions.py`
- `memory/continuity.py`
- `tests/integration/*`

### Phase 4
- `planner/*`
- `skills/*`
- `guardian/*`
- `sandbox/*`
- `server/*`

---

## Critères de réussite v0.1

NUMAX v0.1 est considéré comme valide si :

1. il exécute au moins 2 flows utiles,
2. il possède un état typé,
3. il route entre réponse simple et retrieval,
4. il utilise un registre providers/models,
5. il critique minimalement les sorties,
6. il trace tous les runs,
7. il peut entrer proprement en mode dégradé,
8. il reste testable sans magie implicite.

---

## Ce qu’il ne faut pas faire trop tôt

Ne pas implémenter dès le début :
- tous les providers du monde,
- les subagents complexes,
- la mutation automatique,
- le world model complet,
- l’UI lourde,
- les distributions produit,
- les recipes compliquées,
- les hooks profonds,
- ACP complet.

Le repo doit d’abord tenir debout sur son noyau.

---

## Conventions de code

### Style
- fonctions courtes
- typage partout
- erreurs explicites
- pas de logique implicite cachée
- pas de state mutation sauvage dans `exec()`

### Logging
- logs structurés
- niveau INFO par défaut
- niveau DEBUG activable

### Config
- config centralisée
- priorité : env > local file > base config

### Tests
- tout nœud critique doit avoir au moins un test unitaire
- tout flow de prod doit avoir un test d’intégration

---

## Prochaine étape après ce README

Quand cette base est en place, la suite logique est :
- `README architecture`
- `theory_of_victory.md`
- `deterministic_vs_learned.md`
- `artifact_theory.md`
- benchmark minimal
- supervisor minimal
- providers/models plus riches

---

## Résumé

Le but de ce README technique n’est pas de tout construire d’un coup.
Le but est de permettre un **démarrage propre, réaliste et testable**.

NUMAX v0.1 doit être petit, mais dur.

Petit dans la surface.
Dur dans les invariants.

