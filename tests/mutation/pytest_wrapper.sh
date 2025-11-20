#!/bin/bash
# Wrapper pour pytest qui configure correctement PYTHONPATH pour mutmut

# Le chemin absolu du projet
PROJECT_DIR="/Users/aurelikama/Documents/Projet/contract-test-generation-from-api-documentation"

# Configurer PYTHONPATH pour inclure src original (pas la copie mutmut)
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

# Retourner au répertoire du projet et exécuter les tests depuis là
# en utilisant les tests originaux (pas ceux dans mutants/)
cd "$PROJECT_DIR" && python -m pytest tests/ -x --tb=short --ignore=scripts/
