# NUMAX

NUMAX est un **cortex agentique gouverné**.

Son objectif n’est pas seulement de répondre à une demande. Son objectif est de transformer une intention en trajectoire d’exécution contrôlée puis en artefact structuré, avec :
* compréhension,
* routage,
* récupération de contexte,
* planification,
* exécution,
* critique,
* mémoire,
* gouvernance,
* benchmark,
* mutation contrôlée,
* observabilité,
* continuité.

En une phrase :
> NUMAX n’essaie pas d’être un meilleur modèle. NUMAX essaie d’être un **meilleur système**.

---

## 1. Pourquoi NUMAX existe

Les systèmes classiques de type :
* LLM seul,
* LLM + tools,
* LLM + tools + mémoire légère,

...restent souvent faibles sur :
* les tâches longues,
* la robustesse après erreur,
* la continuité inter-session,
* la gouvernance,
* le contrôle coût/qualité,
* l’évolution sûre du système lui-même.

NUMAX est construit pour traiter précisément ces faiblesses.

---

## 2. La thèse centrale

NUMAX gagne si le système démontre qu’il fait mieux qu’un setup naïf sur cinq axes :
1. robustesse sur tâches longues
2. récupération après erreur
3. contrôle coût / qualité
4. continuité inter-session
5. mutation gouvernée et réversible

Autrement dit :
> La victoire de NUMAX n’est pas une victoire de réponse. C’est une victoire de **trajectoire d’exécution**.

---

## 3. Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt
```

**Flows utiles**
```bash
make run
make run-retrieval
make run-plan
make run-artifact
```

**Serveur**
```bash
make serve
```

**Tests**
```bash
make test
make test-unit
make test-integration
```

**Benchmark**
```bash
numax benchmark-run
```

**Config / learning**
```bash
numax config-show
numax learning-show
```

---

## 4. Architecture condensée

```text
User Intent
   ↓
NumaxState
   ↓
Intent Router
   ↓
Retrieve / Planner / Answer
   ↓
Critic
   ↓
Artifact
   ↓
Memory / Trace / Diagnostics
   ↓
