[app]
# -- Basis Informationen --
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# -- Anforderungen (Internet & SSL fix) --
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer,openssl

# -- Bilder (Direkte Pfade ohne Umwege) --
# WICHTIG: Die Dateien müssen icon.png und presplash.png heißen!
icon.filename = icon.png
presplash.filename = presplash.png

# -- Android Einstellungen --
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
