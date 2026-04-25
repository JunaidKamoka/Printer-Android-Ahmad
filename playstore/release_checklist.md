# Release checklist

A short, ordered list to take HP Printer Tools from local source to a
signed Play Store upload.

## 1. Code

- [ ] Bump `versionCode` and `versionName` in `app/build.gradle.kts`
- [ ] Update `playstore/listing.md` "What's new" section
- [ ] Run the app on a device, confirm every tool launches
- [ ] Print a real document via HP Print Service Plugin

## 2. Signing

- [ ] Generate a release keystore (one-time):
  ```sh
  keytool -genkey -v -keystore release.jks -keyalg RSA -keysize 2048 \
          -validity 10000 -alias hp-printer-release
  ```
- [ ] Copy `keystore.properties.example` → `keystore.properties` and fill in real values
- [ ] Move `release.jks` to a safe location outside source control
  (e.g. `~/keystores/hp-printer/release.jks`) and update `storeFile` accordingly
- [ ] **Back up the keystore.** If you lose it you cannot publish updates.

## 3. Build

```sh
./gradlew clean
./gradlew bundleRelease         # produces app/build/outputs/bundle/release/app-release.aab
./gradlew assembleRelease       # produces a release APK if you need it
```

## 4. Verify

- [ ] Install the release APK on a clean device:
  `adb install -r app/build/outputs/apk/release/app-release.apk`
- [ ] App icon renders correctly (square + round + themed)
- [ ] Splash screen flashes briefly with HP-blue background
- [ ] All 12 tools work; no crashes

## 5. Play Console upload

- [ ] Go to Play Console → Create app
- [ ] Main store listing: copy text from `playstore/listing.md`
- [ ] Upload `playstore/play_store_icon.png` (512×512) as the high-res icon
- [ ] Upload `playstore/feature_graphic.png` (1024×500) as the feature graphic
- [ ] Take 4–8 device screenshots and upload them
- [ ] Set the privacy policy URL (host `playstore/privacy_policy.md` somewhere public)
- [ ] App content: complete the data-safety form (we collect nothing)
- [ ] Choose target audience, content rating
- [ ] Production track → upload `app-release.aab` → roll out
