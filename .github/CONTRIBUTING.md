# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet !

## Auteur Principal

**Aurel IKAMA HONEY**  
Projet : Génération Automatique de Tests de Contrat à partir de Documentation API

## Règles de Contribution

### 📝 Documentation Obligatoire

**IMPORTANT** : Toute modification du code DOIT être accompagnée d'une mise à jour de la documentation.

#### Après chaque modification :

1. **Mettre à jour le README.md** si la fonctionnalité affecte l'utilisation
2. **Mettre à jour la documentation technique** dans `/docs/`
3. **Ajouter des commentaires** dans le code pour expliquer les changements complexes
4. **Mettre à jour les exemples** si les API changent
5. **Documenter les nouvelles variables d'environnement** dans `.env.example`

#### Fichiers de documentation à vérifier :

- `README.md` - Vue d'ensemble et guide d'utilisation
- `docs/ACTION_PLAN.md` - Plan d'action et progression
- `docs/PROJECT_STRUCTURE.md` - Structure du projet
- `docs/OLLAMA_SETUP.md` - Configuration Ollama
- `docs/COST_OPTIMIZATION.md` - Optimisation des coûts
- `scripts/README.md` - Documentation des scripts
- Docstrings Python dans chaque module

### 🔄 Workflow de Contribution

1. **Créer une branche**
   ```bash
   git checkout -b feature/nom-fonctionnalite
   ```

2. **Développer et tester**
   ```bash
   # Faire vos modifications
   python src/main.py  # Tester
   pytest tests/       # Exécuter les tests
   ```

3. **Mettre à jour la documentation**
   ```bash
   # OBLIGATOIRE : Mettre à jour la documentation
   # - README.md si nécessaire
   # - docs/ACTION_PLAN.md pour tracker la progression
   # - Docstrings dans le code
   # - Exemples d'utilisation
   ```

4. **Formatter le code**
   ```bash
   black src/ tests/
   isort src/ tests/
   pylint src/
   ```

5. **Committer avec message clair**
   ```bash
   git add .
   git commit -m "feat: Description de la fonctionnalité
   
   - Détail 1
   - Détail 2
   
   Documentation mise à jour:
   - README.md
   - docs/ACTION_PLAN.md
   "
   ```

6. **Push et Pull Request**
   ```bash
   git push origin feature/nom-fonctionnalite
   ```

### 📋 Checklist avant Pull Request

- [ ] Code fonctionne et a été testé
- [ ] Tests unitaires ajoutés/mis à jour
- [ ] **README.md mis à jour** (si applicable)
- [ ] **Documentation technique mise à jour** (docs/)
- [ ] **Docstrings ajoutées** dans le code
- [ ] **Exemples d'utilisation** mis à jour (si API change)
- [ ] **.env.example** mis à jour (si nouvelles variables)
- [ ] Code formaté avec Black et isort
- [ ] Pas d'erreurs Pylint critiques
- [ ] Commit message descriptif
- [ ] Auteur crédité : Aurel IKAMA HONEY

### 🎯 Types de Commits

Utiliser les préfixes suivants :

- `feat:` - Nouvelle fonctionnalité
- `fix:` - Correction de bug
- `docs:` - Mise à jour documentation uniquement
- `style:` - Formatage, pas de changement de code
- `refactor:` - Refactoring sans changement de fonctionnalité
- `test:` - Ajout ou modification de tests
- `chore:` - Tâches de maintenance

### 📚 Standards de Documentation

#### Pour le code Python :

```python
"""
Module description.

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

#### Pour les nouveaux modules :

Chaque nouveau module doit avoir :
1. Docstring de module avec description et auteur
2. Docstrings pour toutes les fonctions/classes
3. Exemples d'utilisation dans les docstrings
4. Mise à jour de `docs/PROJECT_STRUCTURE.md`

#### Pour les nouvelles fonctionnalités :

1. Section dans README.md si fonctionnalité utilisateur
2. Documentation technique dans docs/ si complexe
3. Script d'exemple dans scripts/ si applicable
4. Tests dans tests/ avec couverture >80%

### 🐛 Rapport de Bugs

Lors du rapport d'un bug, inclure :

1. **Description** : Comportement observé vs attendu
2. **Reproduction** : Étapes pour reproduire
3. **Environnement** : 
   - OS
   - Version Python
   - Variables d'environnement (ENABLE_CLOUD_MODELS, etc.)
   - Modèles LLM utilisés
4. **Logs** : Sortie de logs/app.log
5. **Screenshots** : Si applicable

### 💡 Suggestions de Fonctionnalités

Pour proposer une fonctionnalité :

1. **Contexte** : Pourquoi cette fonctionnalité ?
2. **Cas d'usage** : Comment sera-t-elle utilisée ?
3. **Proposition** : Description de l'implémentation
4. **Impact** : Sur les questions de recherche (RQ1-RQ5)
5. **Documentation** : Quels fichiers devront être mis à jour ?

### 🧪 Tests

- Tous les nouveaux modules doivent avoir des tests
- Couverture minimale : 80%
- Tests à exécuter avant PR :

```bash
# Tests unitaires
pytest tests/ -v

# Couverture
pytest tests/ --cov=src --cov-report=html

# Linting
pylint src/

# Formatage
black --check src/ tests/
isort --check-only src/ tests/
```

### 📊 Questions de Recherche

Ce projet vise à répondre à RQ1-RQ5. Toute contribution doit :

1. **Rester alignée** avec les objectifs de recherche
2. **Documenter l'impact** sur les métriques (oracle quality, test validity, etc.)
3. **Préserver la traçabilité** pour l'analyse scientifique

### 🔒 Licence et Crédits

- **Auteur** : Aurel IKAMA HONEY
- **Licence** : MIT (voir LICENSE)
- Toute contribution sera créditée dans CONTRIBUTORS.md

### 🤝 Code de Conduite

- Respecter les autres contributeurs
- Fournir des retours constructifs
- Maintenir un environnement accueillant
- Suivre les standards du projet

### 📞 Contact

Pour toute question :
- **Issues GitHub** : Créer une issue
- **Discussions** : Utiliser les discussions GitHub
- **Auteur** : Aurel IKAMA HONEY

---

**Rappel Important** : La documentation n'est pas optionnelle. Chaque changement de code DOIT être accompagné d'une mise à jour de la documentation appropriée.

Merci de contribuer à l'amélioration de ce projet ! 🚀
