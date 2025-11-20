#!/bin/bash
# Script de nettoyage automatique du dossier output/
# Nettoie les fichiers de plus de 7 jours et garde seulement les 10 derniers de chaque type

set -e

echo "🧹 Nettoyage du dossier output/"
echo "================================"

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour compter les fichiers
count_files() {
    local dir=$1
    local pattern=$2
    find "$dir" -name "$pattern" -type f 2>/dev/null | wc -l | tr -d ' '
}

# Compter les fichiers avant
echo -e "\n${BLUE}📊 État initial:${NC}"
echo "  Tests Java: $(count_files output/tests/java '*.java')"
echo "  Tests Gherkin: $(count_files output/tests/gherkin '*.feature')"
echo "  Rapports HTML: $(count_files output/reports/html '*.html')"
echo "  Graphiques: $(count_files output/reports/graphs '*.png')"
echo "  Logs: $(count_files output/reports/logs '*.log')"
echo "  Traces: $(count_files output/reports/traces '*.json')"
echo "  Oracles: $(count_files output/oracles '*.txt')"

# Supprimer les fichiers de plus de 7 jours
echo -e "\n${BLUE}🗑️  Suppression des fichiers de plus de 7 jours...${NC}"
deleted_count=$(find output -type f ! -name '.gitkeep' ! -name 'README.md' -mtime +7 -print -delete 2>/dev/null | wc -l | tr -d ' ')
echo -e "${GREEN}✓ $deleted_count fichiers supprimés${NC}"

# Fonction pour garder seulement les N derniers fichiers
keep_latest() {
    local dir=$1
    local pattern=$2
    local keep=$3
    
    if [ -d "$dir" ]; then
        cd "$dir"
        local files=$(ls -t $pattern 2>/dev/null | tail -n +$((keep + 1)))
        if [ ! -z "$files" ]; then
            echo "$files" | xargs rm -f 2>/dev/null
            local removed=$(echo "$files" | wc -l | tr -d ' ')
            echo "  ✓ $dir: $removed ancien(s) fichier(s) supprimé(s)"
        fi
        cd - > /dev/null
    fi
}

# Garder seulement les 10 derniers fichiers de chaque type
echo -e "\n${BLUE}📦 Conservation des 10 derniers fichiers par catégorie...${NC}"
keep_latest "output/reports/html" "*.html" 10
keep_latest "output/reports/graphs" "*.png" 10
keep_latest "output/reports/logs" "*.log" 10
keep_latest "output/reports/traces" "*.json" 10
keep_latest "output/oracles" "*.txt" 10
keep_latest "output/tests/java" "*.java" 20
keep_latest "output/tests/gherkin" "*.feature" 20

# Compter les fichiers après
echo -e "\n${BLUE}📊 État final:${NC}"
echo "  Tests Java: $(count_files output/tests/java '*.java')"
echo "  Tests Gherkin: $(count_files output/tests/gherkin '*.feature')"
echo "  Rapports HTML: $(count_files output/reports/html '*.html')"
echo "  Graphiques: $(count_files output/reports/graphs '*.png')"
echo "  Logs: $(count_files output/reports/logs '*.log')"
echo "  Traces: $(count_files output/reports/traces '*.json')"
echo "  Oracles: $(count_files output/oracles '*.txt')"

# Afficher l'espace disque libéré
echo -e "\n${BLUE}💾 Espace disque:${NC}"
du -sh output/ 2>/dev/null

echo -e "\n${GREEN}✅ Nettoyage terminé!${NC}"
