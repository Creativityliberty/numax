# NUMAX : Theory of Victory

Ce document formalise formellement *pourquoi* et *comment* NUMAX gagne. Il ne s'agit pas de vœux pieux, mais d'une doctrine falsifiable.

## A. La Thèse Fondamentale
**NUMAX gagne non pas par l'intelligence brute d'un modèle (LLM), mais par sa gouvernance systémique.** 
Il découple la réflexion de l'exécution, force une critique interne stricte, et protège sa trajectoire par des seuils mathématiques (Kill Switch, Continuité, Perms). L'intelligence émerge de l'orchestration FSM, pas du prompt magique.

## B. Les Adversaires (Contre qui se compare-t-on ?)
Pour prouver notre valeur, le Benchmark Fondateur mesurera NUMAX contre :
1. **LLM Seul** (Prompting classique zero-shot/few-shot)
2. **LLM + Tools** (Agent ReAct simple sans mémoire de long terme)
3. **LLM + Tools + Mémoire Simple** (Agent avec historique RAG basique, mais sans gouvernance stricte FSM)

## C. Les 5 Promesses Testables (Ce que NUMAX doit battre)
Lors du benchmark, NUMAX garantit statistiquement :
1. **Une meilleure robustesse sur les tâches longues** (Moins de dérive, grâce au Planner et Critic).
2. **Une meilleure récupération après erreur** (Self-correction via les politiques d'erreurs Retry/Degrade sans crash aveugle).
3. **Un meilleur contrôle du Coût/Qualité** (Le Budget tracker limite l'hémorragie token financière).
4. **Une meilleure continuité inter-session** (L'historique n'est pas perdu, il est sérialisé et restaurable en mémoire de travail).
5. **Une meilleure gouvernance des mutations** (Le code de l'agent ne mute pas sans audit de sécurité préalable).

## D. Conditions de Défaite (Ce qui invalide le système)
L'architecture NUMAX est considérée comme un échec (ou une sur-ingénierie inutile) si l'une des conditions suivantes est vérifiée :
- **Si le Benchmark ne montre aucun gain** de qualité ou de résilience par rapport à un agent ReAct basique.
- **Si la Gouvernance coûte trop cher** (Par ex. le Critic consomme 70% des tokens sans améliorer l'output).
- **Si la Continuité (Mémoire) n'apporte aucun bénéfice** (L'agent tourne en rond même en relisant ses échecs passés).
- **Si la Mutation Contrôlée ralentit trop le développement** pour la valeur qu'elle produit.

## E. Axe Principal de Différenciation
> *"NUMAX n'est pas un meilleur modèle, c'est un meilleur système."*

Le modèle sous-jacent (GPT-4, Claude 3, Gemini, Llama) n'est qu'un processeur interchangeable. Le véritable cerveau est la machine à états (FSM).
