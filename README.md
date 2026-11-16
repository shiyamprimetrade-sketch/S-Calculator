# S-Calculator — Offline Android calculator

A dark-theme, offline Kivy calculator with arithmetic, parentheses, postfix percentages, square root, history (last 20 calculations in memory), and graceful error messages. No network calls, analytics, or Android permissions.

## Expression rules

- `+ - * /` follow standard precedence; parentheses override it.
- `%` divides the immediately preceding number/expression by 100: `50%` = `0.5`; `200*10%` = `20`. This is **not** the alternative commercial-calculator behavior where `200+10%` means 220; here it means 200.1.
- `√9` or `√(9+7)` is supported. `√-1` reports an error.
- Explicit multiplication is required (`2*(3+4)`, not `2(3+4)`).
- `AC` and `C` clear the current expression; `⌫` removes the last character.
- History is in memory only, and resets when the app closes.

## Run on desktop (Python 3.11–3.13)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows: activate `.venv\\Scripts\\activate` instead.

## Run tests (no Kivy needed)

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q main.py calculator.py tests
```

## Build Android APK (recommended: Ubuntu 22.04/24.04 x86_64)

Buildozer/python-for-android requires a Linux build environment and Android SDK/NDK. The **first build downloads toolchains and needs internet**; the finished app works offline.

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3 python3-pip python3-venv \
  python3-dev build-essential libffi-dev libssl-dev autoconf automake libtool \
  pkg-config zlib1g-dev libncurses5-dev cmake
python3 -m venv ~/buildozer-venv
source ~/buildozer-venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython==0.29.34
cd s_calculator_project
buildozer -v android debug
ls -lh bin/*.apk
```

Buildozer may request SDK license acceptance or additional dependencies for the host distribution. If the Android toolchain reports incompatibilities, use a supported Ubuntu environment and versions documented by python-for-android; do not assume that changing `android.api` fixes host errors. This project has **not** been APK-compiled in the provided execution environment.

## Termux on Android

Native Buildozer APK compilation **inside Termux is not a supported/reliable path** because Buildozer's Android toolchain targets Linux hosts and depends on SDK/NDK binaries generally unavailable for Android ARM64. Do **not** expect `pkg install buildozer` to produce an APK. Use Termux to edit source, run the standard-library calculator tests, and push files to GitHub, then build using Ubuntu x86_64 (PC, VM, or CI). A remote Ubuntu builder can be controlled from your phone via SSH or GitHub Actions.

```bash
pkg update
pkg install python git
cd ~/s_calculator_project
python -m unittest discover -s tests -v
```

## Install generated APK

Copy `bin/*.apk` from the Linux builder to your phone, open it, and approve installation from the selected file manager when prompted. Debug builds are for testing; release distribution requires release signing and on-device testing.

## Acceptance tests not yet performed

Android SDK/NDK build, actual APK installation, device layout/touch feedback, rotation/accessibility, performance, and release signing require a supported Android build host and physical/emulated device.
