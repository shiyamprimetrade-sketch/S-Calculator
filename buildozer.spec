[app]
title = S-Calculator
package.name = scalculator
package.domain = online.slickk
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0
android.minapi = 24
android.api = 35
android.archs = arm64-v8a
android.permissions =
android.accept_sdk_license = True
# No network permission: calculator works fully offline.
[buildozer]
log_level = 2
warn_on_root = 1
