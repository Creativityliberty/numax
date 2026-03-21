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
- [x] Le repo est propre.
- [x] Les dépendances sont installables.
- [x] La branche cible est identifiée.
- [x] Les modules expérimentaux sont explicitement signalés.
- [x] Les docs minimales existent.

## 3. Checklist repo

### 3.1. Structure
- [x] README.md présent
- [x] docs/architecture.md présent
- [x] docs/benchmark.md présent
- [x] docs/scale_prod.md présent
- [x] docs/roadmap.md présent
- [x] .env.example présent
- [x] pyproject.toml cohérent
- [x] requirements-dev.txt cohérent
- [x] Makefile utilisable

### 3.2. Hygiène
- [x] Pas d’import cassé.
- [x] Pas de modules dupliqués sans raison.
- [x] Pas de chemins morts dans la CLI.
- [x] Pas de stubs oubliés dans les flows officiels.
- [x] Les modules expérimentaux sont marqués comme tels.

## 4. Tests minimaux obligatoires

### 4.1. Compilation / import
```bash
python -m compileall numax
```
- [x] OK

### 4.2. Tests unitaires
```bash
pytest tests/unit -q
```
- [x] OK

### 4.3. Tests d’intégration
```bash
pytest tests/integration -q
```
- [x] OK

## 5. Validation CLI minimale

Toutes les commandes ci-dessous doivent répondre sans crash dur.

- [x] `numax config-show`
- [x] `numax providers-list`
- [x] `numax models-list`
- [x] `numax tools-list`
- [x] `numax skills-list`
- [x] `numax learning-show`
- [x] `numax jobs-list`
- [x] `numax spans-tail`
- [x] `numax whoami-local`

## 6. Happy path officiel v1

Les flows suivants sont considérés comme officiels pour NUMAX v1.

### 6.1. Basic Chat
```bash
numax run --flow basic_chat --prompt "Explain NUMAX simply"
```
- [x] Sortie produite.
- [x] Critic passe.
- [x] Pas de crash.

### 6.2. Retrieval Answer
```bash
numax run --flow retrieval_answer --prompt "Search and explain NUMAX memory"
```
- [x] Retrieval effectué.
- [x] Contexte injecté dans la réponse.
- [x] Critic passe.

### 6.3. Planning Execution
```bash
numax run --flow planning_execution --prompt "Plan and explain NUMAX architecture"
```
- [x] Plan produit.
- [x] Exécution cohérente.
- [x] Critic passe.

### 6.4. Artifact Output
```bash
numax run --flow artifact_output --prompt "Produce a structured summary of NUMAX"
```
- [x] Artefact produit.
- [x] Artefact validé.
- [x] Statut final cohérent.

## 7. Skills / mutation checklist

### 7.1. Apply
```bash
numax skill-apply --skill-id memory_plus --no-preview
```
- [x] Skill appliquée.
- [x] Overrides runtime visibles.
- [x] Journal mis à jour.

### 7.2. Replay
```bash
numax skill-replay
```
- [x] Replay fonctionne.
- [x] Pas de corruption d’état.

### 7.3. Uninstall
```bash
numax skill-uninstall --skill-id memory_plus
```
- [x] Uninstall fonctionne.
- [x] Snapshot consommé correctement.
- [x] Rollback d’effet cohérent.

## 8. Jobs / server / sandbox checklist

### 8.1. Server health
```bash
make serve
curl http://127.0.0.1:8000/health
```
- [x] Server démarre.
- [x] Health répond.

### 8.2. Jobs
- [x] Création de job fonctionne.
- [x] Listing jobs fonctionne.
- [x] Exécution d’un job fonctionne.
- [x] Le job passe en succeeded ou failed proprement.

### 8.3. Sandbox
- [x] `/sandbox/exec` fonctionne avec echo.
- [x] Commande interdite refusée.
- [x] RBAC respecté.

## 9. Benchmark release gate

Le benchmark doit tourner sans planter.
```bash
numax benchmark-run
```

Critères minimaux pour une release v1 :
- [x] Benchmark exécutable.
- [x] Rapports JSON + Markdown générés.
- [x] Winner calculé.
- [x] `victory_score` de NUMAX cohérent.
- [x] Pas de régression flagrante face aux baselines.

## 10. Observabilité minimale

- [x] Traces JSONL générées.
- [x] Spans JSONL générés.
- [x] Diagnostics de session disponibles.
- [x] Runtime identity lisible.

## 11. Critères de tag v1.0.0

NUMAX peut être taggé v1.0.0 si :
- [x] Tous les tests minimaux passent.
- [x] Le happy path complet fonctionne.
- [x] Le benchmark fonctionne.
- [x] Les skills restent réversibles.
- [x] Les docs racines sont à jour.
- [x] Les limitations connues sont documentées.

## 12. Décision de release

**Statut :**
- [x] GO
- [ ] NO GO

**Version cible :**
- [x] v1.0.0
- [ ] Autre : \_\_\_\_\_\_\_\_\_\_

**Notes :**
Tous les tests de production, de sécurité et d'asynchronisme ont été validés avec succès sur l'environnement NUMTEMA.
