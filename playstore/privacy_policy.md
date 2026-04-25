# Privacy Policy — HP Printer Tools

_Last updated: 25 April 2026_

HP Printer Tools ("the app") is a utility for printing, scanning, copying
and faxing through your HP printer. The app is published by Ahmad
("we", "our") and is not affiliated with HP Inc.

## What data we collect

**None.** The app does not collect, store, transmit or sell any personal
information. There are no analytics SDKs, no advertising SDKs, no
crash-reporting services, and no remote servers we operate.

## What the app does on your device

- Reads a photo or document you explicitly pick, only to send it to the
  Android print framework. The file does not leave your device except
  through the print job you start.
- Captures pictures with the camera, only when you tap a tool that
  requires it. Captured images stay on your device unless you choose to
  print or share them.
- Opens local system screens (Wi-Fi settings, app settings, print services).
- Opens public HP web pages (123.hp.com, hp.com) in your browser when you
  tap a tool that supports those flows. Your browser, not this app, is
  responsible for any data sent to those websites.

## Permissions

The app requests **only one permission**: `INTERNET`. This is a normal
permission (not user-prompted) that the Android print framework needs to
deliver print jobs to networked printers.

| Permission | Why it is requested |
|------------|--------------------|
| `android.permission.INTERNET` | So the system print framework can reach your printer over Wi-Fi |

What the app uses **without requesting any permission**:

- **Camera** — through the system camera app (`ACTION_IMAGE_CAPTURE`).
  The system app handles the capture; we never access the camera directly,
  so no camera permission is required or requested.
- **Photos / files** — through the system photo and document pickers
  (Storage Access Framework). We receive only the single URI you select,
  and only for as long as the app is open.

We never share these permissions or any data they expose with anyone.

## Children

The app does not target children under 13 and does not collect data from
any user, including children.

## Third-party services

The app does not use third-party SDKs. It launches your browser and your
email client through standard Android intents; those apps have their own
privacy policies.

## Changes

If the policy changes we will publish a new version of the app and update
the "Last updated" date above.

## Contact

ahmad@example.com   ← replace with a real address before publishing
