# NUMAX — Benchmark & Preuve

## 1. Ce que NUMAX doit prouver

NUMAX ne cherche pas à être "un meilleur LLM". NUMAX doit prouver qu'il est un **meilleur système** capable de gouverner l'exécution.
Pour cela, nous ne le mesurons pas sur la beauté littéraire d'une réponse, mais bien sur sa résilience. 

Il doit battre systématiquement au moins trois baselines :
1. `llm_only`
2. `llm_tools`
3. `llm_tools_memory`

Le système est évalué sur sa :
* **Réussite de tâche**
* **Validité d’artefact**
* **Récupération après erreur**
* **Continuité inter-session**
* **Sécurité de mutation**
* **Efficacité coût/tokens**

## 2. Scénarios Benchmark

Les tests ne sont pas des prompts simples ("Quelle est la capitale de la France ?"). Ce sont des *scénarios de stress* :

1. **Tâche longue (Long Task)** : Planification multi-étapes avant la réponse.
2. **Retrieval failure** : Le contexte ramené est vide ou hors-sujet. NUMAX doit-il forcer une réponse ou dégager gracieusement ?
3. **Provider failure** : Le modèle principal plante (timeout, ban). Le système doit exploiter son Fallback Provider.
4. **Budget overflow** : Le pipeline consomme trop de tokens. Le Juge (Budget) doit déclencher un mode dégradé avant la ruine.
5. **Continuity resume** : L'état d'hier est rechargé. Le système doit promouvoir ses souvenirs pour reprendre le contexte contextuellement pertinent.
6. **Mutation rollback** : Une "skill" altérée est injectée. Le système doit prouver qu'il sait restaurer un `last_known_good` et reprendre le service.

## 3. Les Métriques

Le rapport généré résume les scores suivants (allant de 0.0 à 1.0) :

* `task_success_rate` : Pourcentage de flows allant jusqu'au bout sans crash fatal non intercepté.
* `artifact_validity_rate` : Le rendu final passe-t-il la validation de schéma strict ?
* `recovery_success_rate` : En cas de runtime degraded, l'état final est-il intact ?
* `continuity_resume_score` : Score simulant la qualité du rechargement mnésique.
* `budget_efficiency_score` : Ratio `Succès / Coût USD + Tokens`.
* `mutation_safety_score` : Probabilité de retomber sur ses pattes après l'injection de skills (test du rollback/replay).

## 4. Le "Victory Score"

Le score ultime qui agrège le tout est le `victory_score`.
Il est pondéré ainsi :
* 30% : Succès de la tâche
* 20% : Récupération
* 20% : Continuité
* 20% : Sécurité des mutations
* 10% : Validité des artefacts

**Le Sens du Victory Score :**
> "Quel système a la meilleure capacité globale à aller au bout, survivre, reprendre, évoluer, et produire proprement ?"

## 5. La Preuve Attendue & Localisation

Si NUMAX veut être crédible en tant que framework post-Agent, il doit montrer dans ses rapports que :
1. Son `continuity_resume_score` dépasse les baselines.
2. Son `mutation_safety_score` dépasse de loin les setups naïfs.
3. Son `recovery_success_rate` est quasi-infaillible.
4. Le coût monétaire ou computationnel ajouté par le Graphe est **justifiable**.

Les preuves vivent dans le code :
* Injection des tests : `benchmarks/runner.py` et `benchmarks/report.py`
* Données sorties : `benchmarks/outputs/benchmark_report.json` et `.md`
