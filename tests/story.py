# Lives whole stories day by day: a brand new player from setup to Year 5, and an existing player with 15 landings.
# Checks: setup, stage labels, meters carry over, no scene repeats inside a life, goal scenes appear, the story ends at landing 19.
# Run: python3 tests/story.py  (add "shots" to save screenshots in tests/shots/)
import asyncio, os, sys, random, datetime
PAGE = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
SHOTS = 'shots' in sys.argv
from playwright.async_api import async_playwright
issues = []
LABELS = [None,'Month 1','Month 2','Month 3','Month 4','Month 5','Month 6','Month 8','Month 10','Year 1','Year 1 and 3 months','Year 1 and a half','Year 1 and 9 months','Year 2','Year 2 and a half','Year 3','Year 3 and a half','Year 4','Year 4 and a half','Year 5']

async def play_through(pg, tag):
  choices = 0
  for _ in range(120):
    if await pg.locator('#lbbox').count(): break
    body = await pg.locator('#app').inner_text()
    for bad in ('undefined','NaN','[object','${'):
      if bad in body: issues.append(f'{tag}: "{bad}" on screen: {body[:160]!r}')
    c = pg.locator('.choice')
    if await c.count(): await c.nth(random.randrange(await c.count())).click(); choices += 1
    elif await pg.locator('#next').count(): await pg.click('#next')
  else: issues.append(f'{tag}: never ended')
  return choices

async def setup(pg, rk, deps, goal):
  await pg.click(f'[data-rk="{rk}"]'); await pg.click(f'[data-deps="{deps}"]'); await pg.click(f'[data-goal="{goal}"]'); await pg.click('#sugo')

