#!/bin/bash
# setup-whisper-mac.sh — Whisper.cpp 24/7 capture для PILOT++ Day 2
set -e

VOICE_DIR="$HOME/Documents/Projects/mesh-memory/voice"
MODEL_DIR="$HOME/.whisper-models"
MODEL="ggml-base.bin"
PLIST_NAME="com.user.whisper-capture"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== PILOT++ Day 2: Whisper 24/7 setup ==="

# 1. Зависимости
echo "[1/5] brew install whisper-cpp sox..."
which whisper-cli >/dev/null 2>&1 || brew install whisper-cpp
which sox >/dev/null 2>&1 || brew install sox
which ffmpeg >/dev/null 2>&1 || brew install ffmpeg

# 2. Модель
echo "[2/5] Whisper model..."
mkdir -p "$MODEL_DIR"
if [ ! -f "$MODEL_DIR/$MODEL" ]; then
  curl -L -o "$MODEL_DIR/$MODEL" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
fi

# 3. Voice dir
echo "[3/5] Voice dir..."
mkdir -p "$VOICE_DIR"

# 4. Loop script
echo "[4/5] Loop script..."
cp "$SCRIPT_DIR/whisper-loop.sh" "$HOME/bin/whisper-loop.sh" 2>/dev/null || \
  { mkdir -p "$HOME/bin"; cp "$SCRIPT_DIR/whisper-loop.sh" "$HOME/bin/"; }
chmod +x "$HOME/bin/whisper-loop.sh"

# 5. launchd
echo "[5/5] launchd..."
mkdir -p "$LAUNCH_AGENTS"
sed "s|__HOME__|$HOME|g" "$SCRIPT_DIR/$PLIST_NAME.plist" > "$LAUNCH_AGENTS/$PLIST_NAME.plist"
launchctl unload "$LAUNCH_AGENTS/$PLIST_NAME.plist" 2>/dev/null || true
launchctl load "$LAUNCH_AGENTS/$PLIST_NAME.plist"

echo ""
echo "✅ Whisper 24/7 запущен."
echo "📂 Транскрипт: $VOICE_DIR/$(date +%Y-%m-%d).txt"
echo "📋 Лог: /tmp/whisper-capture.log"
echo "🛑 Откат: launchctl unload $LAUNCH_AGENTS/$PLIST_NAME.plist"
echo ""
echo "Через 5 минут проверь: ls -la $VOICE_DIR/"
