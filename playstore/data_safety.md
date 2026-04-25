# Play Console — Data safety form answers

Pre-filled answers for App content → **Data safety** section. Match
these in Play Console exactly to avoid review delays.

---

## Does your app collect or share any of the required user data types?
**No.**

(Justification: the app reads files the user explicitly picks via system
pickers, captures camera images on demand, and hands content to Android's
print framework. No data leaves the device through code we wrote.)

## Is all of the user data collected by your app encrypted in transit?
**N/A — no data is collected.**

## Do you provide a way for users to request that their data is deleted?
**N/A — no data is collected.**

## Data types

For every category in the Play Console form, select **Not collected**:

| Category | Status |
|----------|--------|
| Personal info (name, email, address, IDs, etc.) | Not collected |
| Financial info | Not collected |
| Health & fitness | Not collected |
| Messages | Not collected |
| Photos and videos | Not collected (user-picked images stay on device) |
| Audio files | Not collected |
| Files and docs | Not collected (user-picked files stay on device) |
| Calendar | Not collected |
| Contacts | Not collected |
| App activity | Not collected |
| Web browsing | Not collected |
| App info and performance | Not collected |
| Device or other IDs | Not collected |

## Security practices
- ☑ Data is encrypted in transit (vacuously true — there's no network
  data flow we control beyond the user's browser)
- ☑ Users can request that data be deleted (vacuously true — no data exists)
- ☑ Committed to Play's Families Policy: **N/A** (not targeted at children)

## Privacy policy URL
Set this in Play Console → Main store listing.
Host the contents of [privacy_policy.md](privacy_policy.md) on:
- GitHub Pages (free, fast)
- A subpage of your portfolio website
- A free Notion / Google Sites page

The URL must be reachable, return HTTP 200, and contain the word
"privacy" — Play crawlers reject 404s, redirects to login walls, or pages
that show a different policy than what was declared.
