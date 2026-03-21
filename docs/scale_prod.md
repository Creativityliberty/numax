# NUMAX — Scale & Prod (Phase 3)

## Le Constat : L'Architecture est Figée, Place à l'Opérationnel

Avec NUMAX V2, le design n'est plus en chantier principal. La boucle OODA gouvernée (Routing, Memory, Critic, Sandbox, Benchmark, Skills JSON) est fermement établie et testée mathématiquement. 

> **L'upgrade maintenant, c'est l'opérationnalisation.**

Le passage d'un excellent framework local à un **véritable runtime déployable (Multi-tenant, Long-Running, Réparti)** repose exclusivement sur les 4 Piliers de Scale détaillés ci-dessous.

---

## Pilier 1 : Connectivité Providers Réellement Async

Le graphe actuel invoque les providers de manière abstraite. Pour tenir la charge réseau et les spécificités des LLMs modernes, l'exécution doit passer 100% Async.

**Objectifs d'Industrialisation :**
- Remplacer les appels synchrones (ex: `httpx.Client()` ou wrappers bloquants) par du **`async/await` natif complet**.
- Implémenter le **Streaming** des réponses pour permettre une interaction real-time avec le client.
- Renforcer le Tracking via `runtime/budget.py` avec le décompte granulaire des Prompt/Completion tokens à la volée.
- Complexifier le **Fallback multi-provider** (ex: switch sur timeout de 3s, ou blacklist temporaire d'un provider si retour `429 Too Many Requests`).

---

## Pilier 2 : Persistance Base de Données (Shared Memory)

L'Hippocampe (la mémoire hiérarchisée) et l'Évolution (le Skills Journal), bien que logiquement brillants, écrivent pour l'instant dans des flatfiles `data/state/*.json` locaux.

**Objectifs d'Industrialisation :**
- **État Partagé** : Pour qu'un cluster de pods Kubernetes NUMAX soit *stateless*, l'état des FSM et la continuité mémoire doivent pivoter sur **PostgreSQL** ou **Redis**.
- **Mémoire Sémantique** : L'intégration d'une DB Vectorielle (ex: **LanceDB**, **Qdrant**, **Pinecone**) remplaçant la recherche simpliste sur textes.
- **Multi-Tenant (RBAC & Auth)** : Isoler les mémoires et le budget global par `user_id` et par `session_id`, interdisant la contamination inter-utilisateurs.

---

## Pilier 3 : Long-Running Tasks & Workers

L'itération de boucle du graphe FSM s'exécute linéairement et de bout en bout dans le thread appelant. Si une "Deep Research" nécessite 4 heures et 100 requêtes RAG, le serveur plantera sous le timeout HTTP.

**Objectifs d'Industrialisation :**
- Découpler l'API d'ingestion de l'exécution pure via un gestionnaire de queue (**Temporal.io**, **Celery**, ou un simple **RabbitMQ**).
- **Wake & Sleep Mode** : Le FSM doit pouvoir "s'endormir" (en serialisant son `NumaxState` en DB) s'il attend le retour d'un humain (Confirmation d'Outil bloquante) ou d'un long script sandbox.
- **Réveil Asynchrone (Polling / Webhook)** : Les Workers récupèrent la tâche, injectent la réponse externe, et relancent le graphe OODA précisément à l'étape `post()`.

---

## Pilier 4 : Observabilité Standardisée (OTel)

La `state.trace` (JSONL locaux) est impuissante pour débugger un système en essaim traitant des milliers d'intentions.

**Objectifs d'Industrialisation :**
- Intégration complète du standard **OpenTelemetry (OTel)**.
- Émission de **Spans** imbriqués (ex: `Run > Routing > API Call Anthropic > Critic`).
- Tableaux de bord en direct via **Grafana**, **Jaeger**, ou un backend spécialisé Agent comme **Langfuse/Smith**.
- Correlation native (Lier `session_id`, `tool_id`, `model_used` et `latency`) pour voir instantanément dans quel nœud le système ralentit.

---

## Synthèse de Route (KPI)

L'accomplissement de ce manifeste marquera le point où NUMAX V3 ne sera plus jugé sur son intelligence structurelle (déjà actée par le Victory Score), mais sur sa capacité à traiter **10,000 requests asynchrones concurrentes avec une perte de mémoire de 0% et un crash système inexistant**.
