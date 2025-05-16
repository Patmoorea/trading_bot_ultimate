#!/bin/bash
echo "=== ARCHITECTURE VERIFICATION ==="

# Check directories
declare -a required_dirs=(
    "src/data/realtime/websocket"
    "src/analysis/technical/advanced"
    "src/analysis/technical/core"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir exists"
    else
        echo "✗ $dir missing - creating..."
        mkdir -p "$dir"
    fi
done

# Check essential files
declare -A essential_files=(
    ["WebSocket Client"]="src/data/realtime/websocket/client.py"
    ["Liquidity Indicators"]="src/analysis/technical/advanced/liquidity.py"
)

for desc in "${!essential_files[@]}"; do
    file="${essential_files[$desc]}"
    if [ -f "$file" ]; then
        echo "✓ $desc: $file"
    else
        echo "✗ $desc missing: $file"
    fi
done

echo "=== VERIFICATION COMPLETE ==="
