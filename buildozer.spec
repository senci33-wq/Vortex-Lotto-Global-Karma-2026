[app]

title = Vortex Karma
package.name = vortexkarma
package.domain = org.karma
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,txt,md
version = 1.0.0
requirements = python3,kivy,kivymd
orientation = portrait
fullscreen = 1

# Android API + NDK (stabil für 2026)
android.api = 34
android.minapi = 23
android.ndk = 25b
android.ndk_api = 23

# Multi-Architektur (Pflicht für Google Play)
android.archs = arm64-v8a,armeabi-v7a

# AAB statt APK
android.release_artifact = aab

# Berechtigungen
android.permissions = INTERNET

# AndroidX + Multidex
android.enable_androidx = True
android.multidex = True
android.gradle_dependencies = com.android.support:multidex:1.0.3

# Signierung (GitHub Actions übernimmt die Secrets)
android.sign = True
android.keystore = my-release-key.keystore
android.keyalias = myappkey

# Optional: Icons & Presplash
# icon.filename = assets/icon.png
# presplash.filename = assets/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# Falls du zusätzliche libs brauchst:
# requirements = python3,kivy,kivymd,requests

[android]
android.extra_args = --enable-optimizations

[spelling]
ignore_words = kivy,kivymd 
