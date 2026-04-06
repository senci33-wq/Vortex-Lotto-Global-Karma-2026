[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
version = 1.1.0

# Nur die nötigsten Requirements
requirements = python3,kivy==2.3.0,requests,certifi,openssl

# WICHTIG: Erstmal nur für EINE Architektur bauen (spart 50% RAM/Zeit)
android.archs = arm64-v8a

# API Anpassungen
android.api = 34
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
