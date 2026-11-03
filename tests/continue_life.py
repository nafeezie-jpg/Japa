# Plays Today's Landing on many days in a row and checks that each day continues the same life.
# Run: python3 tests/continue_life.py  (add "shots" to save screenshots in tests/shots/)
import asyncio, json, os, sys, random, datetime
PAGE = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
SHOTS = 'shots' in sys.argv
from playwright.async_api import async_playwright
issues = []
CASES = [('eu','Netherlands','Lagos → Amsterdam','work'), ('us','Maryland','Lagos → Maryland','study'), ('uk','Manchester','Lagos → Manchester','care'), ('ca','Ontario','Lagos → Toronto','work')]
async def run():
  async with async_playwright() as p:
    b = await p.chromium.launch()
    for ci, (rk, place, trip, path) in enumerate(CASES):
      ctx = await b.new_context(viewport={'width':390,'height':900}, color_scheme=['light','dark'][ci%2]); pg = await ctx.new_page()
      errs = []; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
      async def board(r):
        if r.request.method == 'POST': return await r.fulfill(status=201, content_type='application/json', body='[{"created_at":"2026-11-03T12:00:00Z"}]')
        await r.fulfill(status=200, content_type='application/json', body='[]')
      await pg.route('**/rest/v1/**', board); await pg.route('**/gc.zgo.at/**', lambda r: r.abort()); await pg.route('**/fonts.g*/**', lambda r: r.abort())
      day0 = datetime.datetime(2026, 11, 3, 9, 0)
      await pg.clock.install(time=day0)
      await pg.goto(PAGE)
      town = trip.split(' → ')[1]
      hist = [dict(t=int((day0 - datetime.timedelta(days=k)).timestamp()*1000), r=rk, trip=trip, path=path, v='Settling In', cash=1500, cur='$', rent=1.0, name='T', peace=62, home=58, future=41, daily=True) for k in range(7, 0, -1)]
      await pg.evaluate('h => { localStorage.setItem("nyhl-history", JSON.stringify(h)); localStorage.setItem("nyhl-name","Tester"); localStorage.setItem("nyhl-origin","Lagos"); }', hist)
      prev = None
      for d in range(9):
        await pg.clock.set_fixed_time(day0 + datetime.timedelta(days=d))
        await pg.goto(PAGE)
        hero = await pg.locator('.hero').inner_text()
        n = 8 + d; m = 1 + -(-(n-1)//2)
        if f'Month {m} of your life' not in hero: issues.append(f'{rk} day {d}: hero says {hero[:90]!r}')
        if town not in hero: issues.append(f'{rk} day {d}: hero does not name {town}')
        await pg.click('#dailygo')
        txt = await pg.locator('#app').inner_text()
        if 'Your life carries on' not in txt: issues.append(f'{rk} day {d}: no welcome card')
        if f'MONTH {m} ' not in txt: issues.append(f'{rk} day {d}: header not month {m}')
        start = await pg.evaluate('({cash:S.cash, peace:S.peace, home:S.home, future:S.future, town:L.town})')
        if prev and any(abs(start[k]-prev[k])>0.5 for k in ('peace','home','future')): issues.append(f'{rk} day {d}: meters did not carry over {prev} -> {start}')
        if start['town'] != town: issues.append(f'{rk} day {d}: town changed to {start["town"]}')
        if d==0 and SHOTS and ci==0: await pg.screenshot(path='tests/shots/cont-welcome.png', full_page=True)
        choices = 0
        for _ in range(60):
          if await pg.locator('#lbbox').count(): break
          body = await pg.locator('#app').inner_text()
          for bad in ('undefined','NaN','[object','${'):
            if bad in body: issues.append(f'{rk} day {d}: "{bad}" on screen: {body[:140]!r}')
          c = pg.locator('.choice')
          if await c.count():
            if d==0 and choices==1 and SHOTS and ci==0: await pg.wait_for_timeout(1200); await pg.screenshot(path='tests/shots/cont-scene.png', full_page=True)
            await c.nth(random.randrange(await c.count())).click(); choices += 1
          elif await pg.locator('#next').count(): await pg.click('#next')
        else: issues.append(f'{rk} day {d}: never ended')
        if choices < 6 or choices > 8: issues.append(f'{rk} day {d}: {choices} choices')
        endtxt = await pg.locator('#app').inner_text()
        if 'two weeks' not in endtxt.lower(): issues.append(f'{rk} day {d}: result screen does not say two weeks')
        if d==0 and SHOTS and ci==0: await pg.wait_for_timeout(800); await pg.screenshot(path='tests/shots/cont-end.png', full_page=True)
        prev = await pg.evaluate('({cash:S.cash, peace:S.peace, home:S.home, future:S.future})')
        saved = await pg.evaluate('JSON.parse(localStorage.getItem("nyhl-daily")||"null")')
        if not saved or saved['S']['peace'] != prev['peace']: issues.append(f'{rk} day {d}: life not saved')
        picks = await pg.evaluate('S.cPick')
        if len(set(picks)) != len(picks): issues.append(f'{rk} day {d}: same scene twice in one day')
        seenall = globals().setdefault('SEEN', {}).setdefault(rk, []); rep = [k for k in picks if k in seenall]; seenall.extend(picks)
        if d < 5 and rep: issues.append(f'{rk} day {d}: repeats {len(rep)} scene(s) already lived')
        print(rk, 'day', d, 'month', m, 'choices', choices, 'score', await pg.evaluate('nowScore()'), 'cash', round(prev['cash']), '| picks', [k.split('|')[2][:28] for k in picks][:7])
      if errs: issues.append(f'{rk}: page errors {errs[:3]}')
      await ctx.close()
    await b.close()
asyncio.run(run())
print('ISSUES:', issues or 'none')