Governance / Runtime Controls
```

NUMAX repose sur une séparation nette :
* **Déterministe** pour la gouvernance.
* **Adaptatif** pour certaines optimisations.

**Ce qui reste dur :** FSM, kill switch, priorités, permissions, rollback, identité runtime.
**Ce qui peut apprendre légèrement :** routing, model selection, retrieval ranking, critic calibration, certaines politiques mémoire.

---

## 5. Ce que NUMAX contient déjà

* **Noyau d’exécution** : état typé, nœuds, graphe exécutable, flows.
* **Cognition** : intent router, retrieve, planner, answer, critic.
* **Runtime** : budget, confiance, stop conditions, continuité.
* **Gouvernance** : constitution, priorités, résolution de conflit, kill switch, permissions outils, sandbox logique.
* **Sortie utile** : artefacts typés, validation d’artefacts, rendu d’artefacts.
* **Évolution du système** : journal JSON local de skills, apply / uninstall, replay, rollback, self-change gouverné.
* **Observabilité** : traces JSONL, logs, diagnostics, identité runtime, startup checks.
* **Infra** : providers, catalog modèles, resolver, server FastAPI, CLI, MCP minimal.
* **Preuve** : benchmark runner, scénarios, baselines, victory score.

---

## 6. Preuve / Benchmark

**Baselines comparées**
* `llm_only`
* `llm_tools`
* `llm_tools_memory`

**Scénarios benchmarkés**
tâche longue, retrieval failure, provider failure, budget overflow, continuity resume, mutation rollback.

**Métriques suivies**
`task_success_rate`, `artifact_validity_rate`, `recovery_success_rate`, `continuity_resume_score`, `budget_efficiency_score`, `mutation_safety_score`, `victory_score`.

**Sens du victory score**
Le `victory_score` ne cherche pas à dire “le texte est meilleur”. Il cherche à dire :
> quel système a la meilleure capacité globale à aller au bout, survivre, reprendre, évoluer, et produire proprement.

---

## 7. Mapping des pièces du puzzle

| Pièce / inspiration | Ce qu’on en reprend dans NUMAX | Statut d’intégration | Ce qui manque encore |
| :--- | :--- | :--- | :--- |
| **PocketFlow** | logique de flow, graph orchestration, nœuds, recettes | Élevé | plus de recipes exécutables réelles |
| **Goose** | logique d’agent opérateur, usage borné d’outils, délégation | Moyen | UX agent dev plus directe, sandbox réelle |
| **Skills systems** | apply / uninstall / replay / rollback | Élevé | skills à effets concrets |
| **World-model** | mémoire, continuité, boucle plan/action/critique | Moyen à élevé | simulation plus profonde |
| **Gouvernance dure** | constitution, priorities, conflict resolver, kill switch | Élevé | gouvernance multi-user |
| **Artifact-first** | artifact schema, validators, renderers, output flow | Élevé | scoring métier avancé |
| **Multi-provider layer**| registry, catalog, resolver, fallback | Élevé | async, streaming, coûts réels |
| **MCP/tool ecosyst.** | MCP minimal, tool registry, permissioning | Moyen | surface MCP plus large |
| **Adaptive policy** | router/model selector/ranker/critic feedback | Moyen | boucle d’apprentissage plus robuste |
| **Benchmarked sys.** | scenarios, baselines, metrics, victory score | Élevé | cas encore plus réalistes |
| **Memory hierarchies**| working/episodic/semantic + forgetting/consolidation | Élevé | promotion plus intelligente |
| **Mutation-safe sys.** | journal JSON, replay, rollback, self-change | Élevé | migrations/versioning plus forts |

---

## 8. Tableau des features

Légende : ✅ Présent | 🟡 Partiel | ❌ Manquant

| Feature | Statut | Ce qu’on a déjà | Ce qu’il manque |
| :--- | :---: | :--- | :--- |
| **State global typé** | ✅ | NumaxState, runtime, budget, confidence, trace | enrichissement futur |
| **Node contract** | ✅ | prep / exec / post / fallback | rien de critique |
| **Executable graph** | ✅ | graphe, transitions, flows | visualisation |
| **FSM runtime** | ✅ | états explicites, degraded/halt | outillage runtime |
| **Intent routing** | ✅ | route direct/retrieve, adaptative légère | routing plus riche |
| **Retrieval** | ✅ | moteur local + node + reranking léger | retrieval externe / hybride |
| **Planner** | 🟡 | planner linéaire minimal | planification profonde |
| **Answer engine** | ✅ | provider call + fallback provider/model | fallback plus intelligent |
| **Critic** | ✅ | critic + calibration légère | critic multi-judge |
| **Budget control** | ✅ | budget tracking + stop/degraded | coût réel multi-provider |
| **Confidence model** | ✅ | compréhension/source/output/safety | meilleure agrégation |
| **Kill switch** | ✅ | kill switch gouverné | intégration runtime distribué |
| **Tool registry** | ✅ | outils typés avec risque | surface outillage plus riche |
| **Sandbox** | ✅ | isolation d'exécution, sandbox logique | intégration containers |
| **Memory continuity** | ✅ | save/load continuité | backend partagé |
| **Memory promotion** | ✅ | working → episodic → semantic | scoring plus intelligent |
| **Memory forgetting** | ✅ | oubli contrôlé | oubli contextuel plus fin |
| **Memory consolid.** | ✅ | consolidation de patterns | consolidation sémantique |
| **Artifact schema** | ✅ | types, qualité, trace, statut | plus de types métier |
| **Artifact validation** | ✅ | validation minimale | validation métier avancée |
| **Real providers** | ✅ | OpenAI / Anthropic / Google / Ollama async | streaming natif complet |
| **Provider fallback** | ✅ | fallback logique dans answer | fallback prod plus avancé |
| **Skills journal** | ✅ | journal JSON local | migrations/versioning plus forts |
| **Skill replay** | ✅ | replay journal/explicite | replay d’effets concrets |
| **Rollback** | ✅ | last_known_good | rollback plus transactionnel |
| **Benchmark scen.** | ✅ | scénarios clés | couverture plus large |
| **Victory score** | ✅ | score agrégé + ranking | justification par domaine |
| **FastAPI server** | ✅ | routes de base, auth, RBAC, admin, jobs | - |
| **MCP minimal** | 🟡 | tools/list, tools/call | surface plus complète |
| **Traces** | ✅ | JSONL par run | OTel / spans |
| **Diagnostics** | ✅ | diagnostics de session | dashboards |
| **Tests intégration** | ✅ | flows + benchmark | tests de résilience plus sévères |

---

## 10. Roadmap 30 / 60 / 90 jours

### J+30 — Stabiliser et prouver
**Objectif** : Passer de gros framework cohérent à système prouvable et proprement mesuré.
* **Durcir le benchmark** : brancher plus de scénarios réels, cas d’échec provider, budget/degraded.
* **Renforcer les providers** : fallback plus robuste, erreurs normalisées, meilleure comptabilité.
* **Rendre les skills plus crédibles** : journal plus stable, rejouabilité vérifiée, rollback testé.
* **Augmenter la couverture de test** : résilience runtime, provider failure, benchmark integrity.

### J+60 — Monter en maturité opératoire
**Objectif** : Passer de système local avancé à runtime prêt à sortir du labo.
* ✅ **Providers async / streaming** : appels async natifs, policies retry/timeout claires.
* ✅ **Persistance plus sérieuse** : backend local durable SQLite, stores Redis/Postgres init.
* ✅ **Observabilité standardisée** : OTel natif, manager de spans, export traces structurées.
* 🟡 **Artefacts plus métier** : scoring par type, acceptance criteria plus forts.

### J+90 — Préparer le Scale / Prod
**Objectif** : Passer de runtime local puissant à noyau plateforme scalable.
* ✅ **Jobs et tâches longues** : architecture Repo/Service/Worker locale en place.
* ✅ **Sécurité réelle** : module Guardian (isolation sandbox, kill switches, RBAC).
* ✅ **Multi-user / RBAC** : modèle UserIdentity complet (Admin/Viewer, middlewares).
* **Mémoire partagée** : backend commun, continuité multi-instance, mémoire sémantique.

---

## 11. Priorisation nette

Si on tranche durement, l’ordre des vrais chantiers est :
1. benchmark plus réel
2. providers plus robustes
3. skills réellement transformantes
4. sandbox réelle
5. scoring métier des artefacts
6. async / workers
7. storage partagé
8. auth / RBAC
9. observabilité standardisée

---

## 12. Verdict final

NUMAX n’est plus un simple concept. NUMAX est déjà un framework système cohérent, avec une vraie colonne vertébrale.

**Ce qui est déjà fort :** architecture, gouvernance, mémoire, artefacts, benchmark, mutation réversible, observabilité locale.
**Ce qui reste à faire :** scale, prod, sécurité réelle, infra distribuée, preuve expérimentale plus dure.

La bonne phrase pour résumer :
> NUMAX a déjà absorbé la majorité des pièces du puzzle structurantes. Ce qui manque maintenant n’est plus le cœur du système, mais son durcissement, sa preuve forte, et son passage en échelle réelle.
