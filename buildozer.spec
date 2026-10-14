[app]

# Название приложения на экране телефона
title = Веселая Обучалка

# Имя пакета (латиница, без пробелов)
package.name = babygame

# Домен (можно любой)
package.domain = org.babygame

# Где искать исходники (точка означает текущую папку)
source.dir = .

# Какие расширения файлов включать в APK
source.include_exts = py,png,jpg,kv,atlas,mp3,wav

# Исключить ненужные папки (чтобы не тащить мусор)
source.exclude_dirs = __pycache__, .git, venv, web_game

# Зависимости Python
requirements = python3,kivy,sdl2_ttf,gstreamer

# Ориентация экрана (portrait - вертикально)
orientation = portrait

# Полный экран? (1 - да, 0 - нет)
fullscreen = 0

# Версия Android API (21 = Android 5.0+, подходит для старых и новых телефонов)
android.api_min = 21
android.api_target = 33

# Архитектура процессора (arm64-v8a для современных смартфонов)
android.architectures = arm64-v8a

# Права доступа (если нужен интернет для рекламы/обновлений, оставь INTERNET. Для оффлайн игры можно убрать)
android.permissions = INTERNET

[buildozer]
log_level = 2
color_log = yes