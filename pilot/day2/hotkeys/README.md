# Global hotkeys для voice-записи (skhd)
**Установлено:** 2026-04-17 03:51 МСК.
**Демон:** skhd (PID via `launchctl list | grep skhd`).
## 🔥 3 hotkey

| Hotkey | Длина | Тег | Назначение |
|---|---|---|---|
| **⌘⌥B** | 10 сек | IDEA | Быстрая идея, мысль на ходу |
| **⌘⌥V** | 30 сек | HOTKEY | Стандартная заметка |
| **⌘⌥⇧V** | 60 сек | HOTKEY-LONG | Долгая мысль / monolog |

## Как пользоваться

1. Нажать hotkey **в любом приложении** (Safari, Telegram, Xcode — где угодно)
2. Появится notification «🎙 Запись N сек...»
3. Говорить
4. Через N сек — notification «✅ Voice сохранено» с превью первых 100 символов
5. Полный текст в `~/Documents/Projects/mesh-memory/voice/yyyy-mm-dd.txt`

## ⚠️ Первое нажатие — нужно дать permission

При первом нажатии hotkey macOS попросит:

### 1. Accessibility для skhd
**System Settings → Privacy & Security → Accessibility → переключить ON для `skhd`**

(если skhd там нет — нажать `+` и добавить вручную: `/opt/homebrew/bin/skhd`)

### 2. Микрофон для skhd / sox
**System Settings → Privacy & Security → Microphone → переключить ON для `skhd`**

После обоих permissions — перезапустить skhd:
```bash
skhd --stop-service && skhd --start-service
```

## Управление демоном

```bash
skhd --start-service       # запустить
skhd --stop-service        # остановить
skhd --restart-service     # перезапустить (после правки config)

launchctl list | grep skhd # проверить что жив
```

## Конфиг

`~/.config/skhd/skhdrc` (копия здесь как `skhdrc.example`)

Изменить hotkeys → `skhd --restart-service` → новые работают.

## Откат полностью

```bash
skhd --stop-service
brew uninstall skhd
rm -rf ~/.config/skhd
rm ~/bin/voice-hotkey
```

## Альтернативы (если skhd не понравится)

| Инструмент | Преимущество | Минус |
|---|---|---|
| **Apple Shortcuts.app** | Нативное, через GUI | Нужно создавать вручную через GUI |
| **Hammerspoon** | Lua-скриптинг, очень мощный | Сложнее |
| **Karabiner-Elements** | Полная переназначка клавиатуры | Перебор для одной задачи |
| **Raycast** | Командная палитра + hotkeys | Платное pro для hotkeys |
| **BetterTouchTool** | Жесты + hotkeys | $10 |

skhd выбран как **минимальный** — одна задача, текстовый конфиг, не требует GUI.
