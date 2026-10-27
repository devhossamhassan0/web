// Full render: node promo/tools/render.cjs <frames_dir> [workers]
// Writes 3 subframes per 60 fps frame (t - 1/240, t, t + 1/240) as JPEGs for ffmpeg tmix.
const { chromium } = require("playwright");
const { mkdirSync } = require("node:fs");
const { resolve } = require("node:path");

const root = resolve(__dirname, "..");
const out = process.argv[2];
const workers = +(process.argv[3] || 4);
const FPS = 60;
const OFFSETS = [-1 / 240, 0, 1 / 240];

(async () => {
  mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const duration = 20;
  const total = Math.round(duration * FPS);
  let next = 0;
  await Promise.all(Array.from({ length: workers }, async () => {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    await page.goto(`file://${root}/index.html`);
    while (next < total) {
      const f = next++;
      for (let k = 0; k < 3; k++) {
        const t = Math.min(duration - 1e-4, Math.max(0, f / FPS + OFFSETS[k]));
        await page.evaluate((t) => window.seek(t), t);
        await page.screenshot({ path: `${out}/${String(f * 3 + k).padStart(5, "0")}.jpg`, type: "jpeg", quality: 95 });
      }
      if (f % 120 === 0) console.log(`frame ${f}/${total}`);
    }
  }));
  await browser.close();
})();
