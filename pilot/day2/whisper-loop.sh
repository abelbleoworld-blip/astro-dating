#!/bin/bash
# whisper-loop.sh — пишет 5-мин аудио чанки и транскрибирует в mesh-memory/voice/
set -u

MODEL="$HOME/.whisper-models/ggml-base.bin"
VOICE_DIR="$HOME/Documents/Projects/mesh-memory/voice"
TMP_DIR="/tmp/whisper-capture"
CHUNK_SEC=300  # 5 минут

mkdir -p "$TMP_DIR" "$VOICE_DIR"

while true; do
  TS=$(date +%Y-%m-%d_%H-%M-%S)
  TODAY=$(date +%Y-%m-%d)
  WAV="$TMP_DIR/chunk_$TS.wav"
  OUT="$VOICE_DIR/$TODAY.txt"

  # Запись 5 минут моно 16kHz (Whisper native)
  sox -d -r 16000 -c 1 -b 16 "$WAV" trim 0 $CHUNK_SEC 2>/dev/null || {
    echo "$(date) sox FAIL — устройство микрофона занято?" >&2
    sleep 30
    continue
  }

  # Если файл слишком короткий или тишина — скип
  SIZE=$(stat -f%z "$WAV" 2>/dev/null || echo 0)
  if [ "$SIZE" -lt 100000 ]; then
    rm -f "$WAV"
    sleep 5
    continue
  fi

  # Транскрипт
  TEXT=$(whisper-cli -m "$MODEL" -f "$WAV" -l auto -nt --no-prints 2>/dev/null | tr -d '\r')

  if [ -n "$TEXT" ]; then
    echo "[$TS] $TEXT" >> "$OUT"
  fi

  rm -f "$WAV"
done
