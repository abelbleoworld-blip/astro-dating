#!/bin/bash
# predictor.sh — PC layer 4: вызов Claude с calibrated prompt + текущим контекстом
# Cron: 0 */2 * * * /path/to/predictor.sh
# Manual: bash predictor.sh

set -u
PROJECT="$HOME/Documents/Projects/astro-dating"
MESH="$HOME/Documents/Projects/mesh-memory"
PROMPT_FILE="$PROJECT/predictor/PROMPT.md"
OUT_DIR="$MESH/predictions"
GAME_STATE="$HOME/Documents/Projects/.game/state.json"
mkdir -p "$OUT_DIR"

TS=$(date +%Y-%m-%d_%H-%M)
OUT="$OUT_DIR/$TS.md"

# === GATHER CONTEXT ===
CONTEXT_FILE="/tmp/predictor_context_$$.txt"
{
  echo "## Current time"
  date -Iseconds
  echo ""
  echo "## Last 7 git commits in astro-dating"
  cd "$PROJECT" && git log --oneline -7
  echo ""
  echo "## Active quests + templates"
  if [ -f "$GAME_STATE" ]; then
    python3 -c "
import json
d = json.load(open('$GAME_STATE'))
print(f'Active: {len(d[\"active_quests\"])} quests')
for q in d['active_quests'][:5]:
    print(f'  - {q.get(\"id\", \"?\")}: {q.get(\"name\", \"?\")}')
print(f'Templates available: {len(d[\"quest_templates\"])}')
print(f'Pilot XP: {d[\"pilot\"][\"xp\"]} / next {d[\"pilot\"][\"xp_next\"]}')
"
  else
    echo "(no game state)"
  fi
  echo ""
  echo "## Voice transcript last 20 lines today"
  tail -20 "$MESH/voice/$(date +%Y-%m-%d).txt" 2>/dev/null || echo "(нет записей сегодня)"
  echo ""
  echo "## FOCUS-25 paths"
  awk '/## 4 экспоненциальных пути/,/## 25%/' "$PROJECT/FOCUS-25.md" | head -20
  echo ""
  echo "## Open issues from FOCUS-25"
  awk '/## Open issues/,/## /' "$PROJECT/FOCUS-25.md" | head -10
} > "$CONTEXT_FILE"

# === CALL CLAUDE API ===
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "❌ ANTHROPIC_API_KEY не установлен."
  echo "   export ANTHROPIC_API_KEY=sk-ant-..."
  echo ""
  echo "Пока сохраню только контекст для ручного теста:"
  cp "$CONTEXT_FILE" "$OUT.context"
  echo "📂 Контекст: $OUT.context"
  exit 1
fi

if ! which jq > /dev/null; then
  echo "❌ jq не установлен. brew install jq"
  exit 1
fi

PROMPT=$(cat "$PROMPT_FILE")
CONTEXT=$(cat "$CONTEXT_FILE")

RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n --arg p "$PROMPT" --arg c "$CONTEXT" '{
    model: "claude-sonnet-4-6",
    max_tokens: 2000,
    system: $p,
    messages: [{role: "user", content: $c}]
  }')")

# Extract text and check for errors
TEXT=$(echo "$RESPONSE" | jq -r '.content[0].text // empty')
ERROR=$(echo "$RESPONSE" | jq -r '.error.message // empty')

if [ -n "$ERROR" ]; then
  echo "❌ API error: $ERROR"
  rm -f "$CONTEXT_FILE"
  exit 1
fi

if [ -z "$TEXT" ]; then
  echo "❌ Empty response"
  echo "$RESPONSE" | head -20
  rm -f "$CONTEXT_FILE"
  exit 1
fi

echo "$TEXT" > "$OUT"
rm -f "$CONTEXT_FILE"

echo "✅ Predictor вывел: $OUT"
echo ""
echo "─────────────────────────────────────"
cat "$OUT"
echo "─────────────────────────────────────"

# Send Telegram notification (optional, if BOT_TOKEN set)
if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
  PREVIEW=$(echo "$TEXT" | head -10)
  curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d "chat_id=$TELEGRAM_CHAT_ID" \
    -d "text=🔮 PC Predictor $TS\n\n$PREVIEW\n\n[full: ~/Documents/Projects/mesh-memory/predictions/$TS.md]" > /dev/null
fi
