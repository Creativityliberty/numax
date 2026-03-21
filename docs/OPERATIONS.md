# NUMAX — Operations Guide

Ce document décrit comment exploiter NUMAX en pratique, localement ou dans une première forme de déploiement simple.

## 1. Objectif

Ce guide couvre :
- Démarrage
- Configuration
- Storage
- Jobs
- Skills
- Benchmark
- Traces
- Degraded mode
- Rollback

Il ne couvre pas encore un déploiement distribué de niveau production avancée.

## 2. Installation

### 2.1. Environnement
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt
```

### 2.2. Configuration minimale
Vérifier :
- `configs/base.yaml`
- `configs/providers.yaml`
- `configs/routing.yaml`
- `configs/budget.yaml`
- `configs/governance.yaml`
- `.env`

## 3. Commandes utiles

### 3.1. Runtime local
```bash
numax run --flow basic_chat --prompt "Explain NUMAX simply"
numax run --flow retrieval_answer --prompt "Search and explain NUMAX memory"
numax run --flow planning_execution --prompt "Plan and explain NUMAX architecture"
numax run --flow artifact_output --prompt "Produce a structured summary of NUMAX"
```

### 3.2. Inspection
```bash
numax config-show
numax learning-show
numax providers-list
numax models-list
numax tools-list
numax store-list
numax store-backend
numax jobs-list
numax spans-tail
```

### 3.3. Skills
```bash
numax skills-list
numax skill-apply --skill-id research_mode --no-preview
numax skill-replay
numax skill-uninstall --skill-id research_mode
```

### 3.4. Benchmark
```bash
numax benchmark-run
```

### 3.5. Server
```bash
make serve
```

## 4. Storage backend

NUMAX supporte actuellement plusieurs backends potentiels via `NUMAX_STORE_BACKEND`.

### 4.1. JSON local
Par défaut :
- Simple
- Lisible
- Pratique pour le local

### 4.2. SQLite
Activer avec :
```bash
export NUMAX_STORE_BACKEND=sqlite
export NUMAX_SQLITE_PATH=data/store/numax.db
```

### 4.3. Redis
Préparé mais à considérer comme backend avancé.

### 4.4. Postgres
Préparé mais à considérer comme backend avancé.

## 5. Providers

### 5.1. Providers supportés
- `mock`
- `openai`
- `anthropic`
- `google`
- `ollama`

### 5.2. Politique d’usage
En local, `mock` reste le chemin le plus robuste pour valider NUMAX lui-même. Les providers réels servent à tester :
- Fallback
- Qualité réelle
- Coûts externes
- Comportements de prod

### 5.3. Providers async
La surface async existe déjà mais doit être considérée comme montée de maturité, pas comme noyau v1 le plus stable.

## 6. Skills / mutation

### 6.1. Ce qu’est une skill
Une skill est une mutation bornée du runtime NUMAX.

Elle peut agir sur :
- Runtime overrides
- Router keywords
- Model preferences
- Critic policy

### 6.2. Journal
Le journal local stocke :
- Apply
- Uninstall
- Last known good

### 6.3. Replay
Le replay rejoue les skills connues depuis le journal.

### 6.4. Rollback
Le rollback restaure l’état connu comme sain.

### 6.5. Bon usage
Ne pas appliquer plusieurs skills expérimentales en chaîne sans valider :
- Benchmark
- Happy path
- Uninstall

## 7. Jobs et tâches longues

### 7.1. Modèle actuel
NUMAX dispose d’une couche jobs locale :
- Création
- Persistance
- Exécution
- Suivi d’état

### 7.2. Cycle
- `queued`
- `running`
- `succeeded`
- `failed`
- `cancelled`

### 7.3. Limite actuelle
C’est une base de jobs locale. Ce n’est pas encore une queue distribuée complète.

## 8. Observabilité

### 8.1. Traces
NUMAX écrit déjà :
- Traces JSONL
- Spans JSONL
- Metrics JSONL

### 8.2. Où regarder
- `data/traces/`
- `data/state/`
- `benchmarks/outputs/`

### 8.3. Commandes utiles
```bash
numax spans-tail
```

### 8.4. Limite actuelle
L’export OTel réel n’est pas encore branché. L’observabilité reste locale/structurée.

## 9. Degraded mode

### 9.1. Ce que ça veut dire
Le mode `DEGRADED` signifie que NUMAX a détecté une condition qui empêche une exécution normale :
- Budget
- Critic
- Provider
- Sécurité
- Mutation cassée

### 9.2. Ce qu’il faut faire
Quand NUMAX tombe en `DEGRADED` :
1. Lire le diagnostic.
2. Regarder les traces.
3. Vérifier budget / provider / critic.
4. Vérifier si une skill récente a été appliquée.
5. Rollback si nécessaire.

### 9.3. À ne pas faire
Ne pas forcer immédiatement d’autres mutations sans comprendre la cause.

## 10. Sandbox

### 10.1. Position actuelle
NUMAX possède une sandbox bornée :
- Allowlist de commandes
- Blocked tokens
- Timeout
- Contrôle RBAC

### 10.2. Usage
Route serveur : `/sandbox/exec`
CLI de test : `numax sandbox-echo --message hello`

### 10.3. Limite
La sandbox n’est pas encore une isolation dure type container namespace/seccomp.

## 11. Benchmark en exploitation

Le benchmark doit être lancé régulièrement pour détecter les régressions système.

**Commande :**
```bash
numax benchmark-run
```

**À surveiller :**
- `winner`
- `ranking`
- `victory_score`
- `recovery_success`
- `continuity_score`
- `mutation_safety`
- `artifact_validity`

## 12. Incident handling minimal

En cas d’incident local :
1. Relire le flow fautif.
2. Inspecter `data/traces/`.
3. Inspecter `data/state/`.
4. Vérifier les skills récemment appliquées.
5. Désinstaller / rollback si nécessaire.
6. Relancer un benchmark minimal.

## 13. Exploitation recommandée v1

Le meilleur mode d’exploitation v1 est :
- Local sérieux.
- Storage JSON ou SQLite.
- Benchmark fréquent.
- Skills peu nombreuses mais bien validées.
- Providers réels activés de manière progressive.

## 14. Résumé opérationnel

NUMAX v1 est exploitable si on le traite comme :
- Un système gouverné.
- Une machine testable.
- Un runtime mesuré.
- Un moteur à mutation prudente.

Pas comme une boîte noire magique.
