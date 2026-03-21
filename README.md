# NUMAX : Cortex Agentique Gouverné (V1)

**NUMAX** est plus qu’un framework d'agents IA, c'est un **système autonome, gouverné et déterministe**. Il ne cherche pas simplement à empiler des appels LLM ou produire "un modèle plus performant", mais vise un système d'exécution formelle garantissant une **robustesse absolue sur les tâches longues** grâce à une constitution explicite et des garanties budgétaires.

---

## 🚀 Le Cœur de la V1 : L'Architecture Complète

NUMAX est construit selon **7 phases architecturales** clés, toutes implémentées nativement dans le système. Ce document lie la philosophie abstraite aux **modules Python concrets** de l'engin :

### 1. Robustesse, Limites et Outils (`numax/errors/`, `numax/runtime/`, `numax/tools/`)
La base de l'exécution :
*   `taxonomy.py` & `policies.py` : Typage formel des erreurs (Compréhension, Budget, Temps, API) avec politique de résilience (Retry, Degrade, Halt).
*   `stop_conditions.py` : Limites mathématiques de l'exécution.
*   `registry.py` & `node.py` : Un écosystème d'outils branché directement au Flow, calculant ses propres latences.

### 2. Gouvernance, Gardiens & Hubs de Sécurité (`numax/guardian/`, `numax/sandbox/`)
NUMAX ne s'emballe jamais. Avant chaque appel d'outil (via `hooks/pre_tool_use.py`), le code traverse :
*   `permission_judge.py` : Analyse du risque de l'outil face au *Autonomy Mode* global de l'environnement (`ASSISTED`, `MUTATION_FORBIDDEN`, etc).
*   `sandbox/manager.py` : Restriction logique empêchant matériellement un agent d'altérer les mauvaises couches de données.
*   `tool_confirmation_router.py` : Couche d'Human-In-The-Loop asynchrone pour les opérations haut-risque (ex: modification de BD).

### 3. Planification, Recettes & Subagents (`numax/planner/`, `numax/subagents/`)
L'axe cognitif :
*   Un nœud d'orchestration (`planner/task.py`) capable de casser une requête ambiguë (Intent) en `TaskMorsels`.
*   Des sous-agents encapsulés et bornés par un contrat d'autonomie `config.py` et gérés par le `SubagentRunner`.
*   Des `recipes` (`loader.py`), véritables matrices JSON pré-définissant le flow cognitif.

### 4. Mode Serveur, API & MCP Protocol (`numax/server/`, `numax/mcp/`)
NUMAX est conçu pour tourner 24/7 en backend asynchrone :
*   Une architecture `FastAPI` (dans `server/app.py`), découpée en routes (`sessions`, `models`, `providers`, `recipes`).
*   Intégration du standard **Model Context Protocol (MCP)** via `FastMCP` (`mcp/server.py`), permettant à d'autres écosystèmes IA (comme Claude ou Cursor) de manipuler les outils de NUMAX.

### 5. Observabilité, Diagnostics et Identité Runtime (`numax/obs/`, `numax/session/`)
La prédictibilité avant tout :
*   Des Traces JSONL indexées par Session ID (`obs/traces.py`), couplées à un `diagnostics.py` mesurant la santé du run (confiance, budget, dégradation).
*   `identity/runtime_identity.py` (hash SHA-256 des paramètres d'exécution) et `health/startup_checks.py` garantissant qu'aucune execution ne démarre dans un environnement corrompu ou incomplet.

### 6. Gestion Verrouillée des Artefacts (`numax/artifacts/`)
Fini les sorties textes non cadrées :
*   Typage strict (`schema.py`, `types.py`) forçant NUMAX à produire des standards (`spec`, `report`, `code_scaffold`).
*   Des validateurs intrinsèques évaluant `completeness`, `correctness`, et format validity avant de classer l'artefact en `validated`.

### 7. La Constitution Exécutable & Le Kill Switch Matériel (`numax/governance/`)
La fierté du système NUMAX : sa constitution implémentée mathématiquement :
*   `priorities.py` & `constitution.py` : Établissent que la `SAFETY (100)` est toujours numériquement supérieure à la `SPEED (40)`.
*   `conflict_resolver.py` tranchant les ambiguïtés dynamiques (`Cost` vs `Quality`).
*   Un `kill_switch.py` impitoyable, capable de forcer l'état système à `DEGRADED` ou de stopper l'exécution si la confiance ou le budget s'effondre.

---

## 🧩 Le FSM Maître (Flux Cognitif Principal)

Peu importe la couche traversée (`planning_execution`, `retrieval_answer`, ou `artifact_output`), le système respecte le cycle :
`PERCEVOIR` → `ROUTER` → `RÉCUPÉRER` → `PLANIFIER` → `EXÉCUTER (Tools)` → `CRITIQUER` → `LIVRER ARTEFACT`

**Toute sortie non validée par le nœud `Critic` est soit répétée (Retry), soit bloquée par le `KillSwitch`.**

---

## 🛠️ Utilisation et Commandes (`numax.app`)

Installer NUMAX via `pip install -e .` ou `make install`.

- **Serveur API REST :**
  ```bash
  make serve
  ```
- **Diagnostic et Identité Runtime :**
  ```bash
  python -m numax.app startup-checks
  python -m numax.app runtime-identity
  ```
- **Exécution FSM directe en CLI :**
  ```bash
  make run flow="artifact_output" prompt="Explique la gouvernance de NUMAX"
  ```
- **Inspecter le registre d'outil :**
  ```bash
  python -m numax.app tools-list
  ```
