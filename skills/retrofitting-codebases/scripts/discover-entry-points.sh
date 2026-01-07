#!/bin/bash
# Finds common entry point patterns across languages
# Usage: bash scripts/discover-entry-points.sh [src_dir]

SRC_DIR="${1:-src}"

echo "=== API Routes ==="
grep -rn "Route\|MapGet\|MapPost\|HttpPost\|HttpGet\|@app\.\|@router\.\|router\." \
    --include="*.cs" --include="*.py" --include="*.ts" --include="*.js" --include="*.java" \
    "$SRC_DIR" 2>/dev/null | head -50

echo ""
echo "=== CLI Commands ==="
grep -rn "Command\|ArgParser\|ArgumentParser\|@click\|yargs\|commander" \
    --include="*.cs" --include="*.py" --include="*.ts" --include="*.js" --include="*.java" \
    "$SRC_DIR" 2>/dev/null | head -20

echo ""
echo "=== Background Jobs ==="
grep -rn "Cron\|Schedule\|BackgroundService\|@scheduled\|setInterval\|celery" \
    --include="*.cs" --include="*.py" --include="*.ts" --include="*.js" --include="*.java" \
    "$SRC_DIR" 2>/dev/null | head -20

echo ""
echo "=== Event Handlers ==="
grep -rn "Subscribe\|Handler\|Consumer\|@EventListener\|\.on\(.\|addEventListener" \
    --include="*.cs" --include="*.py" --include="*.ts" --include="*.js" --include="*.java" \
    "$SRC_DIR" 2>/dev/null | head -20

echo ""
echo "=== Controllers/Handlers ==="
grep -rn "Controller\|Handler\|Resolver\|Service" \
    --include="*.cs" --include="*.py" --include="*.ts" --include="*.js" --include="*.java" \
    "$SRC_DIR" 2>/dev/null | grep -i "class\|export\|public" | head -30

echo ""
echo "Done. Review above for entry points to investigate."
