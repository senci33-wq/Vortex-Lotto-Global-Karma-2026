[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# WICHTIG: Alle Internet-Voraussetzungen sind hier aktiv
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer,openssl

# Deine Bilder (ohne # davor!)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

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
