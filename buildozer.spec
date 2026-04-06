[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33

# WICHTIG: Keine Leerzeichen nach den Kommas!
requirements = python3,kivy==2.3.0,requests,certifi,openssl

# Android spezifisch
android.api = 34
android.minapi = 21

# NDK 25b ist die stabilste Version für Kivy 2.3.0 auf GitHub
android.ndk = 25b
android.ndk_path = 

# Architektur für moderne Smartphones (64-bit)
android.archs = arm64-v8a

# Erforderlich für neuere Android APIs
android.allow_backup = True
android.copy_libs = 1

# Verhindert Fehler beim Starten des Build-Prozesses im Runner
buildozer.allow_org_name_start = 1

# Log Level auf 2 lassen für detaillierte Fehlersuche
log_level = 2
