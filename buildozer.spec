[app]
title = Vortex Ultra Safe
package.name = vortexultrasafe
package.domain = org.senci33

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 8.8.1

# WICHTIG: numpy und openssl für deinen Daten-Sync
requirements = python3,kivy==2.3.0,numpy,requests,urllib3,charset-normalizer,idna,openssl

# Icon & Splash
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

# Berechtigungen
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# --- GITHUB ACTIONS STABILITÄT ---
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

# Tastatur-Fix
android.softinput_mode = pan

# Automatisches Akzeptieren der Lizenzen (verhindert hängenbleiben)
android.accept_sdk_license = True

# Debug Level auf 2, falls es doch kracht (für bessere Analyse)
log_level = 2
