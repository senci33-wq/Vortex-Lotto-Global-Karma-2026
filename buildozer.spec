[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
source.include_exts = py,kv,json
version = 0.7

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
17 # (str) Title of your application
18 title = ZellSchutz
19
20 # (str) Package name
21 package.name = zellschutzapp
22
23 # (str) Package domain (needed for android packaging)
24 package.domain = org.vortex
25
26 # (str) Icon of the application
27 icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2

