#!/bin/bash
# setup-beelink.sh — запустить НА Beelink (после ssh azw-ser9)
set -e

ABEL_DIR="$HOME/abel"
REPO_URL="https://github.com/abelbleoworld-blip/astro-dating.git"

echo "=== PILOT++ Day 2: Beelink setup ==="

# 1. Базовые зависимости
echo "[1/4] Базовые пакеты..."
which git >/dev/null 2>&1 || sudo apt-get install -y git
which python3 >/dev/null 2>&1 || sudo apt-get install -y python3 python3-pip

# 2. Структура
echo "[2/4] ~/abel/..."
mkdir -p "$ABEL_DIR"
cd "$ABEL_DIR"

# 3. Clone astro-dating
echo "[3/4] Clone astro-dating..."
if [ ! -d astro-dating ]; then
  git clone "$REPO_URL"
else
  cd astro-dating && git pull && cd ..
fi

# 4. Smoke test
echo "[4/4] Smoke test..."
cd astro-dating
echo "Git status:"
git log --oneline -3
echo ""
echo "Python:"
python3 --version
echo ""
echo "Файлы PILOT++:"
ls -la docs/ARCHITECTURE-2N.md docs/MESH-DISTRIBUTION.md docs/PREDICTIVE-CONTEXT.md 2>/dev/null
echo ""

# 5. Mark Beelink alive
HOSTNAME=$(hostname)
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"node\": \"$HOSTNAME\", \"role\": \"executor\", \"alive_since\": \"$DATE\", \"pilot_day\": 2}" \
  > ~/abel/beelink-alive.json
cat ~/abel/beelink-alive.json
echo ""
echo "✅ Beelink готов как mesh executor."
echo "📂 ~/abel/astro-dating/ — рабочая копия"
echo "🔗 Для mesh-memory queue — см. README.md в pilot/day2/"
