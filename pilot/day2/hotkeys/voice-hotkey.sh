#!/bin/bash
# voice-hotkey — версия voice для запуска по hotkey (без stdin, с notifications)
# Usage: voice-hotkey [seconds] [tag]

DURATION="${1:-30}"
TAG="${2:-HOTKEY}"
MODEL="$HOME/.whisper-models/ggml-base.bin"
VOICE_DIR="$HOME/Documents/Projects/mesh-memory/voice"
TMP="/tmp/voice_hotkey_$(date +%s).wav"
TODAY=$(date +%Y-%m-%d)
TS=$(date +%Y-%m-%d_%H-%M-%S)
OUT="$VOICE_DIR/$TODAY.txt"

mkdir -p "$VOICE_DIR"

# Запись с уведомлением
osascript -e "display notification \"🎙 Запись ${DURATION} сек...\" with title \"Voice\" sound name \"Pop\"" &
sox -d -r 16000 -c 1 -b 16 "$TMP" trim 0 "$DURATION" 2>/dev/null

SIZE=$(stat -f%z "$TMP" 2>/dev/null || echo 0)
if [ "$SIZE" -lt 50000 ]; then
  osascript -e 'display notification "⚠️ Запись пустая или микрофон не отвечает" with title "Voice" sound name "Basso"'
  rm -f "$TMP"
  exit 1
fi

# Транскрипт
TEXT=$(/opt/homebrew/bin/whisper-cli -m "$MODEL" -f "$TMP" -l auto -nt --no-prints 2>/dev/null | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

if [ -z "$TEXT" ]; then
  osascript -e 'display notification "⚠️ Whisper ничего не распознал" with title "Voice" sound name "Basso"'
  rm -f "$TMP"
  exit 1
fi

# Сохранить
echo "[$TS] ($TAG) $TEXT" >> "$OUT"

# Уведомление с превью (первые 100 символов)
PREVIEW=$(echo "$TEXT" | cut -c1-100)
osascript -e "display notification \"$PREVIEW\" with title \"✅ Voice сохранено\" sound name \"Glass\""

rm -f "$TMP"
