[app]
# (str) Title of your application
title = Vortex Lotto

# (str) Package name (MUSS klein sein)
package.name = vortexlotto

# (str) Package domain (MUSS klein sein)
package.domain = org.senci33

source.dir = .
source.include_exts = py,kv,json,png,jpg,atlas
version = 1.0.0
version.code = 1

# WICHTIG: openssl für Internet-Sicherheit (HTTPS)
requirements = python3,kivy,requests,certifi,charset-normalizer,idna,urllib3,openssl

android.permissions = INTERNET
orientation = portrait
fullscreen = 0

# ==========================================================
# Android Einstellungen (Play Store Optimiert)
# ==========================================================

# API 33 ist aktuell die stabilste Wahl für Buildozer-Actions
android.api = 34
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True

# Hier wird das .aab Format für Google Play aktiviert
android.release_artifact = aab

# Google Play verlangt Support für 64-bit (arm64-v8a)
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
