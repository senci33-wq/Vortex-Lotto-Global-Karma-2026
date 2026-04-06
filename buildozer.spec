[app]
# (str) Title of your application
title = Vortex Lotto
# (str) Package name
package.name = vortexlotto
# (str) Package domain
package.domain = org.senci33

# (list) Application requirements
# WICHTIG: Cython hier NICHT eintragen (wird über den Workflow installiert)
requirements = python3,kivy==2.3.0,requests,certifi,openssl

# (int) Android API to use
android.api = 34
# (int) Minimum API your APK will support
android.minapi = 21
# (str) Android NDK version to use (25b ist am stabilsten für CI)
android.ndk = 25b

# (list) Architectures to build for (arm64-v8a ist Standard für moderne Handys)
android.archs = arm64-v8a

# (bool) Copy libs to the setup (behebt oft "Broken Pipe" Fehler)
android.copy_libs = 1

# (int) Log level (2 für detaillierte Fehlersuche im CI)
log_level = 2

# (bool) Allow to run buildozer as root (erforderlich für GitHub Actions)
buildozer.allow_org_name_start = 1
