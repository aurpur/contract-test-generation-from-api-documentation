#!/bin/bash
# Script pour lancer les tests de mutation avec mutmut

# Ajouter src au PYTHONPATH
export PYTHONPATH="/Users/aurelikama/Documents/Projet/contract-test-generation-from-api-documentation/src:$PYTHONPATH"

# Nettoyer le cache mutmut
rm -rf .mutmut-cache

# Lancer mutmut
echo "========================================="
echo "Lancement des tests de mutation avec mutmut"
echo "========================================="
echo ""

mutmut run --paths-to-mutate=src/ --runner="pytest tests/ -x --tb=line --ignore=scripts/"
