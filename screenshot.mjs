/**
 * screenshot.mjs — take a full-page screenshot of a localhost URL
 * Usage: node screenshot.mjs <url> [label]
 * Saves to: ./temporary screenshots/screenshot-N[-label].png
 */

import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const url   = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';

// Ensure output directory exists
const outDir = path.join(__dirname, 'temporary screenshots');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// Auto-increment filename
function nextFilename() {
  let n = 1;
  while (true) {
    const name = label
      ? `screenshot-${n}-${label}.png`
      : `screenshot-${n}.png`;
    if (!fs.existsSync(path.join(outDir, name))) return name;
    n++;
  }
}

const filename = nextFilename();
const outPath  = path.join(outDir, filename);

// Puppeteer — try installed locations
let browser;
try {
  browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
} catch (e) {
  console.error('Failed to launch Puppeteer:', e.message);
  process.exit(1);
}

const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

// Scroll through the page to trigger IntersectionObserver callbacks
await page.evaluate(async () => {
  const totalHeight = document.body.scrollHeight;
  const step = 300;
  for (let y = 0; y < totalHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 60));
  }
  window.scrollTo(0, 0);
});

// Wait for animations to complete
await new Promise(r => setTimeout(r, 1200));

await page.screenshot({ path: outPath, fullPage: true });
await browser.close();

console.log(`Screenshot saved: temporary screenshots/${filename}`);
