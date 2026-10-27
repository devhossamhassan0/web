// Render single frames for review: node promo/tools/probe.cjs out_dir t1 t2 ...
const { chromium } = require("playwright");
const { mkdirSync } = require("node:fs");
const { resolve } = require("node:path");

const root = resolve(__dirname, "..");
const [out, ...times] = process.argv.slice(2);

(async () => {
  mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto(`file://${root}/index.html`);
  for (const t of times.map(Number)) {
    await page.evaluate((t) => window.seek(t), t);
    await page.screenshot({ path: `${out}/t${t.toFixed(2).padStart(5, "0")}.png` });
  }
  await browser.close();
})();
