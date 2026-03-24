[app]
title = Vortex Karma
package.name = vortexkarma
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# WICHTIG: Die Anforderungen für deine Quanten-Abfrage
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer

orientation = portrait
fullscreen = 0

# TURBO-MODUS: Nur für moderne Handys bauen spart 50% Zeit
android.archs = arm64-v8a
android.allow_backup = True

# Berechtigungen für das Internet (wegen der API)
android.permissions = INTERNET
