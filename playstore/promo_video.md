# Promo video — 30-second storyboard

Play Store accepts a YouTube link as a promo video. A short, punchy clip
above the fold drives a measurable lift in install rate.

## Specs
- **Length:** 30 s recommended (max 2 min)
- **Aspect:** 16:9 landscape (Play Store crops to 16:9)
- **Format:** YouTube link (unlisted is fine)
- **No audio narration required** — most users browse muted; show captions

## Storyboard

| Time | Visual | On-screen text | Audio cue |
|------|--------|---------------|-----------|
| 0:00–0:03 | App icon zooms onto an HP-blue background | **HP Printer Tools** | Soft swoosh |
| 0:03–0:07 | Hand reaches for an HP printer; phone screen lights up showing the home grid | "12 tools. One tap each." | Light pop |
| 0:07–0:11 | Tap "Print Photo" → photo picker → a glossy photo slides out of the printer | "Print photos straight from your gallery" | Paper-feed sound |
| 0:11–0:15 | Tap "Scan Document" → camera shutter → page appears as PDF preview | "Scan a page in seconds" | Camera click |
| 0:15–0:19 | Tap "ID Card Copy" → front + back capture → printed combined sheet | "Copy ID cards both sides on one page" | Subtle whoosh |
| 0:19–0:23 | Quick montage: Photocopy, Mobile Fax, Find Printer, Ink Levels | "Photocopy. Fax. Setup. Status." | Rising synth |
| 0:23–0:27 | Phone shows app gallery with all 12 cards visible | "Everything you need from your HP printer." | — |
| 0:27–0:30 | App icon + "Get HP Printer Tools" + Play Store button | **Free · No ads · No sign-up** | Final chime |

## Production tips

- Use a real HP printer if possible — DeskJet 4100, OfficeJet Pro 9015, or
  ENVY 6055 work well on camera and are commonly searched for.
- Shoot phone screen recordings at 60 fps with `adb shell screenrecord`
  then crop in DaVinci Resolve / iMovie:
  ```sh
  adb shell screenrecord --bit-rate 12000000 --size 1080x1920 /sdcard/demo.mp4
  adb pull /sdcard/demo.mp4 .
  ```
- Caption every spoken phrase — most users browse Play Store muted.
- Keep the icon in a corner of every cut so users associate the app with
  the visual.
- Upload to YouTube as **unlisted**, then paste the URL into Play Console
  → Main store listing → Promo video.

## Thumbnail
Use [playstore/feature_graphic.png](../feature_graphic.png) as the YouTube
thumbnail — it already matches the listing aesthetic.
