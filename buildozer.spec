[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,kv,json,png,jpg,atlas
version = 1.2

# WICHTIG für SSL und Google Play Anforderungen
requirements = python3,kivy,requests,certifi,charset-normalizer,idna,urllib3,openssl

android.permissions = INTERNET
orientation = portrait
fullscreen = 0

# ==========================================================
# Android Play Store Optimierung
# ==========================================================

# API 33 ist stabil für den GitHub Build
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True

# Dies erzeugt die .aab Datei
android.release_artifact = aab

# Google Play verlangt zwingend arm64-v8a
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
