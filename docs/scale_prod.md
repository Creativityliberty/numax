# NUMAX — Scale / Prod Plan + Features Map

Ce document complète le README principal et le README d’architecture.
Il sert à répondre à deux questions :
1. **Comment NUMAX passe d'un framework local avancé à un runtime scale/prod ?**
2. **Quelles features sont déjà présentes, partiellement présentes, ou encore manquantes ?**

---

## 1. Où en est NUMAX aujourd’hui

NUMAX est déjà un système local sérieux avec :
- noyau exécutable,
- flows,
- providers/models,
- critic,
- budget,
- mémoire,
- artefacts,
- benchmark,
- journal JSON des skills,
- replay / rollback,
- server-first,
- observabilité locale.

En revanche, NUMAX n’est pas encore un runtime scale/prod complet. Le passage à l’étape suivante demande surtout : **durcissement, connectivité réelle, persistance partagée, observabilité standard, exécution asynchrone, gouvernance multi-instance.**

---

## 2. Plan Scale / Prod

### 2.1. Providers réellement production-ready
**État actuel** : abstraction provider propre, providers mock + réels branchables, fallback modèle/provider de base, health checks simples.
**Upgrade attendu** :
* appels async natifs
* streaming
* gestion fine des timeouts
* erreurs provider normalisées
* budget/cost réel par provider
* tracing par appel provider
* retry policy configurable

**Fichiers futurs probables** : 
`numax/providers/async_base.py`, `numax/providers/policies.py`, `numax/providers/costs.py`, `numax/providers/retries.py`

### 2.2. Persistance et mémoire partagée
**État actuel** : JSON local, continuité locale, journaux skills locaux, feedback learning local.
**Upgrade attendu** :
* stockage partagé entre instances
* sessions centralisées
* mémoire sémantique plus robuste
* lecture/écriture concurrente fiable

**Stack possible** : Redis (état rapide / coordination), SQLite/Postgres (journalisation durable), LanceDB / Qdrant / PGVector (mémoire sémantique).

**Fichiers futurs probables** : 
`numax/storage/base.py`, `numax/storage/local_json.py`, `numax/storage/sqlite.py`, `numax/storage/redis.py`, `numax/storage/vector.py`

### 2.3. Long-running tasks / workers
**État actuel** : flows synchrones, exécution locale séquentielle.
**Upgrade attendu** :
* tâches longues découplées
* reprise automatique
* supervision des jobs
* retry différé
* pause / resume explicites

**Stack possible** : Celery, Dramatiq, RQ, Temporal.

**Fichiers futurs probables** : 
`numax/jobs/queue.py`, `numax/jobs/worker.py`, `numax/jobs/scheduler.py`, `numax/jobs/state_machine_bridge.py`

### 2.4. Observabilité standardisée
**État actuel** : traces JSONL, diagnostics synthétiques, identité runtime.
**Upgrade attendu** :
* spans OTel
* corrélation run/session/tool/model/provider
* dashboards
* alerting
* analyse de goulots

**Stack possible** : OpenTelemetry, Jaeger, Grafana, Langfuse.

**Fichiers futurs probables** : 
`numax/obs/otel.py`, `numax/obs/spans.py`, `numax/obs/metrics_export.py`, `numax/obs/correlation.py`

### 2.5. Sécurité opératoire réelle
**État actuel** : permissions logiques, sandbox logique, kill switch.
**Upgrade attendu** :
* sandbox système réelle
* isolation des outils à risque
* classification avancée du risque
* secrets handling propre
* prompt injection defense plus robuste

**Fichiers futurs probables** : 
`numax/security/prompt_injection.py`, `numax/security/tool_risk_classifier.py`, `numax/security/secrets_policy.py`, `numax/sandbox/runtime_isolation.py`

### 2.6. Plateforme multi-user / multi-tenant
**État actuel** : sessions locales, API simple.
**Upgrade attendu** :
* auth
* RBAC
* ownership
* quotas
* isolation de sessions par utilisateur / équipe

**Fichiers futurs probables** :
`numax/auth/`, `numax/rbac/`, `numax/server/middleware/auth.py`, `numax/server/middleware/tenant.py`

---

## 3. Tableau des features NUMAX

Légende : 
✅ **Présent** : intégré réellement
🟡 **Partiel** : présent en v0.1/v1 mais encore léger
❌ **Manquant** : non encore intégré sérieusement

