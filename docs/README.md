# Documentation du Projet

**Auteur** : Aurel IKAMA HONEY

## Vue d'ensemble

Ce dossier contient toute la documentation technique du projet de génération automatique de tests de contrat.

## Documents Disponibles

### 📋 [ACTION_PLAN.md](ACTION_PLAN.md)
Plan d'action détaillé du projet organisé en phases de développement.

**Contenu:**
- Phase 1: Setup Initial (Infrastructure, Configuration, Tests de base)
- Phase 2: Parser Bruno (Analyse des formats, Modèles de données, Validation)
- Phase 3: Agent Inductor (Extraction du contexte, Analyse sémantique)
- Phase 4: Agent Oracle (Génération des oracles, Validation des règles)
- Phase 5: Agent Contractor (Génération de code Java/Rest-Assured)
- Phase 6: Agent Runner (Exécution, Feedback, Boucle adaptative)
- Phase 7: Métriques et Évaluation (Réponses aux questions RQ1-RQ5)
- Phase 8: Optimisation et Déploiement

### 🏗️ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
Structure complète du projet avec description de chaque dossier et fichier.

**Contenu:**
- Arborescence complète
- Description de chaque module
- Rôle des dossiers
- Organisation du code

### 🏠 [OLLAMA_SETUP.md](OLLAMA_SETUP.md)
Guide complet de configuration et d'utilisation d'Ollama pour l'exécution locale de modèles LLM.

**Contenu:**
- Installation d'Ollama (macOS, Linux)
- Configuration des modèles (Mistral, Llama)
- Vérification de l'installation
- Commandes utiles
- Performance et comparaisons
- Dépannage
- Migration depuis API cloud

### 💰 [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md)
Guide détaillé sur l'optimisation des coûts avec le mode développement économique.

**Contenu:**
- Mode développement vs production
- Configuration de ENABLE_CLOUD_MODELS
- Économies réalisables (0€ vs $80-350/mois)
- Cas d'usage recommandés
- Migration entre modes
- Dépannage
- Impact sur les questions de recherche

## Guide de Navigation

### Pour commencer
1. Lire [README.md](../README.md) à la racine du projet
2. Consulter [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) pour comprendre l'organisation
3. Suivre [OLLAMA_SETUP.md](OLLAMA_SETUP.md) pour installer les prérequis
4. Configurer le [mode développement économique](COST_OPTIMIZATION.md)

### Pour développer
1. Consulter [ACTION_PLAN.md](ACTION_PLAN.md) pour voir la roadmap
2. Lire [Guide de Contribution](../.github/CONTRIBUTING.md)
3. Suivre les standards de documentation du projet

### Pour déployer
1. Passer en mode production (voir [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md))
2. Configurer les clés API cloud
3. Ajuster la configuration selon les besoins

## Règles de Documentation

### 📝 Principe Fondamental

**Toute modification de code DOIT être accompagnée d'une mise à jour de la documentation.**

### Quand mettre à jour la documentation ?

- ✅ **Après chaque nouvelle fonctionnalité** → Mettre à jour README.md et docs/
- ✅ **Après modification de structure** → Mettre à jour PROJECT_STRUCTURE.md
- ✅ **Après changement de configuration** → Mettre à jour les guides concernés
- ✅ **Après ajout de script** → Mettre à jour scripts/README.md
- ✅ **Après nouvelle variable .env** → Mettre à jour .env.example et docs/
- ✅ **Dans le code** → Ajouter/mettre à jour les docstrings

### Checklist Documentation

Avant chaque commit :
- [ ] README.md à jour si nécessaire
- [ ] Documentation technique mise à jour (docs/)
- [ ] Docstrings ajoutées/mises à jour
- [ ] Exemples d'utilisation à jour
- [ ] .env.example mis à jour si nouvelles variables
- [ ] ACTION_PLAN.md mis à jour pour tracker la progression

## Format des Docstrings Python

```python
"""
Module description courte.

Description détaillée du module si nécessaire.

Author: Aurel IKAMA HONEY
Created: YYYY-MM-DD
"""

def fonction_exemple(param1: str, param2: int) -> dict:
    """
    Description courte de la fonction.
    
    Description détaillée si nécessaire.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description du retour
        
    Raises:
        ValueError: Description de l'erreur
        
    Example:
        >>> fonction_exemple("test", 42)
        {'result': 'success'}
    """
    pass
```

## Organisation des Documents

### Documents Techniques
Placer dans `docs/` :
- Guides de configuration
- Architecture technique
- Décisions de design
- Guides d'optimisation

### Documentation Utilisateur
Placer dans `README.md` :
- Vue d'ensemble du projet
- Installation rapide
- Guide d'utilisation de base
- Exemples simples

### Documentation Contributeur
Placer dans `.github/` :
- Guide de contribution (CONTRIBUTING.md)
- Templates (PR, issues)
- Workflows CI/CD

## Questions de Recherche

Ce projet vise à répondre à 5 questions de recherche (RQ1-RQ5). La documentation doit :

1. **Tracer l'impact** sur les métriques de recherche
2. **Documenter les décisions** qui affectent les RQ
3. **Maintenir la cohérence** avec les objectifs scientifiques
4. **Faciliter la reproductibilité** des expérimentations

Voir [ACTION_PLAN.md](ACTION_PLAN.md) Phase 7 pour les détails sur les métriques.

## Maintenance de la Documentation

### Révision Régulière
- Vérifier la documentation à chaque phase du projet
- Mettre à jour les captures d'écran si nécessaire
- Corriger les liens cassés
- Actualiser les versions et dépendances

### Qualité de la Documentation
- Utiliser un langage clair et concis
- Fournir des exemples concrets
- Inclure des diagrammes si pertinent
- Maintenir une structure cohérente

## Outils de Documentation

### Génération
- **Markdown** pour tous les documents
- **Docstrings Python** pour le code
- **Type hints** pour la clarté
- **Sphinx** (futur) pour générer la doc API

### Validation
- Vérifier les liens avec un linter Markdown
- Tester les exemples de code
- Valider la syntaxe des snippets

## Contact et Questions

Pour toute question sur la documentation :
- Ouvrir une issue avec le label `documentation`
- Utiliser le template [documentation.md](../.github/ISSUE_TEMPLATE/documentation.md)
- Consulter le [Guide de Contribution](../.github/CONTRIBUTING.md)

---

**Rappel** : La documentation n'est pas optionnelle. Elle est essentielle pour la maintenabilité, la reproductibilité de la recherche, et la collaboration.

**Auteur du Projet** : Aurel IKAMA HONEY  
**Licence** : MIT (voir [LICENSE](../LICENSE))
