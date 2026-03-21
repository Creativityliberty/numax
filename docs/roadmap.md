# NUMAX — Roadmap 30 / 60 / 90 Jours

## Le Verdict Post-V2

> **"NUMAX a déjà intégré la majorité des pièces du puzzle structurantes. Ce qui manque désormais, ce sont surtout la maturité opératoire, la preuve expérimentale forte, et l’approfondissement de quelques couches critiques."**

Nous ne sommes plus face à une idée ou un "wrapper LLM". C'est un **système cognitif gouverné**.
Le cœur tourne et se défend (`routing`, `critic`, `memory`, `governance`, `skills`, `benchmarks`). 

La suite se concentre sur le durcissement, le "Scale" et le "Real-World Proof". L'ordre d'implémentation suit les priorités de la **Theory of Victory**.

---

## Plan à 30 Jours : Le "Real-World Benchmark" & Fallbacks 

L'objectif est de s'assurer que face aux pires conditions d'API, le système NUMAX continue de router intelligemment et de justifier son existence via des métriques indiscutables.

1. **Benchmark Plus Infaillible** 
   - Remplacer les "simulations d'échec" par des timeouts d'API réels dans les scénarios de benchmark.
   - Améliorer l'Output `benchmarks_report.md` avec des Delta (+15% vs llm_tools).
2. **Fallback Providers Complets en Prod**
   - Brancher massivement le réseau réel : OpenAI ↔ Anthropic ↔ Google ↔ Ollama.
   - Si Claude 3.5 refuse pour "Overloaded", le noeud `answer.py` switche en 5ms sur `gpt-4o-mini` via l'autodétection. Coût réel / tracking de token.
3. **Apprentissage Léger Structurant** 
   - Bouclage effectif des feedbacks : le retour du Critic modifie durablement le `learning/router.py` pour un profil utilisateur donné.

---

## Plan à 60 Jours : Outils, Mutations & Agents Connectés

Le focus bascule vers l'action de NUMAX sur le monde (via des Tools) de manière sûre, tout en gardant sa gouvernance.

1. **Skills et Mutations "Vraiment" Invasives** 
   - Installer de "vraies" skills (ex: une intégration GitHub native, un script Python custom) qui altèrent le RAG en profondeur. S'appuyer massivement sur `rollback_to(LKG)` via le `journal.json` à la moindre erreur fatale.
2. **Sandbox Réelle & Isolation (Execution Engine)**
   - Exécuter les outputs de code produit (python, scripts JS) dans un container sécurisé (Docker/Firecracker), et non plus dans une simple "sandbox logique".
3. **Artifact Scoring Job-Oriented** 
   - Des validateurs d'artefact qui connaissent les schémas métiers (ex: "Valide si l'artefact généré est un manifest Kubernetes valide" via parseur AST/YAML natif, au lieu d'un jugement LLM approximatif).

---

## Plan à 90 Jours : La Plateforme (Multi-Tenant & Async)

L'objectif est d'abandonner l'exécution synchrone, terminale, monothread, pour atteindre la "Production Scale".

1. **RBAC, Auth & Plateforme Multicompte** 
   - Multi-tenant data structures : Un `NUMAX_ENV` par utilisateur. L'Hippocampe (`memory/`) doit pivoter sur de vraies DB (Postgres/LanceDB) plutôt que sur des `json` flatfiles indexés localement.
2. **Deep Planner & Asynchronous Jobs (Workers/Queue)** 
   - Le graphe FSM actuel tourne linéairement. Nous utiliserons Temporal, Celery ou un RabbitMQ pour autoriser des "Long-Running Tasks" de 5 Heures avec reprise, sleep, et polling (ex: "Code moi ce backend, fais des tests internet et reviens vers moi").
3. **Observabilité (OTel Dashboards)**
   - Remplacer les arrays de traces JSONL par de l'OpenTelemetry complet. Envoyer les traces de confiance, noeuds et budgets vers un serveur Jaeger ou Grafana Tempo. Dashboard complet du Cortex NUMAX live.
