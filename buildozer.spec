[app]

# (str) Title of your application
title = Vortex Lotto

# (str) Package name
package.name = vortexlotto

# (str) Package domain (needed for android packaging)
package.domain = org.senci33

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (WICHTIG: json für deine Projekte!)
source.include_exts = py,kv,json,png

# (str) Application version
version = 0.9

# (list) Application requirements
# WICHTIG: certifi für SSL-Verschlüsselung der Quanten-API!
requirements = python3,kivy,requests,certifi,urllib3,charset_normalizer,idna

# (str) Custom source folders for requirements
# (list) Permissions
android.permissions = INTERNET

# (str) Icon of the application
# Wenn du ein Logo hast, lade es als icon.png hoch und aktiviere diese Zeile:
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Android API to use
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
