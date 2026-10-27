# ResizePhoto — promo storyboard

- Format: 1080×1920 vertical, 20 s, 60 fps (rendered from 3 subframes per frame)
- Grid: 120 BPM, beat = 0.5 s, bar = 2 s. Re-calibrated to the real kick hits once the song arrives
- Accent: orange `#FF5B14` on near-black `#0B0B0C` and off-white `#F5F4F1`
- Type: IBM Plex Sans Arabic (Arabic, letter-spacing 0 so letters stay joined), Inter (Latin, tight tracking), right-to-left layout
- Safe area: top 220 px, bottom 400 px, right 140 px kept clear of Reels/TikTok UI
- On-screen text never ends with a full stop

| Bar | Time | Script line | Picture (on the beat) | Motion sound (peak on the cue) |
|---|---|---|---|---|
| 1 Hook | 0.0–2.0 | بتتعامل مع صور كتير؟ | 0.0 «صور كتير» · 0.5 «من صيغة» · 1.0 «لصيغة» · 1.5 «تانية؟» masked reveals | `word_swish` on 0.0 / 0.5 / 1.0 / 1.5 |
| 2 UI | 2.0–4.0 | اختار الصور وحدّد الصيغة | 2.0 «صيغة» morphs into the app · 2.5 cursor picks 3 real images · 3.0 clicks WEBP · 3.5 clicks «حوّل», circle opens to 4.0 | `morph` 2.0 · `ui_click` 2.5 / 3.0 / 3.5 · `riser` peaking 4.0 |
| 3 Drop | 4.0–6.0 | بدل ما تحوّل كل صورة لوحدها | 4.0 4×4 wall of real clips, scan line top to bottom · 4.5 / 5.0 / 5.5 three winners outlined orange · «كل صورك مرة واحدة» | `drop_sub` 4.0 (under the song's drop) · `scan` · `lock` 4.5 / 5.0 / 5.5 |
| 4 Formats | 6.0–8.0 | JPG أو PNG أو WEBP | match cut from a winner · 6.0 JPG · 6.5 PNG · 7.0 WEBP in orange | `match` 6.0 · `word_swish` 6.0 / 6.5 / 7.0 |
| 5 Carousel | 8.0–10.0 | مواقع، متاجر، منتجات | 3D carousel of real clips with floor reflections · 9.5 motion-blurred whip · 10.0 settles on hero | `carousel` swelling to 9.0 · `whip` 9.5 |
| 6 Phone + results | 10.0–12.0 | البرنامج يجهّز ملفاتك | 10.0 hero inside a phone, panel «منتج.jpg · [real size]» below · 11.0 panel flips · 11.5 «WEBP · [real size]» | `match` 10.0 · `flip` 11.0 |
| 7 Stats | 12.0–14.0 | وفّر وقتك ومجهودك | push cuts · 12.0 stat 1 · 13.0 stat 2 (real numbers only) | `push` 12.0 / 13.0 |
| 8 Ticker | 14.0–16.0 | أسهل وأسرع | 14.0 «اختار» · 14.5 «حدّد» · 15.0 «حوّل» in orange | `word_swish` 14.0 / 14.5 / 15.0 |
| 9 Logo | 16.0–18.0 | ResizePhoto — حوّل صورك بسهولة | 16.0 ResizePhoto · 16.5 «حوّل صورك بسهولة» · 17.0 «وركّز في شغلك أكتر» | `logo` 16.0 |
| 10 CTA | 18.0–20.0 | اكتبلي في الكومنتات | 18.0 «أكتر صيغة بتستخدمها إيه؟ 👇» · 18.5–20.0 fade to black | `outro` 18.5 |

## Motion sounds

All effects are synthesized by `promo/tools/make_sfx.py` (no third-party samples, so they are free for commercial use).
`promo/sfx/sfx.json` stores each file's measured peak; the mix places a sound at `cue − peak` so the peak lands on the cue.
`promo/sfx/cue_preview.m4a` is the 20 s cue track over a quiet metronome (accented on each downbeat).
In the final mix the effects sit well under the music and the whole is loudness-normalized to −14 LUFS.

## Waiting on

- 10–20 vertical clips you own → `promo/clips/`
- A song licensed for commercial use with a clear drop → `promo/music/` (this container cannot reach Mixkit)
- Screenshots or a screen recording of ResizePhoto → `promo/ui/`
- Real numbers for bar 7, or 3 before/after images converted with the app
