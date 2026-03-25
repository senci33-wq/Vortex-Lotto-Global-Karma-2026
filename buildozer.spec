[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,kv,json
version = 0.2

# WICHTIG: Diese 4 müssen drin sein für die Quanten-Abfrage!
requirements = python3,kivy,requests,certifi

orientation = portrait
fullscreen = 0
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Keine Bilder = Kein Absturz
# icon.filename = %(source.dir)s/icon.png <-- Bleibt aus!

[buildozer]
log_level = 2

