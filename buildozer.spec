[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,kv,json
version = 0.1

# Nur die Basis-Anforderungen, damit es schnell geht
requirements = python3,kivy,requests,certifi,openssl

# WICHTIG: Icons und Presplash bleiben komplett weg!
# Der Server nutzt dann einfach das Standard-Kivy-Logo.

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
