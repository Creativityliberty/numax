# NUMAX — Scale / Prod Plan + Features Map

Ce document complète le README principal et le README d’architecture.
Il sert à répondre à deux questions :
1. **Comment NUMAX passe d'un framework local avancé à un runtime scale/prod ?**
2. **Quelles features sont déjà présentes, partiellement présentes, ou encore manquantes ?**

---

## 1. Le Constat : L'Architecture est Figée, Place à l'Opérationnel

Avec NUMAX V2, le design n'est plus en chantier principal. La boucle OODA gouvernée (Routing, Memory, Critic, Sandbox, Benchmark, Skills JSON) est fermement établie et testée mathématiquement. 

> **L'upgrade maintenant, c'est l'opérationnalisation.**

Le passage d'un excellent framework local à un **véritable runtime déployable (Multi-tenant, Long-Running, Réparti)** repose exclusivement sur les 4 Piliers de Scale détaillés ci-dessous.

### Pilier 1 : Connectivité Providers Réellement Async
Le graphe actuel invoque les providers de manière abstraite. Pour tenir la charge réseau et les spécificités des LLMs modernes, l'exécution doit passer 100% Async.
- **Async/Await Natif** : Remplacer les wrappers bloquants.
- **Streaming** : Interaction real-time avec le client.
- **Tracking / Fallback** : Switch sur timeout de 3s, ou blacklist temporaire d'un provider si erreur 429.

### Pilier 2 : Persistance Base de Données (Shared Memory)
L'Hippocampe (la mémoire hiérarchisée) et le Skills Journal écrivent pour l'instant dans des flatfiles `data/state/*.json`.
- **État Partagé** : Pivoter sur **PostgreSQL** ou **Redis** pour un cluster Kubernetes stateless.
- **Mémoire Sémantique** : Intégration d'une DB Vectorielle (**LanceDB**, **Qdrant**, **PGVector**).
- **Multi-Tenant (RBAC & Auth)** : Isoler les mémoires et le budget global par `user_id` et `session_id`.

### Pilier 3 : Long-Running Tasks & Workers
L'itération de boucle du graphe FSM s'exécute linéairement. Si une "Deep Research" nécessite 4 heures, le serveur HTTP plantera.
- **Queues & Workers** : Découpler l'API de l'exécution via **Temporal.io**, **Celery**, ou **RabbitMQ**.
- **Wake & Sleep Mode** : Le FSM s'endort en DB s'il attend un input humain.
- **Réveil Asynchrone** : Les Workers récupèrent la tâche et relancent le graphe OODA précisément à l'étape correspondante.

### Pilier 4 : Observabilité Standardisée (OTel)
La `state.trace` (JSONL local) est impuissante pour débugger un système en essaim traitant des milliers d'intentions.
- **OpenTelemetry (OTel)** : Émission de Spans imbriqués.
- **Dashboards** : En direct via **Grafana**, **Jaeger**, ou **Langfuse**.
- **Correlation** : Lier `session_id`, `tool_id`, `model_used` et `latency`.

---

## 2. Implémentation Pratique (Stack & Fichiers Ciblés)

En complément des piliers, voici l'impact direct sur la structure du repo.

**Providers Production-ready**
Fichiers probables : `numax/providers/async_base.py`, `numax/providers/policies.py`, `numax/providers/costs.py`, `numax/providers/retries.py`

**Persistance (Redis/Vector)**
Fichiers probables : `numax/storage/base.py`, `numax/storage/local_json.py`, `numax/storage/sqlite.py`, `numax/storage/redis.py`, `numax/storage/vector.py`

**Jobs & Workers (Celery/Temporal)**
Fichiers probables : `numax/jobs/queue.py`, `numax/jobs/worker.py`, `numax/jobs/scheduler.py`, `numax/jobs/state_machine_bridge.py`

**Observabilité OTel**
Fichiers probables : `numax/obs/otel.py`, `numax/obs/spans.py`, `numax/obs/metrics_export.py`, `numax/obs/correlation.py`

**Sécurité & Isolation**
Fichiers probables : `numax/security/prompt_injection.py`, `numax/security/tool_risk_classifier.py`, `numax/sandbox/runtime_isolation.py`

**Plateforme Multi-tenant (Auth / RBAC)**
Fichiers probables : `numax/auth/`, `numax/rbac/`, `numax/server/middleware/auth.py`, `numax/server/middleware/tenant.py`

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
| **Sandbox** | 🟡 | sandbox logique | Vraie isolation OS/système |
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
| **Runtime identity** | ✅ | hash/identity | Drift detection complet |
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

## 6. Synthèse de la Route de Scale

| Chantier de Scale | Pourquoi c’est critique |
| :--- | :--- |
| **Providers async / streaming** | Tenir 50+ requêtes LLM lourdes en parallèle sans écrouler l'interface. |
| **Storage partagé (Redis/Vector)** | Partager la Session Continuity et l'Hybrid Search RAG sur 10 Pods stateless. |
| **Workers / long tasks (Temporal)**| Éviter les pannes réseau si un Workflow RAG profond dure 3 heures. |
| **OTel / observabilité standard**| Tracer une hallucination à travers 5 nœuds sans ouvrir de fichiers logs en SSH. |
| **Sandbox réelle (Firecracker)** | Isoler le code généré par l'agent pour éviter la corruption du host. |
| **Skills à effets concrets** | Permettre à NUMAX d'installer lui-même ses propres packages MCP. |
| **Benchmark plus réaliste** | Modéliser une panne de Cloudflare dans la notation de robustesse de NUMAX. |
| **Artifact scoring métier** | Valider la syntaxe et sémantique métier des JSON/Code plutôt qu'uniquement via LLM. |
| **RBAC / Auth Multicompte** | Lancer NUMAX pour des équipes B2B avec des Data Silos stricts. |

L'accomplissement de ces points marquera le point où NUMAX V3 ne sera plus jugé sur son intelligence structurelle, mais sur sa capacité à traiter **10,000 requests asynchrones concurrentes avec une perte de mémoire de 0% et un crash système inexistant**.
