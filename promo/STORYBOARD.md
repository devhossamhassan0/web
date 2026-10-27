# ResizePhoto — promo storyboard

- Format: 1080×1920 vertical, 20 s, 60 fps (3 subframes per frame blended with ffmpeg tmix for motion blur)
- Grid: 120 BPM, beat = 0.5 s, bar = 2 s
- Audio: no music and no voice-over. Synthesized motion sounds are the whole soundtrack, −14 LUFS
- Accent: orange `#FF5B14` on near-black `#0B0B0C` and off-white `#F5F4F1`
- Type: IBM Plex Sans Arabic (letter-spacing 0 so letters stay joined), Inter (tight tracking), right-to-left layout
- Content comes from a real run of the app: 4 PNGs (bankette, bed, dresser, wardrobe) to WEBP at quality 92,
  saving 86.5–89.9% per file and 13.6 MB in total. Output formats: JPG, PNG, WEBP, GIF
- On-screen text never ends with a full stop

| Bar | Time | Picture (on the beat) | Motion sound (peak on the cue) |
|---|---|---|---|
| 1 Hook | 0.0–2.0 | 0.0 «صور كتير» · 0.5 «من صيغة» · 1.0 «لصيغة» · 1.5 «تانية؟» masked reveals | `word_swish` 0.0 / 0.5 / 1.0 / 1.5 |
| 2 App | 2.0–4.0 | 2.0 «صيغة» glides into «صيغة الإخراج» in the app · 2.5 the 4 files land · 3.0 JPG → WEBP · 3.5 «حوّل واضغط», a dark circle opens to 4.0 | `morph` 2.0 · `ui_click` 2.5 / 3.0 / 3.5 · `riser` peaking 4.0 |
| 3 Drop | 4.0–6.0 | «كل صورك مرة واحدة» · scan line crosses each file on its beat (4.0 / 4.5 / 5.0 / 5.5) and .png rolls to .webp | `drop_sub` 4.0 · `scan` · `lock` 4.0 / 4.5 / 5.0 / 5.5 |
| 4 Formats | 6.0–8.0 | «اختار الصيغة المناسبة لشغلك» · 6.0 JPG · 6.5 PNG · 7.0 WEBP (orange) · 7.5 GIF | `match` 6.0 · `word_swish` 6.0 / 6.5 / 7.0 / 7.5 |
| 5 Ring | 8.0–10.0 | 3D ring of uses with floor reflection · slow turn, whip at 9.5 · lands on «صور منتجات» at 10.0 | `carousel` · `whip` 9.5 |
| 6 Result | 10.0–12.0 | «ضغط وتحويل في خطوة واحدة» · bed.png card · 11.0 flips to −89.8% bed_compressed.webp | `match` 10.0 · `flip` 11.0 |
| 7 Stats | 12.0–14.0 | push cuts · 12.0 «13.6 MB اتوفّروا من ٤ صور بس» · 13.0 «89.9% أقل في حجم الصورة» | `push` 12.0 / 13.0 |
| 8 Ticker | 14.0–16.0 | 14.0 «اختار» · 14.5 «حدّد» · 15.0 «اضغط» · 15.5 «حوّل» (orange) | `word_swish` on each |
| 9 Logo | 16.0–18.0 | 16.0 ResizePhoto · 16.5 «حوّل صورك بسهولة» · 17.0 «وركّز في شغلك أكتر» | `logo` 16.0 · `word_swish` 16.5 / 17.0 |
| 10 CTA | 18.0–20.0 | 18.0 «أكتر صيغة» · 18.5 «بتستخدمها إيه؟» + «اكتبلي في الكومنتات 👇» · 19.0–20.0 fade to black | `word_swish` 18.0 / 18.5 · `outro` 19.0 |

## Build

- `promo/index.html`: the composition; `window.seek(t)` sets every style from `t` alone
- `node promo/tools/probe.cjs <out_dir> <t> ...`: single frames for review
- `promo/tools/build.sh <work_dir> <out.mp4>`: sounds → subframes → motion blur → mux
- `promo/tools/make_sfx.py`: synthesizes every sound and places each by its measured peak
- Fonts: IBM Plex Sans Arabic and Inter, both under the SIL Open Font License
