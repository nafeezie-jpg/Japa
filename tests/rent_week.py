# Plays Rent Week on many days in a row in each city, checking that the life carries on and nothing breaks.
# Run: python3 tests/rent_week.py   (add "shots" to save screenshots in tests/shots/)
import asyncio, os, sys, random, datetime
from playwright.async_api import async_playwright
PAGE = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'week', 'index.html'))
SHOTS = 'shots' in sys.argv
issues = []
async def play_week(pg, tag, shoot=False):
  taps = 0
  for _ in range(700):
    if await pg.locator('#over:not([hidden]) #share').count(): return taps
    if await pg.locator('#drive #dauto').count(): await pg.click('#dauto'); await pg.wait_for_timeout(100); continue
    if await pg.locator('#mg #mgauto').count(): await pg.click('#mgauto'); await pg.wait_for_timeout(100); continue
    if await pg.locator('#over:not([hidden]) #begin').count(): await pg.click('#begin'); await pg.wait_for_timeout(1000); continue
    body = await pg.locator('body').inner_text()
    if 'Heading to' in body: await pg.wait_for_timeout(400); continue
    if await pg.locator('#snagok').count(): await pg.click('#snagok'); continue
    for bad in ('undefined','NaN','[object','${'):
      if bad in body: issues.append(f'{tag}: "{bad}" on screen'); return taps
    if await pg.locator('#next:not([disabled])').count():
      await pg.click('#next:not([disabled])'); await pg.wait_for_timeout(950 if 'Friday' not in body else 50); continue
    if await pg.locator('#phone:not([hidden])').count() and random.random() < .45: await pg.click('#phone'); continue
    if await pg.locator('.daycard').count() or await pg.locator('#next').count(): await pg.wait_for_timeout(300); continue
    acts = pg.locator('.act:not([disabled])'); n = await acts.count()
    if n > 1:
      if shoot and taps == 3: await pg.screenshot(path='tests/shots/week-place.png')
      await acts.nth(random.randrange(n - 1)).click(); taps += 1; continue
    if n == 1 and 'Go somewhere' not in (await acts.nth(0).inner_text()): await acts.nth(0).click(); continue
    pins = pg.locator('.pin:not(.shut)'); await pins.nth(random.randrange(await pins.count())).click()
  issues.append(f'{tag}: week never ended'); return taps
async def run():
  async with async_playwright() as p:
    b = await p.chromium.launch()
    for ci, city in enumerate(['houston','london','toronto','lagos','abuja','ph','ibadan','kano','enugu','ilorin']):
      ctx = await b.new_context(viewport={'width':390,'height':844}); pg = await ctx.new_page()
      errs = []; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
      await pg.route('**/gc.zgo.at/**', lambda r: r.abort()); await pg.route('**/fonts.g*/**', lambda r: r.abort())
      day0 = datetime.datetime(2026, 11, 20, 10, 0)
      await pg.clock.install(time=day0); await pg.goto(PAGE)
      await pg.click('#wgo'); NGS = {'lagos':'Lagos','abuja':'FCT','ph':'Rivers','ibadan':'Oyo','kano':'Kano','enugu':'Enugu','ilorin':'Kwara'}
      await pg.click('.city[data-c="ng"]' if city in NGS else f'.city[data-c="{city}"]')
      if city in NGS: await pg.select_option('#placesel', NGS[city])
      await pg.click('#placego'); await pg.click('[data-me="' + 'whm'[ci % 3] + '"]'); await pg.click('[data-fam="' + ['single','married','kids','solo'][ci % 4] + '"]'); await pg.click('#mego'); await pg.wait_for_timeout(300)
      if SHOTS and ci == 0: await pg.screenshot(path='tests/shots/week-intro.png')
      for d in range(7 if ci < 4 else 3):
        if d: await pg.clock.set_fixed_time(day0 + datetime.timedelta(days=d)); await pg.goto(PAGE); await pg.wait_for_timeout(300)
        before = await pg.evaluate('JSON.parse(localStorage.getItem("nyhl-week"))')
        if before['week'] != d + 1 and not before.get('lives', 1) > 1: issues.append(f'{city} day {d}: expected week {d+1}, got {before["week"]}')
        taps = await play_week(pg, f'{city} day {d}', shoot=SHOTS and ci == 0 and d == 0)
        if SHOTS and ci == 0 and d in (0, 5): await pg.wait_for_timeout(600); await pg.screenshot(path=f'tests/shots/week-end{d}.png')
        st = await pg.evaluate('JSON.parse(localStorage.getItem("nyhl-week"))')
        h = st['hist'][-1]
        print(city, 'week', h['w'], 'PASS' if h['pass'] else 'fail', 'left', h['left'], 'stars', h['stars'], 'taps', taps, '| unlocks', [k for k in ('promo','office','stall') if st[k]] + (['car'] if st['car']=='fixed' else []), 'warn', st['warnings'])
        if taps < 8: issues.append(f'{city} day {d}: only {taps} choices')
        await pg.goto(PAGE); await pg.wait_for_timeout(300)
        if not await pg.locator('#over:not([hidden])').filter(has_text='YOU PLAYED TODAY').count(): issues.append(f'{city} day {d}: replay not blocked')
        if SHOTS and ci == 0 and d == 0: await pg.screenshot(path='tests/shots/week-done.png')
      if errs: issues.append(f'{city}: page errors {errs[:3]}')
      await ctx.close()
    await b.close()
asyncio.run(run())
print('ISSUES:', issues or 'none')
