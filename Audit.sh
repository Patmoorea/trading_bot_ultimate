#!/usr/bin/env bash

# Vérification portable des modules
missing_modules() {
  jq -e '
    .critical_modules |
    map_values(. > 0) |
    to_entries |
    .[] |
    select(.value == false) |
    .key
  ' .bot_manifest.json
}

if [[ $(missing_modules | wc -l) -gt 0 ]]; then
  echo "❌ Modules manquants :"
  missing_modules
  exit 1
else
  echo "✅ Tous les modules critiques sont présents"
  exit 0
fi
