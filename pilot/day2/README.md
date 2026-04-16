# PILOT++ Day 2 — Beelink + Whisper 24/7
**Дедлайн:** 11:00 МСК (будильник `com.user.pilot-day2-deadline.plist`).
**Цель дня:** Beelink онлайн в mesh + Whisper 24/7 capture на Mac → mesh-memory/voice/.
## Что запустить утром (3 команды)
### 1. На Mac — Whisper 24/7
```bash
cd ~/Documents/Projects/astro-dating/pilot/day2
bash setup-whisper-mac.sh
```
Скрипт: `brew install whisper-cpp sox`, скачает модель `ggml-base.bin` (~150MB),
скопирует launchd plist, загрузит демон. Через 5 минут первый транскрипт
появится в `~/Documents/Projects/mesh-memory/voice/2026-04-17.txt`.
### 2. На Beelink — клон + тест
```bash
ssh azw-ser9
# на Beelink:
curl -sL https://raw.githubusercontent.com/abelbleoworld-blip/astro-dating/master/pilot/day2/setup-beelink.sh | bash
```
Скрипт: создаст `~/abel/`, склонирует astro-dating, запустит smoke-test
(Python + git + версия). Если всё ОК — Beelink готов как mesh-нода.
### 3. Тест mesh-memory queue (день 2 минимум)
```bash
# На Mac создать pending-задачу:
echo "echo 'beelink alive' > ~/abel/test-result.txt" > \
  ~/Documents/Projects/mesh-memory/tasks/pending/test-001.sh
# Beelink через minute получит и выполнит (cron позже, пока вручную):
ssh azw-ser9 'mv ~/abel/mesh-memory/tasks/pending/test-001.sh \
  ~/abel/mesh-memory/tasks/in-progress/ && bash ~/abel/mesh-memory/tasks/in-progress/test-001.sh \
  && mv ~/abel/mesh-memory/tasks/in-progress/test-001.sh \
     ~/abel/mesh-memory/tasks/done/test-001.sh.done'
cat ~/abel/test-result.txt  # должно быть "beelink alive"
```
## Как проверить что Whisper работает
```bash
ls -la ~/Documents/Projects/mesh-memory/voice/  # файлы за сегодня
tail -20 ~/Documents/Projects/mesh-memory/voice/2026-04-17.txt
launchctl list | grep whisper-capture  # должен быть запущен
```
Если файлы не появляются — `cat /tmp/whisper-capture.log` для диагностики.
## Метрики дня 2 (что замерить вечером)
- ◻ Whisper записал ≥ 1 час и распознал
- ◻ Beelink ответил на mesh-memory задачу
- ◻ Voice-файл в mesh-memory ≥ 200 строк
- ◻ Subjective: «не мешает работать?» 7+/10
## Если что-то сломалось
Откат Whisper: `launchctl unload ~/Library/LaunchAgents/com.user.whisper-capture.plist`
Откат будильника: `launchctl unload ~/Library/LaunchAgents/com.user.pilot-day2-deadline.plist`
Beelink не отвечает: проверить `ssh azw-ser9 echo ok`, если нет — Wi-Fi/mesh.
## День 2 завершён, когда
3 ◼ из 4 метрик. Тогда вечером можно `quest complete pilot_d2` (если бы pilot_d2 был
в колоде — мы сделали 64 anchor-квеста, не pilot day квесты, но прогресс отмечается
коммитами в repo).
