# La Frontière Cognitive : Déterministe vs Appris

Pour que NUMAX ne devienne jamais une "boîte noire floue" où les erreurs sont inexplicables, l'architecture trace une frontière absolue entre ce qui est régi par des mathématiques strictes (Déterministe) et ce qui est optimisé par l'historique et l'IA (Appris).

## 1. La Zone Déterministe (Le Code en Dur)
Ces éléments **garantissent la survie, la sécurité et la traçabilité** de l'agent. Ils sont audités mathématiquement et logiquement. L'agent n'a *pas le droit* de les modifier seul de manière empirique sans le processus lourd de Mutation.

* **Les Invariants et la Constitution** (Règles fondamentales immuables).
* **Le Graph FSM (Machine à États)** (Le cheminement Route -> Retrieve -> Reason -> Critic -> Tool est gravé dans le marbre).
* **Le Kill Switch** (L'arrêt du système via Budget ou Safety threshold est mathématique et non négociable).
* **Les Seuils de Sécurité & Permission Gates** (Guardian + Sandbox rules).
* **Le Versioning & Ownership** (La cryptographie de l'Identity).
* **Le Pipeline de Mutation & Rollback** (La procédure de mise à jour s'exécute de manière déterministe).

## 2. La Zone Apprise (L'Optimisation)
Ces éléments **garantissent l'efficience, la personnalisation et la progression** de l'agent. Ils s'affinent au fil des itérations, des réussites, et des logs d'erreurs (Feedback Loop).

* **Le Routing Fin** (Classifier de mieux en mieux les intentions des utilisateurs).
* **Le Ranking Retrieval** (Apprendre quels documents RAG sont réellement utiles selon le contexte).
* **La Sélection de Modèle (Model Selection)** (Rétrograder vers un modèle moins cher si la tâche est prouvée asynchrone et simple).
* **La Calibration du Critic** (Ajuster la sévérité du juge interne si les artefacts sont rejetés abusivement).
* **La Promotion Mémoire (Working -> Episodic -> Semantic)** (L'agent apprend ce qui vaut la peine d'être conservé à vie).
* **Le Scoring de Plan/Simulation** (Choisir les meilleurs chemins d'actions).

## 3. Matrice de Différenciation Architecturale

| Composant | Type | Justification / Raison |
| :--- | :--- | :--- |
| **FSM (Graphe Core)** | 🔒 Déterministe | Traçabilité absolue, sécurité et audit des transitions. |
| **Kill Switch** | 🔒 Déterministe | Algorithme vital d'arrêt d'urgence. Non négociable. |
| **Sandbox / Permissions** | 🔒 Déterministe | Prévention mathématique des accès systèmes dangereux. |
| **Model Selector** | 🧠 Appris | Optimisation dynamique de la balance Qualité/Coût. |
| **Retrieval Ranker** | 🧠 Appris | Amélioration progressive de l'accès au contexte interne. |
| **Memory Promotion** | ⚖️ Hybride | Seuil mathématique (score) + Intelligence du choix pour oublier le bruit. |

> **Règle d'Architecture** : Chaque fois qu'une fonctionnalité est ajoutée à NUMAX, les développeurs doivent répondre à cette question : *"Est-ce un mécanisme de Sécurité (Déterministe) ou d'Optimisation (Appris) ?"*
