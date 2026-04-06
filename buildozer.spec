[app]
# (1) Basis-Informationen
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# --- VERSION FIX ---
version = 1.1.0

# --- REQUIREMENTS (Wichtig für Quanten-API & SSL) ---
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,idna,openssl

# (2) Android Spezifikationen
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# --- ANDROID SDK/API FIX ---
android.api = 34
android.minapi = 21
android.sdk = 34
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET

# (3) Build-Einstellungen
[buildozer]
log_level = 2
warn_on_root = 1
