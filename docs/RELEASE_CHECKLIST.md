# NUMAX — Release Checklist

Ce document définit la checklist minimale pour considérer une release NUMAX comme suffisamment propre pour être gelée, taggée et utilisée.

## 1. Objectif

La release checklist existe pour éviter deux erreurs classiques :
- Publier une version qui “semble marcher” mais dont le comportement réel n’est pas stabilisé.
- Continuer à ajouter des features alors que la version n’a pas encore été figée proprement.

Une release NUMAX n’est valide que si :
- Le happy path tient.
- Les tests passent.
- Les flows officiels tournent.
- Le benchmark produit un signal cohérent.
- La mutation reste réversible.
- La documentation de base est à jour.

## 2. Préconditions avant release

Avant de lancer la checklist finale, vérifier que :
- [ ] Le repo est propre.
- [ ] Les dépendances sont installables.
- [ ] La branche cible est identifiée.
- [ ] Les modules expérimentaux sont explicitement signalés.
- [ ] Les docs minimales existent.

## 3. Checklist repo

### 3.1. Structure
- [ ] README.md présent
- [ ] docs/architecture.md présent
- [ ] docs/benchmark.md présent
- [ ] docs/scale_prod.md présent
- [ ] docs/roadmap.md présent
- [ ] .env.example présent
- [ ] pyproject.toml cohérent
- [ ] requirements-dev.txt cohérent
- [ ] Makefile utilisable

### 3.2. Hygiène
- [ ] Pas d’import cassé.
- [ ] Pas de modules dupliqués sans raison.
- [ ] Pas de chemins morts dans la CLI.
- [ ] Pas de stubs oubliés dans les flows officiels.
- [ ] Les modules expérimentaux sont marqués comme tels.

## 4. Tests minimaux obligatoires

### 4.1. Compilation / import
```bash
python -m compileall numax
```
- [ ] OK

### 4.2. Tests unitaires
```bash
pytest tests/unit -q
```
- [ ] OK

### 4.3. Tests d’intégration
```bash
pytest tests/integration -q
```
- [ ] OK

## 5. Validation CLI minimale

Toutes les commandes ci-dessous doivent répondre sans crash dur.

- [ ] `numax config-show`
- [ ] `numax providers-list`
- [ ] `numax models-list`
- [ ] `numax tools-list`
- [ ] `numax skills-list`
- [ ] `numax learning-show`
- [ ] `numax jobs-list`
- [ ] `numax spans-tail`
- [ ] `numax whoami-local`

## 6. Happy path officiel v1

Les flows suivants sont considérés comme officiels pour NUMAX v1.

### 6.1. Basic Chat
```bash
numax run --flow basic_chat --prompt "Explain NUMAX simply"
```
- [ ] Sortie produite.
- [ ] Critic passe.
- [ ] Pas de crash.

### 6.2. Retrieval Answer
```bash
numax run --flow retrieval_answer --prompt "Search and explain NUMAX memory"
```
- [ ] Retrieval effectué.
- [ ] Contexte injecté dans la réponse.
- [ ] Critic passe.

### 6.3. Planning Execution
```bash
numax run --flow planning_execution --prompt "Plan and explain NUMAX architecture"
```
- [ ] Plan produit.
- [ ] Exécution cohérente.
- [ ] Critic passe.

### 6.4. Artifact Output
```bash
numax run --flow artifact_output --prompt "Produce a structured summary of NUMAX"
```
- [ ] Artefact produit.
- [ ] Artefact validé.
- [ ] Statut final cohérent.

## 7. Skills / mutation checklist

### 7.1. Apply
```bash
numax skill-apply --skill-id memory_plus --no-preview
```
- [ ] Skill appliquée.
- [ ] Overrides runtime visibles.
- [ ] Journal mis à jour.

### 7.2. Replay
```bash
numax skill-replay
```
- [ ] Replay fonctionne.
- [ ] Pas de corruption d’état.

### 7.3. Uninstall
```bash
numax skill-uninstall --skill-id memory_plus
```
- [ ] Uninstall fonctionne.
- [ ] Snapshot consommé correctement.
- [ ] Rollback d’effet cohérent.

## 8. Jobs / server / sandbox checklist

### 8.1. Server health
```bash
make serve
curl http://127.0.0.1:8000/health
```
- [ ] Server démarre.
- [ ] Health répond.

### 8.2. Jobs
- [ ] Création de job fonctionne.
- [ ] Listing jobs fonctionne.
- [ ] Exécution d’un job fonctionne.
- [ ] Le job passe en succeeded ou failed proprement.

### 8.3. Sandbox
- [ ] `/sandbox/exec` fonctionne avec echo.
- [ ] Commande interdite refusée.
- [ ] RBAC respecté.

## 9. Benchmark release gate

Le benchmark doit tourner sans planter.
```bash
numax benchmark-run
```

Critères minimaux pour une release v1 :
- [ ] Benchmark exécutable.
- [ ] Rapports JSON + Markdown générés.
- [ ] Winner calculé.
- [ ] `victory_score` de NUMAX cohérent.
- [ ] Pas de régression flagrante face aux baselines.

## 10. Observabilité minimale

- [ ] Traces JSONL générées.
- [ ] Spans JSONL générés.
- [ ] Diagnostics de session disponibles.
- [ ] Runtime identity lisible.

## 11. Critères de tag v1.0.0

NUMAX peut être taggé v1.0.0 si :
- Tous les tests minimaux passent.
- Le happy path complet fonctionne.
- Le benchmark fonctionne.
- Les skills restent réversibles.
- Les docs racines sont à jour.
- Les limitations connues sont documentées.

## 12. Décision de release

**Statut :**
- [ ] GO
- [ ] NO GO

**Version cible :**
- [ ] v1.0.0
- [ ] Autre : \_\_\_\_\_\_\_\_\_\_

**Notes :**
...
