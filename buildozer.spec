[app]
title = Vortex Karma
package.name = vortexkarma
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Hinzugefügt: openssl für HTTPS/Requests Support
requirements = python3,kivy,requests,urllib3,certifi,idna,charset-normalizer,openssl

orientation = portrait
fullscreen = 0

# Nur arm64-v8a ist super für moderne Geräte (schnellerer Build)
android.archs = arm64-v8a
android.allow_backup = True
android.permissions = INTERNET