async def run():
  async with async_playwright() as p:
    b = await p.chromium.launch()
    for ci, (rk, deps, goal, old) in enumerate([('uk','parents','house',False), ('ca','kids','family',True), ('us','none','savings',False), ('eu','siblings','papers',True)]):
      ctx = await b.new_context(viewport={'width':390,'height':900}, color_scheme=['light','dark'][ci%2]); pg = await ctx.new_page()
      errs = []; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
      async def board(r):
        if r.request.method == 'POST': return await r.fulfill(status=201, content_type='application/json', body='[{"created_at":"2026-11-13T12:00:00Z"}]')
        await r.fulfill(status=200, content_type='application/json', body='[]')
      await pg.route('**/rest/v1/**', board); await pg.route('**/gc.zgo.at/**', lambda r: r.abort()); await pg.route('**/fonts.g*/**', lambda r: r.abort())
      day0 = datetime.datetime(2026, 11, 13, 9, 0)
      await pg.clock.install(time=day0); await pg.goto(PAGE)
      await pg.evaluate('() => { localStorage.setItem("nyhl-name","Tester"); localStorage.setItem("nyhl-origin","Lagos"); }')
      tag0 = f'{rk}/{goal}{" old" if old else ""}'
      if old:
        hist = [dict(t=int((day0 - datetime.timedelta(days=k)).timestamp()*1000), r='us', trip='Lagos → Maryland', path='work', v='Settling In', cash=2100, cur='$', rent=1.0, name='T', peace=63, home=57, future=44, daily=True) for k in range(15, 0, -1)]
        await pg.evaluate('h => localStorage.setItem("nyhl-history", JSON.stringify(h))', hist)
        await pg.goto(PAGE)
        hero = await pg.locator('.hero').inner_text()
        if 'Make it my story' not in hero: issues.append(f'{tag0}: hero does not offer Make it my story: {hero[:120]!r}')
        await pg.click('#dailygo')
        st = await pg.locator('#app').inner_text()
        if 'Month 10' not in st: issues.append(f'{tag0}: setup does not say Month 10 (15 landings = month 8 lived): {st[:200]!r}')
        if SHOTS and ci==1: await pg.screenshot(path='tests/shots/story-setup-old.png', full_page=True)
        await setup(pg, rk, deps, goal)
        n0 = 8
      else:
        hero = await pg.locator('.hero').inner_text()
        if 'Start my story' not in hero: issues.append(f'{tag0}: new hero wrong: {hero[:120]!r}')
        await pg.click('#dailygo')
        await pg.click('#sugo')
        if 'Pick who' not in await pg.locator('#sumsg').inner_text(): issues.append(f'{tag0}: setup let me go without picks')
        if SHOTS and ci==0: await pg.screenshot(path='tests/shots/story-setup-new.png', full_page=True)
        await setup(pg, rk, deps, goal)
        txt = await pg.locator('#app').inner_text()
        if 'chapter 1 of your story' not in txt.lower(): issues.append(f'{tag0}: first month note missing')
        await play_through(pg, tag0+' month 1')
        saved = await pg.evaluate('JSON.parse(localStorage.getItem("nyhl-daily")||"null")')
        if not saved or saved.get('n') != 1 or saved['S'].get('me',{}).get('goal') != goal: issues.append(f'{tag0}: month 1 not saved as a story: {saved and saved.get("n")}')
        n0 = 2
      seen, goal_hits, prev = set(), 0, None
      for d, n in enumerate(range(n0, 20)):
        await pg.clock.set_fixed_time(day0 + datetime.timedelta(days=d+1))
        await pg.goto(PAGE)
        hero = await pg.locator('.hero').inner_text()
        if LABELS[n] not in hero: issues.append(f'{tag0} n{n}: hero should say {LABELS[n]}: {hero[:100]!r}')
        await pg.click('#dailygo')
        start = await pg.evaluate('({peace:S.peace, home:S.home, future:S.future, n:S.cont && S.cont.n, label:S.cont && S.cont.label})')
        if start['n'] != n: issues.append(f'{tag0}: expected landing {n}, got {start["n"]}')
        if prev and any(abs(start[k]-prev[k])>0.5 for k in ('peace','home','future')): issues.append(f'{tag0} n{n}: meters did not carry over')
        picks = await pg.evaluate('S.cPick')
        rep = [k for k in picks if k in seen]
        if rep: issues.append(f'{tag0} n{n}: repeated {len(rep)} scene(s): {rep[0][:50]!r}')
        seen.update(picks)
        goal_hits += await pg.evaluate('SCENES.filter(s => s.goalScene).length')
        if SHOTS and ci==0 and n in (2, 19):
          await pg.wait_for_timeout(600); await pg.screenshot(path=f'tests/shots/story-n{n}.png', full_page=True)
        ch = await play_through(pg, f'{tag0} n{n}')
        want = 4
        if ch < want: issues.append(f'{tag0} n{n}: only {ch} choices')
        endtxt = await pg.locator('#app').inner_text()
        if n < 19 and f'Chapter {n} of 19 done' not in endtxt: issues.append(f'{tag0} n{n}: no story card on result')
        if n == 19 and 'the whole story' not in endtxt.lower(): issues.append(f'{tag0}: no life summary at the end')
        if SHOTS and ci==0 and n in (2, 19):
          await pg.wait_for_timeout(800); await pg.screenshot(path=f'tests/shots/story-end-n{n}.png', full_page=True)
        prev = await pg.evaluate('({peace:S.peace, home:S.home, future:S.future})')
      if goal_hits < 4: issues.append(f'{tag0}: only {goal_hits} goal scenes in a whole life')
      await pg.clock.set_fixed_time(day0 + datetime.timedelta(days=40)); await pg.goto(PAGE)
      hero = await pg.locator('.hero').inner_text()
      if 'Start a new life' not in hero and 'Start my story' not in hero: issues.append(f'{tag0}: after the end, hero does not offer a new life: {hero[:100]!r}')
      print(f'{tag0}: {len(seen)} different scenes, {goal_hits} goal scenes')
      for e in errs: issues.append(f'{tag0}: page error {e}')
      await ctx.close()
    await b.close()
  print('ISSUES:', 'none' if not issues else '')
  for i in issues[:40]: print(' -', i)
asyncio.run(run())
