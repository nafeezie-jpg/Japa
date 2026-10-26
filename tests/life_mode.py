# Plays My Life Abroad from the locked card to the end of the last written chapter, many times.
# Run: python3 tests/life_mode.py  (add "shots" to save 390px screenshots in tests/shots/)
import asyncio, json, random, os, sys, time
PAGE = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
SHOTS = 'shots' in sys.argv
from playwright.async_api import async_playwright
issues = []
DAY = 86400000
async def run():
  async with async_playwright() as p:
    b = await p.chromium.launch()
    for g in range(12):
      route = ['us','uk','ca','eu'][g % 4]
      ctx = await b.new_context(viewport={'width':390,'height':900}, color_scheme=['light','dark'][g % 2]); pg = await ctx.new_page()
      errs = []; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
      posts = []
      async def board(r, posts=posts):
        if r.request.method == 'POST': posts.append(1)
        await r.fulfill(status=200, content_type='application/json', body='[]')
      await pg.route('**/rest/v1/**', board); await pg.route('**/gc.zgo.at/**', lambda r: r.abort()); await pg.route('**/fonts.g*/**', lambda r: r.abort())
      await pg.goto(PAGE)
      await pg.select_option('#origin', index=(g*5) % 37)
      card = await pg.locator('#lifecard').inner_text()
      if 'Unlocks when you become a JJC' not in card: issues.append(f'life {g}: card not locked for a new player')
      if g == 0 and SHOTS: await pg.locator('#lifecard').screenshot(path='tests/shots/life-locked.png')
      now = int(time.time()*1000)
      hist = [dict(t=now - k*DAY, r='us', trip='Lagos → Baltimore', path='work', v='Settling In', cash=900, cur='$', rent=1.2, name='', peace=60, home=55, future=40, daily=True) for k in (1, 2)]
      await pg.evaluate('h => localStorage.setItem("nyhl-history", JSON.stringify(h))', hist)
      await pg.reload()
      await pg.click(f'#lifecard .lflags button >> nth={["us","uk","ca","eu"].index(route)}')
      await pg.select_option('#lplace', index=(g*7) % await pg.locator('#lplace option').count())
      await pg.select_option('#lpath', index=g % await pg.locator('#lpath option').count())
      await pg.select_option('#lfund', index=g % 5)
      if g == 0 and SHOTS: await pg.locator('#lifecard').screenshot(path='tests/shots/life-setup.png')
      await pg.click('#lifego')
      for ch in range(0, 3):
        steps = 0; backed = False
        for _ in range(140):
          if await pg.locator('#lhome').count(): break
          body = await pg.locator('#app').inner_text()
          for bad in ('undefined', 'NaN', '[object', '${'):
            if bad in body: issues.append(f'life {g} ch{ch}: "{bad}" on screen: {body[:120]!r}')
          if g == 0 and SHOTS and ch == 1 and steps == 3: await pg.wait_for_timeout(700); await pg.screenshot(path='tests/shots/life-ch1-scene.png', full_page=True)
          c = pg.locator('.choice')
          if await c.count(): await c.nth(random.randrange(await c.count())).click(); steps += 1
          elif ch and not backed and steps == 2 and await pg.locator('#back').count(): await pg.click('#back'); backed = True; steps -= 1
          elif await pg.locator('#next').count(): await pg.click('#next')
        else: issues.append(f'life {g} ch{ch}: never ended')
        if ch and steps not in (9, 10): issues.append(f'life {g} ch{ch}: {steps} choices, expected 9 or 10')
        if await pg.locator('#lbbox').count(): issues.append(f'life {g} ch{ch}: leaderboard box on a life screen')
        lf = await pg.evaluate('loadLife()')
        if not lf or lf['ch'] != ch: issues.append(f'life {g}: saved chapter {lf and lf["ch"]}, expected {ch}')
        if g == 0 and SHOTS: await pg.wait_for_timeout(700); await pg.screenshot(path=f'tests/shots/life-end-ch{ch}.png', full_page=True)
        await pg.click('#lhome')
        card = await pg.locator('#lifecard').inner_text()
        if ch < 2 and 'unlocks in' not in card: issues.append(f'life {g} ch{ch}: home card does not show the countdown: {card[:100]!r}')
        if ch == 2 and 'being written' not in card: issues.append(f'life {g}: chapter 3 not shown as coming soon')
        if g == 0 and SHOTS and ch == 0: await pg.locator('#lifecard').screenshot(path='tests/shots/life-waiting.png')
        if ch < 2:   # pretend a day has passed
          await pg.evaluate('() => { const l = loadLife(); l.doneOn = "2000-01-01"; saveLife(l); }')
          await pg.reload(); await pg.click('#lifeplay')
      if posts: issues.append(f'life {g}: posted {len(posts)} times to the leaderboard')
      # the life travels in the move code
      code = await pg.evaluate('progressCode()')
      ctx2 = await b.new_context(); pg2 = await ctx2.new_page(); await pg2.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
      await pg2.goto(PAGE); await pg2.evaluate('c => importProgress(c)', code)
      moved = await pg2.evaluate('loadLife()')
      if not moved or moved['ch'] != 2: issues.append(f'life {g}: move code lost the life')
      await ctx2.close()
      if errs: issues.append(f'life {g} js errors: {errs}')
      await ctx.close()
    print('ISSUES:', issues or 'none'); await b.close()
asyncio.run(run())
