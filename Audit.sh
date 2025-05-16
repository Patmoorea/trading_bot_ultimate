#!/bin/bash
# --------------------------------------------------
# Audit.sh - Vérification approfondie des modules
# Usage : ./Audit.sh [--fix] [--backup]
# --------------------------------------------------

# Configuration
BACKUP_DIR="./audit_backup_$(date +%Y%m%d)"
LOG_FILE="./audit_report_$(date +%Y%m%d).txt"

# Fonctions principales
check_structure() {
    echo "=== STRUCTURE DES MODULES ===" > $LOG_FILE
    find src -type d | grep -v "__pycache__" | tee -a $LOG_FILE
    
    echo "" >> $LOG_FILE
    echo "=== FICHIERS CRITIQUES ===" >> $LOG_FILE
    find src \( -name "*.py" -o -name "*.yaml" \) -exec ls -la {} \; | tee -a $LOG_FILE
}

verify_imports() {
    echo "" >> $LOG_FILE
    echo "=== IMPORTS PYTHON ===" >> $LOG_FILE
    grep -r "^import\|^from" src/ | awk -F':' '{print $1}' | sort | uniq | tee -a $LOG_FILE
}

run_tests() {
    echo "" >> $LOG_FILE
    echo "=== TESTS UNITAIRES ===" >> $LOG_FILE
    pytest --cov=src --cov-report=term-missing | tee -a $LOG_FILE
}

reorganize_project() {
    mkdir -p $BACKUP_DIR
    echo "Reorganisation sécurisée :"
    
    # Exemple : Standardisation des noms
    for dir in src/*arbitration*; do
        if [ -d "$dir" ]; then
            mv "$dir" "${dir/arbitration/arbitrage}" 
            echo "Renommé : $dir -> ${dir/arbitration/arbitrage}"
        fi
    done
    
    cp -r src/ $BACKUP_DIR/
    echo "Backup créé dans $BACKUP_DIR"
}

# Exécution
case $1 in
    --fix)
        reorganize_project
        ;;
    --backup)
        mkdir -p $BACKUP_DIR
        cp -r src/ tests/ $BACKUP_DIR/
        ;;
    *)
        check_structure
        verify_imports
        run_tests
        ;;
esac

echo "Rapport complet : $LOG_FILE"