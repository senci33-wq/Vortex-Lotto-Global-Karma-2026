[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33

# Keine Leerzeichen nach den Kommas!
requirements = python3,kivy==2.3.0,requests,certifi,openssl

# Android-Konfiguration
android.api = 34
android.minapi = 21

# NDK 25b ist zwingend für Ubuntu 24.04 (höhere Versionen verursachen glibc-Fehler)
android.ndk = 25b
android.ndk_path = 

# Architektur für moderne Geräte
android.archs = arm64-v8a

# Wichtig für den Erfolg des Builds
android.accept_sdk_license = True
android.copy_libs = 1

# CI-spezifische Erlaubnis
buildozer.allow_org_name_start = 1

# Log-Level für detaillierte Fehleranalyse im GitHub-Log
log_level = 2
