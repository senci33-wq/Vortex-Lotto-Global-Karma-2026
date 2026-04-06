[app]
title = Vortex Karma
package.name = vortexkarma
package.domain = org.karma
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,txt,md
version = 1.0.0

# OPTIMIERUNG: Cython und hostpython3 explizit für Stabilität
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

orientation = portrait
fullscreen = 1

# OPTIMIERUNG: API 34 benötigt oft Java 17 (im Workflow bereits gesetzt)
android.api = 34
android.minapi = 21
# NDK 25b ist gut, aber 25c ist oft stabiler für API 34
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a,armeabi-v7a

# WICHTIG: Für Tests in GitHub Actions erst mal auf 'apk' lassen. 
# 'aab' brauchst du nur für den Play Store Upload.
android.release_artifact = apk

# Berechtigungen
android.permissions = INTERNET

android.enable_androidx = True
# Multidex ist bei KivyMD oft nötig
android.multidex = True

# ACHTUNG: Deaktiviere das Signieren für den ersten Build in GitHub Actions!
# Wenn du kein Keystore-File im Repo hast, bricht der Build sofort ab.
android.skip_update_check = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

[android]
# Hilft gegen Speicherfehler während des Kompilierens
android.extra_args = --enable-optimizations
