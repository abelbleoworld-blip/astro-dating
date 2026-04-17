#!/bin/bash
# OCR Альмагеста Веселовского (1998) — 672 страницы DjVu → текст
set -euo pipefail

DJVU="/Users/macbookpro14/Downloads/Ptolemey_Almagest-ili-matematicheskoe-sochinenie-v-trinadcati-knigah.129855.djvu"
OUT_DIR="/Users/macbookpro14/Documents/Projects/astro-dating/data/almagest-ocr"
FULL_TEXT="/Users/macbookpro14/Documents/Projects/astro-dating/data/almagest-veselovsky-1998.txt"

mkdir -p "$OUT_DIR"
TOTAL=$(djvused "$DJVU" -e 'n')
echo "[OCR] Альмагест: $TOTAL страниц → $OUT_DIR"

> "$FULL_TEXT"

for p in $(seq 1 $TOTAL); do
  OUTFILE="$OUT_DIR/page_$(printf '%03d' $p).txt"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    cat "$OUTFILE" >> "$FULL_TEXT"
    printf "\n--- page $p ---\n" >> "$FULL_TEXT"
    continue
  fi

  TMPBASE="/tmp/almagest-ocr-p${p}"
  ddjvu -format=tiff -page=$p -size=2400x3200 "$DJVU" "${TMPBASE}.tiff" 2>/dev/null
  sips -s format png "${TMPBASE}.tiff" --out "${TMPBASE}.png" >/dev/null 2>&1
  tesseract "/private${TMPBASE}.png" stdout -l rus --psm 6 2>/dev/null > "$OUTFILE" || true
  rm -f "${TMPBASE}.tiff" "${TMPBASE}.png"

  cat "$OUTFILE" >> "$FULL_TEXT"
  printf "\n--- page $p ---\n" >> "$FULL_TEXT"

  if [ $((p % 50)) -eq 0 ]; then
    echo "[OCR] $p / $TOTAL"
  fi
done

echo "[OCR] Готово: $(wc -l < "$FULL_TEXT") строк"
