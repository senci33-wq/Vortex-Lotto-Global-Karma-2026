[app]
# (str) Name der App auf dem Handy
title = Vortex Lotto

# (str) Interner Paketname (keine Leerzeichen)
package.name = vortexlotto

# (str) Deine Domain (identifiziert dich als Entwickler)
package.domain = org.senci33

# (str) Verzeichnis in dem die main.py liegt
source.dir = .

# (list) Dateiendungen die mit in die App müssen (json wichtig für Projekte!)
source.include_exts = py,kv,json,png

# (str) Versionsnummer (immer erhöhen für Updates!)
version = 1.0.

# (list) Wichtige Pakete für Kivy + Internet + SSL
requirements = python3,kivy,requests,certifi,urllib3,idna,charset-normalizer

# (list) Berechtigungen (Internet ist Pflicht!)
android.permissions = INTERNET

# (str) Pfad zu deinem Logo
icon.filename = %(source.dir)s/icon.png

# (str) Pfad zum Startbildschirm (Splash)
presplash.filename = %(source.dir)s/presplash.png

# (str) Ausrichtung
orientation = portrait

# (int) Android API Level (31 ist aktuell Standard für Google Play)
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
