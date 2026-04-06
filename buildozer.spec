[app]
title = Vortex Karma
package.name = vortexkarma
package.domain = org.karma
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,txt,md
version = 1.0.0

# Optimierte Requirements für Stabilität
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,chardet,certifi

orientation = portrait
fullscreen = 1

# Android Konfiguration für API 34
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Wichtig für KivyMD & Google Play Standards
android.enable_androidx = True
android.multidex = True

# Erstmal APK für Tests (AAB nur für Play Store Release)
android.release_artifact = apk
android.permissions = INTERNET

# Deaktiviere Signierung für CI-Builds (verhindert File-not-found Fehler)
android.skip_update_check = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

[android]
# Speicheroptimierung beim Kompilieren
android.extra_args = --enable-optimizations
