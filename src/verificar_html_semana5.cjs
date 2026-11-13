// QA local, somente páginas geradas pelo projeto. Requer Playwright no ambiente.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
(async () => {
  const root = path.resolve(__dirname, '..');
  const dir = path.join(root, 'dados', 'execucoes_engenharia', 'qa_visual_semana5');
  fs.mkdirSync(dir, {recursive: true});
  const browser = await chromium.launch({channel: 'msedge', headless: true});
  const page = await browser.newPage({viewport: {width: 1366, height: 900}});
  const results = [];
  for (const file of ['relatorio_executivo.html', 'mini_deck.html']) {
    await page.goto(pathToFileURL(path.join(root, 'saidas', 'semana5_consolidada', file)).href);
    await page.evaluate(() => Promise.all([...document.images].map(im => im.decode())));
    const sections = page.locator('section');
    const count = await sections.count();
    const overflow = await page.evaluate(() => [...document.querySelectorAll('section')].some(s => s.scrollWidth > s.clientWidth));
    for (let i=0; i<count; i++) {
      await sections.nth(i).screenshot({path: path.join(dir, file.replace('.html', '') + '_' + (i+1) + '.png')});
    }
    if (process.argv.includes('--pdf')) {
      const output = path.join(root,'saidas','semana5_consolidada',file.replace('.html','.pdf'));
      const options = file.startsWith('mini_deck')
        ? {width:'13.333in',height:'7.5in',scale:0.9,margin:{top:'0.15in',bottom:'0.15in',left:'0.2in',right:'0.2in'}}
        : {format:'A4',scale:0.95,margin:{top:'12mm',bottom:'12mm',left:'10mm',right:'10mm'}};
      await page.pdf({path:output,printBackground:true,...options});
    }
    const sha256 = crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'saidas','semana5_consolidada',file))).digest('hex');
    results.push({file, sections:count, horizontalOverflow:overflow, sha256});
    if (overflow) throw new Error('Tabela extrapola seção: '+file);
  }
  await browser.close();
  fs.writeFileSync(path.join(root,'saidas','semana5_consolidada','tabelas','qa_visual.json'),JSON.stringify(results,null,2));
  console.log(JSON.stringify(results));
})().catch(e => {console.error(e);process.exit(1);});