| Feature | Statut | Ce qu’on a déjà | Ce qu’il manque |
| :--- | :---: | :--- | :--- |
| **State global typé** | ✅ | NumaxState, runtime, budget, confidence, trace | Enrichissement futur seulement |
| **Node contract** | ✅ | prep / exec / post / fallback | Rien de critique |
| **Executable graph** | ✅ | graphe, transitions, flows | Visualisation / debug tooling |
| **FSM runtime** | ✅ | états explicites, degraded/halt | Outillage runtime plus riche |
| **Intent routing** | ✅ | route direct/retrieve, logique adaptative légère | Routing plus riche multi-classe |
| **Retrieval** | ✅ | moteur local + node + reranking léger | Retrieval externe / hybride |
| **Planner** | 🟡 | planner linéaire minimal | Planification profonde / multi-branch |
| **Answer engine** | ✅ | provider call + fallback provider/model | Fallback encore plus intelligent |
| **Critic** | ✅ | critic + calibration légère | Critic multi-check / multi-judge |
| **Budget control** | ✅ | budget tracking + stop/degraded | Coût réel multi-provider |
| **Confidence model** | ✅ | compréhension/source/output/safety | Meilleure agrégation / calibration |
| **Stop conditions** | ✅ | arrêt et dégradation explicites | Conditions plus contextuelles |
| **Kill switch** | ✅ | kill switch gouverné | Intégration plus large à runtime distribué |
| **Governance const.** | ✅ | priorités, conflit, politique interne | Gouvernance multi-tenant |
| **Tool registry** | ✅ | outils typés avec risque | Surface outillage plus riche |
| **Permission judge** | ✅ | allow / ask / deny | Règles plus fines par profil |
| **Sandbox** | 🟡 | sandbox logique | Vraie isolation système |
| **Memory continuity** | ✅ | save/load continuité | Backend partagé |
| **Memory promotion** | ✅ | working → episodic → semantic | Scoring plus intelligent |
| **Memory forgetting** | ✅ | oubli contrôlé | Oubli contextuel plus fin |
| **Memory consolid.** | ✅ | consolidation de patterns | Consolidation sémantique plus robuste |
| **Memory policy up.** | ✅ | policy update depuis history | Apprentissage plus structuré |
| **Artifact schema** | ✅ | types, qualité, trace, statut | Plus de types métier |
| **Artifact validation** | ✅ | validation minimale | Validation métier avancée |
| **Artifact rendering** | ✅ | texte / markdown | Renderers supplémentaires |
| **Artifact prod flow**| ✅ | flow artifact_output | Flows spécialisés par artifact |
| **Provider registry** | ✅ | registre providers | Auto-discovery plus avancé |
| **Model catalog** | ✅ | specs, roles, capabilities | Coûts/capacités plus précises |
| **Model resolver** | ✅ | préféré + fallbacks | Meilleure stratégie live |
| **Real providers** | 🟡 | OpenAI / Anthropic / Google / Ollama branch. | Async, streaming, coûts réels |
| **Provider fallback** | ✅ | fallback logique dans answer | Fallback prod plus avancé |
| **Learning router** | ✅ | feedback JSON local | Validation/stratégie plus robuste |
| **Learning model sel.**| ✅ | préférence simple JSON | Apprentissage plus riche |
| **Learning retrieval**| ✅ | boosts locaux | Meilleure boucle d’apprentissage |
| **Learning critic** | ✅ | offset/strict mode | Calibration plus statistique |
| **Feedback persist.** | ✅ | JSONL local | Meilleur schéma/validation |
| **Skills journal** | ✅ | journal JSON local | Migrations/versioning plus forts |
| **Skill apply/uninst.**| ✅ | journalisés | Effets réels sur runtime |
| **Skill replay** | ✅ | replay journal/explicite | Replay d’effets concrets |
| **Rollback** | ✅ | last_known_good | Rollback plus transactionnel |
| **Self change gov.** | ✅ | permission de mutation | Politiques plus fines |
| **Benchmark scenar.** | ✅ | scénarios clés | Couverture plus large |
| **Benchmark. basel.** | ✅ | 3 baselines | Baselines plus réalistes |
| **Benchmark. metrics**| ✅ | métriques système | Métriques plus fines |
| **Victory score** | ✅ | score agrégé + ranking | Justification par domaine |
| **Benchmark report** | ✅ | JSON + Markdown | Visualisations plus riches |
| **CLI** | ✅ | run / serve / config / benchmark / learning| UX plus avancée |
| **FastAPI server** | ✅ | routes de base | Auth, RBAC, jobs |
| **MCP minimal** | 🟡 | tools/list, tools/call | Surface plus complète |
| **Sessions** | ✅ | create/list/get | Persistance multi-user |
| **Traces** | ✅ | JSONL par run | OTel / spans |
| **Diagnostics** | ✅ | diagnostics de session | Dashboards |
| **Runtime identity** | ✅ | hash/identity | Drift detection plus complet |
| **Startup checks** | ✅ | checks simples | Checks infra plus larges |
| **Tests unitaires** | ✅ | beaucoup de briques testées | Couverture à élargir |
| **Tests intégration** | ✅ | flows + benchmark | Tests de résilience plus sévères |
| **Docs architecture** | ✅ | README archi complet | Docs spécialisées supplémentaires |
| **Docs benchmark** | ✅ | README preuve et mapping | Docs benchmark dédiées si besoin |

