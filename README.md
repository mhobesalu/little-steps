# Little Steps

Visual routine app for kids (store name: "Little Steps: Visual Routines"). Picture cards for morning, going out and bedtime, one step at a time with "Next up" and a gentle timer bar. Parents can make their own routines and chores, pick colours and pictures, and use their own photos as cards. English + Estonian: to add a language, copy the `en` block in `STR` and add the language to each entry in `CARDS`.

- Free download: the Morning routine. One-time in-app purchase (planned $7.99) unlocks every routine, own routines and photo cards. No ads, no accounts, no subscription.
- All data, photos included, stays on the device (localStorage). Nothing is sent anywhere.
- Purchases sit behind a grown-up check (a times-table question). The grown-up settings open by holding the gear button for 1.2 s.
- The web version (index.html opened in a browser) is a free demo with everything open.
- All picture cards and the app icon are original drawings. Fonts (Fredoka, Nunito, OFL) are bundled in `fonts/`.

## Native apps (Capacitor, same setup as Mischief & Motive)

- Bundle ID / package: `ee.silgrowth.littlesteps`, seller Sild Growth OÜ.
- In-app product IDs: App Store `ee.silgrowth.littlesteps.full` (non-consumable), Google Play `full` (one-time product).
- `native/build-web.js` copies `index.html` and `fonts/` into `native/www`.
- GitHub Actions: "iOS build check" and "Android build check" run on every push; "iOS release to TestFlight" and "Android release" are run by hand and need the same secrets as Mischief & Motive (listed at the top of each workflow file).
