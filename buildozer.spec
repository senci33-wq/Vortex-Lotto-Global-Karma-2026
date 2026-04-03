[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,kv,json,png,jpg,atlas
version = 1.3

# WICHTIG: openssl für Google Play / Internet-Sicherheit
requirements = python3,kivy,requests,certifi,charset-normalizer,idna,urllib3,openssl

android.permissions = INTERNET
orientation = portrait
fullscreen = 0

# ==========================================================
# Android Play Store Einstellungen
# ==========================================================

# Google verlangt aktuell API 34 für neue Apps, aber 33 wird oft noch akzeptiert.
# Wir bleiben bei 33 für die Stabilität im Build, da 34 oft Java-Fehler wirft.
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.0
android.accept_sdk_license = True

# WICHTIG: Hier wird festgelegt, dass eine .aab statt einer .apk erzeugt wird
android.release_artifact = aab
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
