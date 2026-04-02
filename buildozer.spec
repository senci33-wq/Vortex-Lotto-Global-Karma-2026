[app]
# (str) Title of your application
title = Vortex Lotto

# (str) Package name
package.name = vortexlotto

# (str) Package domain (needed for android packaging)
package.domain = org.senci33

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (WICHTIG: json für die Projekte!)
source.include_exts = py,kv,json,png

# (str) Application version
version = 1.1

# (list) Application requirements
# WICHTIG: certifi ist nötig für die Quanten-Abfrage (SSL)
requirements = python3,kivy,requests,certifi,charset-normalizer,idna,urllib3

# (str) Custom source folders for requirements
# (list) Permissions
android.permissions = INTERNET

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Android API to use
android.api = 34
android.minapi = 21
p4a.branch = master
android.ndk = 25b
android.archs = arm64-v8a
android.release_artifact = aab
[buildozer]
log_level = 2
