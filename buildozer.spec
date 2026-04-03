# (1) Der App-Titel und Paketname (Sicherstellen, dass keine Sonderzeichen drin sind)
title = MeinLottoProjekt
package.name = lottovortex
package.domain = org.deinname

# (2) Die Requirements - Das ist das Herzstück!
# Wir setzen Kivy auf 2.3.0 fest und fügen pyjnius hinzu
requirements = python3,kivy==2.3.0,pyjnius,requests,certifi,charset-normalizer,idna,urllib3

# (3) Android Spezifikationen
# API 34 ist aktuell Standard für den Play Store
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

requirements = python3,kivy==2.3.0,pyjnius,requests,certifi,charset-normalizer,idna,urllib3
# Falls diese Zeile auskommentiert ist (mit #), entferne das #
android.permissions = INTERNET

# (5) Architekturen
# Für moderne Handys und den Play Store brauchst du beide:
android.archs = arm64-v8a, armeabi-v7a

# (6) Log-Level auf 2 lassen, damit wir Fehler sehen
log_level = 2
