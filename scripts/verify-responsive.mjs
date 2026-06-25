import puppeteer from 'puppeteer-core';
import { mkdir } from 'node:fs/promises';

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SITE_URL = process.env.SITE_URL || 'http://127.0.0.1:4173/';

const viewports = [
  { name: 'mobile-320', width: 320, height: 900 },
  { name: 'mobile-375', width: 375, height: 900 },
  { name: 'mobile-390', width: 390, height: 1000 },
  { name: 'mobile-430', width: 430, height: 1000 },
  { name: 'tablet-768', width: 768, height: 1100 },
  { name: 'desktop-1440', width: 1440, height: 1000 },
];

await mkdir('assets/responsive', { recursive: true });

const browser = await puppeteer.launch({
  executablePath: CHROME_PATH,
  headless: 'new',
  args: ['--disable-gpu', '--hide-scrollbars'],
});

let failed = false;
const results = [];

for (const vp of viewports) {
  const page = await browser.newPage();
  await page.setViewport({ width: vp.width, height: vp.height, deviceScaleFactor: 1 });
  await page.goto(SITE_URL, { waitUntil: 'networkidle0' });
  const metrics = await page.evaluate(() => {
    const doc = document.documentElement;
    const body = document.body;
    const maxScrollWidth = Math.max(doc.scrollWidth, body.scrollWidth);
    const maxClientWidth = Math.max(doc.clientWidth, body.clientWidth, window.innerWidth);
    const cta = document.querySelector('.cta-row');
    const h1 = document.querySelector('h1');
    const nav = document.querySelector('.nav');
    const portrait = document.querySelector('.portrait-box');
    const ctaRect = cta?.getBoundingClientRect();
    const h1Rect = h1?.getBoundingClientRect();
    const portraitRect = portrait?.getBoundingClientRect();
    return {
      innerWidth: window.innerWidth,
      scrollWidth: maxScrollWidth,
      clientWidth: maxClientWidth,
      overflowX: maxScrollWidth > window.innerWidth + 1,
      ctaVisibleInitial: !!ctaRect && ctaRect.top < window.innerHeight && ctaRect.bottom > 0,
      h1Width: h1Rect?.width ?? 0,
      h1FontSize: getComputedStyle(h1).fontSize,
      navHeight: nav?.getBoundingClientRect().height ?? 0,
      portraitWidth: portraitRect?.width ?? 0,
      bodyHeight: body.scrollHeight,
    };
  });
  await page.screenshot({ path: `assets/responsive/${vp.name}.png`, fullPage: true });
  const ok = !metrics.overflowX && metrics.ctaVisibleInitial;
  if (!ok) failed = true;
  results.push({ ...vp, ...metrics, ok });
  await page.close();
}

await browser.close();
console.log(JSON.stringify(results, null, 2));
if (failed) process.exit(1);
