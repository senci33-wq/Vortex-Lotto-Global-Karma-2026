[app]
title = Vortex Lotto
package.name = vortexlotto
package.domain = org.senci33
source.dir = .
version = 1.0.0

# Anforderungen (keine Leerzeichen nach Kommas!)
requirements = python3,kivy==2.3.0,requests,certifi,openssl

android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.copy_libs = 1
buildozer.allow_org_name_start = 1
log_level = 2
