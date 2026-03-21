# NUMAX — Known Limitations

Ce document liste les limites connues de NUMAX v1.

Le but n’est pas de diminuer NUMAX. Le but est d’empêcher la confusion entre :
- Ce qui est réellement supporté.
- Ce qui est partiellement supporté.
- Ce qui reste futur.

## 1. Position générale

NUMAX v1 est déjà un framework système cohérent et sérieux. Mais NUMAX v1 n’est pas encore :
- Une plateforme distribuée complète.
- Une couche sandbox dure.
- Un système multi-tenant mature.
- Ni un runtime production-grade final sur tous les axes.

## 2. Providers

### 2.1. Providers réels
Les providers réels existent et sont branchables. Mais ils restent encore moins matures que la colonne vertébrale système elle-même.

**Limites :**
- Surface partielle.
- Streaming pas encore uniformisé partout.
- Coûts réels pas encore complètement instrumentés.
- Comportement réseau pas encore durci sur tous les cas.

## 3. Async

NUMAX a une base async. Mais la couche async n’est pas encore la voie principale la plus durcie du système.

**Limites :**
- Intégration progressive.
- Tous les flows ne sont pas encore nativement async end-to-end.
- Instrumentation async encore simple.

## 4. Storage

La couche storage est abstraite. C’est une force.
Mais en v1, le backend le plus sûr reste encore :
- JSON local
- SQLite

**Limites :**
- Redis/Postgres préparés mais pas encore validés comme voie par défaut.
- Pas encore de stratégie de migration de schéma complète.
- Concurrence avancée non encore durcie sur tous les backends.

## 5. Jobs / workers

NUMAX possède une couche jobs locale exploitable.

**Limites :**
- Ce n’est pas encore une queue distribuée complète.
- Pas encore de retries avancés distribués.
- Pas encore de reprise orchestrée type Temporal/Celery.

## 6. Observabilité

NUMAX écrit déjà des traces, spans et métriques structurées localement.

**Limites :**
- Pas encore d’export OTel réel branché.
- Pas encore de dashboard standard.
- Pas encore de corrélation infra complète.

## 7. Auth / RBAC

NUMAX a maintenant une base auth/RBAC.

**Limites :**
- Middleware simple.
- Pas encore d’auth forte.
- Pas encore de tokens/session/auth provider réels.
- Pas encore de multi-tenant mature.

## 8. Sandbox

NUMAX possède une sandbox bornée plus concrète qu’une simple abstraction logique.

**Limites :**
- Pas encore d’isolation dure type container.
- Allowlist encore simple.
- Politique de risque encore limitée.
- Protection injection/outillage encore perfectible.

## 9. Skills / mutation

Le système de skills est déjà une des grandes forces de NUMAX.

**Limites :**
- Les skills agissent encore sur un périmètre borné.
- Toutes les mutations possibles du runtime ne sont pas encore skillifiées.
- Les effets restent surtout config/policy/runtime, pas encore transformations profondes de modules.

## 10. Memory

La mémoire hiérarchique existe déjà et fonctionne.

**Limites :**
- Pas encore de scoring sémantique très avancé.
- Pas encore de mémoire vectorielle réellement centrale.
- Promotion / oubli encore perfectibles.
- Peu de benchmark mémoire cross-domaines.

## 11. Planner

Le planner existe.

**Limites :**
- Il reste encore relativement simple.
- Peu de stratégies multi-branches.
- Peu de recherche explicite profonde.

## 12. Benchmark

Le benchmark NUMAX est déjà une vraie force.

**Limites :**
- Baselines encore simples.
- Scénarios encore centrés principalement sur NUMAX lui-même.
- Pas encore de benchmark multi-domaines massif.
- Pas encore de benchmark distribué/long-running complet.

## 13. Artefacts

NUMAX produit et valide déjà des artefacts.

**Limites :**
- Scoring métier encore minimal.
- Peu de types métier fortement spécialisés.
- Peu d’évaluateurs experts par artefact.

## 14. Prod scale

NUMAX v1 est prêt pour :
- Local sérieux.
- Démonstration solide.
- Exploitation prudente.
- Benchmarking continu.

NUMAX v1 n’est pas encore prêt pour affirmer sans réserve :
- Scale massif distribué.
- Multi-tenant durci.
- Sécurité forte d’exploitation.
- Infra cloud complète et standardisée.

## 15. Ce que cela veut dire correctement

La bonne lecture de NUMAX v1 est :
**Un framework système très avancé et déjà démontrable, mais pas encore la forme finale industrialisée sur tous les axes.**

C’est une position très forte. Ce n’est pas une faiblesse.

## 16. Résumé final

**NUMAX v1 supporte réellement :**
- Flows gouvernés
- Critic
- Budget
- Artefacts
- Mémoire hiérarchique
- Benchmark système
- Skills réversibles
- Rollback
- Jobs locaux
- Observabilité locale structurée
- Auth/RBAC de base
- Sandbox bornée

**NUMAX v1 ne supporte pas encore pleinement :**
- Prod distribuée dure
- Auth forte multi-tenant
- Sandbox dure
- Queue réelle
- OTel réel
- Scoring artefact métier avancé
- Mémoire sémantique prod-grade large

C’est précisément ce qui définit la frontière entre **V1 démontrée** et **Phase Scale/Prod**.
