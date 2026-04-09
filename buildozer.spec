[app]

# (str) Titel deiner App
title = Vortex Ultra Safe

# (str) Paket-Name (Keine Leerzeichen!)
package.name = vortexultrasafe

# (str) Paket-Domain (dein GitHub-Name ist ideal)
package.domain = org.senci33

# (str) Quellcode-Verzeichnis
source.dir = .

# (list) Dateiendungen, die eingeschlossen werden
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Versionsnummer (BEI JEDEM UPDATE ERHÖHEN!)
version = 8.8.1

# (list) App-Abhängigkeiten (WICHTIG für requests und numpy)
# Wir fügen openssl hinzu, damit https-Anfragen (Sync) funktionieren
requirements = python3,kivy==2.3.0,numpy,requests,urllib3,charset-normalizer,idna,openssl

# (str) Custom Icon
icon.filename = %(source.dir)s/icon.png

# (str) Presplash (Ladebildschirm)
presplash.filename = %(source.dir)s/icon.png

# (list) Berechtigungen (INTERNET ist Pflicht für deinen Sync)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API (34 ist aktuell für 2026)
android.api = 34
android.minapi = 21
android.ndk = 25b

# (str) Android Architekturen (arm64 ist Standard für moderne Handys)
android.archs = arm64-v8a, armeabi-v7a

# --- TASTATUR OPTIMIERUNG ---
# 'pan' sorgt dafür, dass das Layout hochschiebt, wenn die Tastatur kommt
android.softinput_mode = pan

# (bool) Erlaube Backup der Daten durch Google (optional)
android.allow_backup = True

# --- GITHUB ACTIONS FIX ---
# Verhindert, dass der Build abbricht, wenn Lizenzen bestätigt werden müssen
android.accept_sdk_license = True