---

## 4. Tableau "Pièces du puzzle" → Feature impact

Ce tableau fait le lien entre les inspirations / briques discutées et les features concrètes de NUMAX.

| Pièce du puzzle | Features impactées dans NUMAX | Niveau d’absorption actuel |
| :--- | :--- | :--- |
| **PocketFlow** | graph execution, flows, recipes, discipline node-based | Élevé |
| **Goose** | usage d’outils, agent opérateur, délégation pratique | Moyen |
| **Skills systems** | apply/uninstall/replay/rollback | Élevé |
| **World-model** | memory, continuity, plan/action/critique loop | Moyen à élevé |
| **Gouvernance dure** | constitution, priorities, conflict resolver, kill switch | Élevé |
| **Artifact-first** | artifact schema, validators, renderers, output flow | Élevé |
| **Multi-provider** | registry, catalog, resolver, fallback | Élevé |
| **MCP / ecosystems**| MCP minimal, tool registry, permissioning | Moyen |
| **Adaptive policy** | router/model selector/ranker/critic feedback | Moyen |
| **Benchmarked** | scenarios, baselines, metrics, victory score | Élevé |
| **Memory hierarchies**| working/episodic/semantic + forgetting/consolidation | Élevé |
| **Mutation-safe** | journal JSON, replay, rollback, self-change | Élevé |

---

## 5. Ce qu’on a déjà vraiment utilisé

**Oui, on a déjà utilisé une grande partie des idées structurantes discutées.**
Mais il faut distinguer deux niveaux :

**Niveau architecture (OUI)**
On a déjà absorbé beaucoup : flow orchestration, cognition gouvernée, mémoire hiérarchique, artefacts, benchmark système, mutation réversible, providers/fallback, observabilité locale.

**Niveau maturité prod (EN CHANTIER)**
Pas encore totalement industriel : async réel, storage partagé, workers, sandbox réelle, auth/RBAC, observabilité standardisée.

---

## 6. Ce qu’il manque encore, en bref

| Manque | Pourquoi c’est important |
| :--- | :--- |
| **Providers async / streaming** | Passage à la vraie prod |
| **Storage partagé** | Mémoire/sessions multi-instance |
| **Workers / long tasks** | Tâches longues et reprise réelle |
| **OTel / observabilité standard**| Lisibilité scale |
| **Sandbox réelle** | Sécurité opératoire |
| **Skills à effets concrets** | Mutation vraiment utile |
| **Benchmark plus réaliste** | Preuve plus solide |
| **Artifact scoring métier** | Valeur finale mesurable |
| **RBAC / auth** | Passage plateforme |

---

## 7. Verdict final

NUMAX n’est plus un simple concept. NUMAX est déjà un framework système cohérent, avec une vraie colonne vertébrale. Ce qui reste à faire se concentre sur : le **scale**, la **prod**, la **sécurité réelle**, l'**infra distribuée** et la **preuve expérimentale plus dure**.

> NUMAX a déjà absorbé la majorité des pièces du puzzle structurantes. Ce qui manque maintenant n’est plus le cœur du système, mais son durcissement, sa preuve forte, et son passage en échelle réelle.
