# Play Store screenshots

All assets are pre-rendered. Re-run `python3 scripts/generate_screenshots.py`
from the project root to refresh them.

## Phone (required — upload at least 2, max 8)
**Resolution:** 1080 × 1920 (16:9 portrait)

| File | Headline | What it shows |
|------|----------|---------------|
| [phone/01_home.png](phone/01_home.png) | "12 powerful tools, one tap away" | Full grid of all 12 tools |
| [phone/02_print_photo.png](phone/02_print_photo.png) | "Print photos in seconds" | Print Photo detail screen |
| [phone/03_scan.png](phone/03_scan.png) | "Turn your phone into a scanner" | Scan tool |
| [phone/04_id_copy.png](phone/04_id_copy.png) | "Copy IDs both sides on one page" | ID card tool |
| [phone/05_setup.png](phone/05_setup.png) | "Set up any HP printer in seconds" | Setup tool |

**Upload order:** `01_home → 02_print_photo → 03_scan → 04_id_copy → 05_setup`.
The first one is by far the most important — it shows variety and the
quantified value prop ("12 tools").

## 7-inch tablet (optional but recommended)
**Resolution:** 1200 × 1920

- [tablet7/01_home.png](tablet7/01_home.png)
- [tablet7/02_print_photo.png](tablet7/02_print_photo.png)
- [tablet7/03_setup.png](tablet7/03_setup.png)

## 10-inch tablet (optional but recommended)
**Resolution:** 1600 × 2560

- [tablet10/01_home.png](tablet10/01_home.png)
- [tablet10/02_scan.png](tablet10/02_scan.png)
- [tablet10/03_id.png](tablet10/03_id.png)

## Capturing real-device screenshots (optional, post-launch)

For higher conversion, replace the rendered mockups with real screenshots
from a Pixel device:

```sh
adb shell screencap -p /sdcard/01_home.png
adb pull /sdcard/01_home.png playstore/screenshots/phone/
```

Then overlay the marketing tagline using the same Python script's
`compose_marketing()` function — pass the real device PNG instead of the
mock UI render.
