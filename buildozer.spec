[app]
# (str) Title of your application
title = Vortex Lotto

# (str) Package name
package.name = vortexlotto

# (str) Package domain (needed for android packaging)
package.domain = org.senci33

# (list) Application requirements
# WICHTIG: Cython hier NICHT listen, das haben wir im Workflow installiert
requirements = python3,kivy==2.3.0,requests,certifi,openssl

# (int) Android API to use
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
# Version 25b ist die stabilste Wahl für Kivy 2.3.0 auf GitHub Runners
android.ndk = 25b

# (list) The Android architectures to build for
android.archs = arm64-v8a

# (bool) Use copy-libs (needed for some newer NDKs)
android.copy_libs = 1

# (int) Log level (0 = error only, 1 = info, 2 = debug)
# Auf 2 lassen, falls es doch noch einen Fehler gibt!
log_level = 2

# (bool) Allow to run buildozer as root (wichtig für CI)
buildozer.allow_org_name_start = 1
