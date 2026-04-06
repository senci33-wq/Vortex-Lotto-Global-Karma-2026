[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# --- VERSION FIX ---
version = 1.1.0

# --- REQUIREMENTS FIX (Für API & SSL) ---
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,idna,openssl

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# --- GITHUB BUILD FIX ---
android.accept_sdk_license = True
android.api = 34
android.minapi = 21
android.sdk = 34
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
