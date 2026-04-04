[app]

title = Vortex Karma
package.name = vortexkarma
package.domain = org.karma
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json,txt,md
version = 1.0.0
requirements = python3,kivy,kivymd
orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 23
android.ndk = 25b
android.ndk_api = 23
android.archs = arm64-v8a,armeabi-v7a

android.release_artifact = aab
android.permissions = INTERNET

android.enable_androidx = True
android.multidex = True
android.gradle_dependencies = com.android.support:multidex:1.0.3

android.sign = True
android.keystore = my-release-key.keystore
android.keyalias = myappkey

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# zusätzliche libs hier eintragen

[android]
android.extra_args = --enable-optimizations

[spelling]
ignore_words = kivy,kivymd 
