[app]
title = Vortex Ultra Safe
package.name = vortexultrasafe
package.domain = org.senci33
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 8.8.1

# WICHTIG: numpy und openssl zwingend erforderlich
requirements = python3,kivy==2.3.0,numpy,requests,urllib3,charset-normalizer,idna,openssl

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# TASTATUR-FIX
android.softinput_mode = pan

# AUTOMATISIERUNG
android.accept_sdk_license = True
log_level = 2
