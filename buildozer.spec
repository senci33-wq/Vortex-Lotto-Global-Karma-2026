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
source.include_exts = py,kv,json,png,jpg

# (str) Application version
version = 1.2

# (list) Application requirements
# WICHTIG: openssl ist nötig für HTTPS-Abfragen (SSL)
requirements = python3,kivy,requests,certifi,charset-normalizer,idna,urllib3,openssl

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

# ==========================================================
# Android specific configurations
# ==========================================================

# (int) Android API to use (33 ist stabiler für GitHub Actions)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version
android.build_tools_version = 33.0.0

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The Android arch to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup
android.allow_backup = True

# (str) python-for-android branch to use
p4a.branch = master

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
