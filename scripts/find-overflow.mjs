import puppeteer from 'puppeteer-core';
const browser = await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:'new', args:['--disable-gpu']});
for (const width of [320,375,390]) {
 const page = await browser.newPage();
 await page.setViewport({width, height: 900});
 await page.goto('http://127.0.0.1:4173/', {waitUntil:'networkidle0'});
 const offenders = await page.evaluate(() => {
   const vw = window.innerWidth;
   return [...document.querySelectorAll('*')].map(el => {
     const r = el.getBoundingClientRect();
     return {tag: el.tagName, cls: el.className, id: el.id, text: (el.textContent||'').trim().slice(0,60), left:r.left, right:r.right, width:r.width};
   }).filter(x => x.right > vw + 1 || x.left < -1).sort((a,b)=>b.right-a.right).slice(0,20);
 });
 console.log('\nWIDTH', width, 'offenders');
 console.log(JSON.stringify(offenders, null, 2));
 await page.close();
}
await browser.close();
