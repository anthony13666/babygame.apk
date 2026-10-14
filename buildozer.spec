[app]
title = BabyGame
package.name = babygame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav
version = 0.1
requirements = python3,kivy==2.3.0,sdl2_ttf==2.20.0,gstreamer
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api_min = 21
android.api_target = 33
android.architectures = arm64-v8a

[buildozer]
log_level = 2
color_log = yes
