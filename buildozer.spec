[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,kv,json,png,jpg,atlas
version = 1.2

# WICHTIG: openssl für Google Play / HTTPS
requirements = python3,kivy,requests,certifi,charset-normalizer,idna,urllib3,openssl

android.permissions = INTERNET
orientation = portrait
fullscreen = 0

# ==========================================================
# Android Einstellungen für Play Store
# ==========================================================

# API 33 ist für den Build am stabilsten
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True

# Hier wird die .aab Datei aktiviert
android.release_artifact = aab

# Google Play verlangt beide Architekturen (insb. arm64-v8a)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
