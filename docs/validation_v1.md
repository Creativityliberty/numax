# Batterie Minimaliste de Validation V1

Ce document recense les commandes essentielles pour valider que l'architecture NUMAX V1, incluant les piliers d'industrialisation (Scale & Prod), fonctionne correctement sur votre machine.

## 1. Vérification de la CLI (Sanity Check)

Vérifions que l'application se charge et que tous les registres (modèles, outils, skills, etc.) sont bien connectés :

```bash
numax config-show
numax providers-list
numax models-list
numax tools-list
numax skills-list
numax jobs-list
numax whoami-local
```

## 2. Le "Happy Path" des Flows (Le cœur de NUMAX)

Faisons tourner l'agent sur les 4 flows principaux pour valider le moteur cognitif orienté graphe (FSM) :

```bash
numax run --flow basic_chat --prompt "Explique NUMAX simplement"
numax run --flow retrieval_answer --prompt "Cherche et explique la mémoire de NUMAX"
numax run --flow planning_execution --prompt "Fais un plan pour construire une nouvelle feature"
numax run --flow artifact_output --prompt "Produis un résumé structuré de l'architecture"
```

> **Astuce :** Après chaque run, exécutez `numax spans-tail` pour visualiser la queue des traces OTel (OpenTelemetry) générées en arrière-plan.

## 3. Test du Système Évolutif (Skills & Mutations)

Vérifions que le système peut muter localement de manière réversible grâce au système transactionnel des skills :

```bash
numax skill-apply --skill-id memory_plus --preview False
numax skill-replay
numax skill-uninstall --skill-id memory_plus
```

## 4. Test du Superviseur Asynchrone (Serveur & Jobs)

Vérifions que l'API de Production tourne bien avec les middlewares RBAC et permet d'isoler des commandes dans la Sandbox.

**Dans un premier terminal, lancez le serveur :**
```bash
make serve
```

**Dans un second terminal, interrogez l'API :**

*1. Vérifier la santé du serveur :*
```bash
curl http://127.0.0.1:8000/health
```

*2. Vérifier les permissions RBAC de l'identité Admin :*
```bash
curl -H "x-numax-roles: admin" http://127.0.0.1:8000/admin/whoami
```

*3. Lancer une commande isolée dans la Sandbox (Nécessite le rôle `admin`) :*
```bash
curl -X POST http://127.0.0.1:8000/sandbox/exec \
     -H "Content-Type: application/json" \
     -H "x-numax-roles: admin" \
     -d '{"command": ["echo", "Hello depuis la NUMAX Sandbox !"]}'
```

## 5. La Preuve Scientifique (Benchmark)

Pour prouver que ce système surclasse les implémentations LLM naïves grâce à sa "Theory of Victory" (mémoire, récupération après erreur, mutabilité...) :

```bash
numax benchmark-run
```

---

*Si l'ensemble de ces commandes s'exécute avec succès, la fondation NUMAX V1 est opérationnelle et prête pour les environnements de production (Scale).*
