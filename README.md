# HP Printer Tools (Android · Kotlin · Compose)

A simple Android app that wraps **12 easy-to-use tools** for an HP Smart printer.
Built with **Kotlin + Jetpack Compose + Material 3** so the code stays short and
modern. Printing is done through Android's built-in `PrintHelper` /
`PrintManager`, which works with HP printers via the **HP Print Service Plugin**
(or Mopria).

## Tools included

| # | Tool | What it does |
|---|------|--------------|
| 1 | Print Photo | Pick a picture from gallery and print |
| 2 | Print Document | Pick PDF / DOCX / image and print |
| 3 | Scan Document | Capture a page with the camera, then print or save |
| 4 | Photocopy | Snap a page and immediately print a copy |
| 5 | ID Card Copy | Capture front + back, print combined on one page |
| 6 | Mobile Fax | Compose an email with attachment via your mail app |
| 7 | Find Printer | Open Wi-Fi settings to join the printer's network |
| 8 | Printer Status | Open Android print services to check status |
| 9 | Ink Levels | Open HP supplies page in browser |
| 10 | Setup Printer | Open `123.hp.com/setup` in browser |
| 11 | Print Web Page | Open a website to use the browser's print menu |
| 12 | HP Print Plugin | Install the HP Print Service Plugin from Play Store |
| 13 | App Settings | Open this app's permissions screen |

## Project layout

```
Printer/
├── build.gradle.kts          ← root plugins
├── settings.gradle.kts
├── gradle.properties
├── gradle/wrapper/gradle-wrapper.properties
└── app/
    ├── build.gradle.kts
    ├── proguard-rules.pro
    └── src/main/
        ├── AndroidManifest.xml
        ├── java/com/ahmad/hpprinter/
        │   ├── MainActivity.kt           ← entry point + nav
        │   └── ui/
        │       ├── Tools.kt              ← 12 tool definitions
        │       ├── Actions.kt            ← what each tool does
        │       ├── HomeScreen.kt         ← 2-column grid
        │       ├── ToolScreen.kt         ← detail + launchers
        │       └── theme/Theme.kt        ← HP-blue theme
        └── res/                          ← strings, colors, icon
```

## Build & run

1. Open the `Printer` folder in **Android Studio Hedgehog or newer**.
2. Let Studio sync — it will download Gradle 8.9 and generate the wrapper.
3. Pick a device or emulator running **Android 7.0 (API 24)** or higher.
4. Press ▶ Run.

> If Studio asks to add a wrapper, accept. From the command line you can run
> `gradle wrapper` once (with a system-installed Gradle ≥ 8.9) to generate
> `gradlew` and `gradlew.bat` before building.

## Printing on a real device

Real printing happens through Android's print framework. To make sure your
HP printer is discoverable:

1. Open **Tool 12 → HP Print Plugin** and install it from the Play Store.
2. On the printer, enable **Wi-Fi Direct** or join your home Wi-Fi.
3. Open **Tool 7 → Find Printer** to confirm the phone is on the same network.
4. Use **Tool 1 / 2** — the Android print dialog should list your HP printer.

## Tech stack

- Kotlin 2.0.20, AGP 8.5.2
- Jetpack Compose (BOM 2024.09.02), Material 3
- Navigation Compose 2.8
- `androidx.core:core-splashscreen` 1.0.1 (system-managed splash)
- `androidx.print` `PrintHelper` for image printing, `Intent(ACTION_VIEW)`
  with `application/pdf` for documents
- Min SDK 24, Target SDK 34

## Publishing

Everything needed for the Play Store is in [playstore/](playstore/) and
[scripts/](scripts/).

| File | Purpose |
|------|---------|
| [playstore/play_store_icon.png](playstore/play_store_icon.png) | 512×512 high-res icon |
| [playstore/feature_graphic.png](playstore/feature_graphic.png) | 1024×500 feature graphic |
| [playstore/screenshots/phone/](playstore/screenshots/phone/) | 5 phone screenshots (1080×1920) |
| [playstore/screenshots/tablet7/](playstore/screenshots/tablet7/) | 3 7-inch tablet screenshots |
| [playstore/screenshots/tablet10/](playstore/screenshots/tablet10/) | 3 10-inch tablet screenshots |
| [playstore/listing.md](playstore/listing.md) | ASO-optimized title, short + long descriptions, keyword strategy |
| [playstore/privacy_policy.md](playstore/privacy_policy.md) | Privacy policy text — host on a public URL |
| [playstore/data_safety.md](playstore/data_safety.md) | Pre-filled answers for Play Console's Data safety form |
| [playstore/promo_video.md](playstore/promo_video.md) | 30-second promo video storyboard |
| [playstore/release_checklist.md](playstore/release_checklist.md) | Step-by-step from `keytool` to AAB upload |

Re-run [scripts/generate_icons.py](scripts/generate_icons.py) and
[scripts/generate_screenshots.py](scripts/generate_screenshots.py) any
time the design changes — they regenerate every PNG asset deterministically.
