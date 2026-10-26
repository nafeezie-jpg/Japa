# Plays 24 full random games with the leaderboard mocked. Run: python3 tests/full_games.py
import asyncio, json, random, os
PAGE = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
from playwright.async_api import async_playwright
posts=[]; issues=[]
async def run():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    async def h(r,*a):
      if r.request.method=='POST':
        posts.append(json.loads(r.request.post_data)); return await r.fulfill(status=201, content_type='application/json', body='[{"created_at":"2026-10-24T22:00:00Z"}]')
      await r.fulfill(status=200, content_type='application/json', body=json.dumps([dict(x,created_at="2026-10-24T22:00:00Z", spotted=x.get('spotted',0)) for x in posts]))
    games=0
    for g in range(24):
      route=['us','uk','ca','eu'][g%4]
      ctx=await b.new_context(viewport={'width':390,'height':900}, color_scheme=['light','dark'][g%2]); pg=await ctx.new_page()
      errs=[]; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
      await pg.route('**/rest/v1/**', h); await pg.route('**/gc.zgo.at/**', lambda r: r.abort()); await pg.route('**/fonts.g*/**', lambda r: r.abort())
      await pg.goto(PAGE)
      if g%4==0: await pg.fill('#pname','Tester'+str(g)); await pg.press('#pname','Tab')
      await pg.select_option('#origin', index=g % 37)
      if g%5==0:
        await pg.click('#dailygo')
      else:
       await pg.click('#moredet > summary')
       await pg.click(f'.quick-btn[data-q="{route}"]')
       opts = await pg.eval_on_selector('#qpath','e=>[...e.options].map(o=>o.value)')
       await pg.select_option('#qpath', opts[g % len(opts)])
       await pg.select_option('#qfund', ['','savings','sold','borrowed','kept'][g%5])
       await pg.select_option('#qplace', index=(g*7) % (await pg.locator('#qplace option').count()))
       await pg.click('#qgo')
      backed=False; steps=0
      for _ in range(120):
        if await pg.locator('#lbbox').count(): break
        if await pg.locator('.art.vn').count() and random.random()<.3: await pg.click('.art.vn')
        ch=pg.locator('.choice')
        if await ch.count(): await ch.nth(random.randrange(await ch.count())).click(); steps+=1
        elif not backed and await pg.locator('#back').count() and steps==3: await pg.click('#back'); backed=True
        elif await pg.locator('#next').count(): await pg.click('#next')
      else: issues.append(f'game {g} never ended')
      await pg.wait_for_timeout(900)
      box = await pg.locator('#lbbox').inner_text()
      if 'this week, of' not in box: issues.append(f'game {g} box: {box[:80]}')
      if not await pg.locator('#cardimg:not([hidden])').count(): issues.append(f'game {g} no card')
      wa = await pg.get_attribute('#s-wa','href')
      if '%23' not in wa: issues.append(f'game {g} no rank in share')
      if g==0:
        await pg.click('#pada'); await pg.click('#move'); await pg.locator('#movebox .route-btn').first.click(); await pg.click('#go2')
        await pg.wait_for_selector('.choice'); landing2 = await pg.evaluate('S.landing')
        if landing2!=2: issues.append('japa again failed')
      if g==1:
        await pg.click('#again'); await pg.wait_for_selector('.quick-btn')
        await pg.click('.glossbtn' if await pg.locator('.glossbtn').count() else 'details.how >> nth=1')
        await pg.evaluate('openJournal()'); await pg.wait_for_selector('#journalover .j-row')
        await pg.evaluate('openBoard()'); await pg.wait_for_selector('.lb-row')
        for t in ['score','spotted','refused','sent','fooled']: await pg.click(f'.lb-tab[data-t="{t}"]')
      if errs: issues.append(f'game {g} js errors: {errs}')
      games+=1; await ctx.close()
    # winners page
    ctx=await b.new_context(viewport={'width':390,'height':900}); pg=await ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.route('**/rest/v1/**', h); await pg.route('**/gc.zgo.at/**', lambda r: r.abort())
    await pg.goto(PAGE+'?winners=this'); await pg.wait_for_selector('#wimg', timeout=8000)
    if errs: issues.append(f'winners errors {errs}')
    print('games played', games, '| posts', len(posts), '| scores', sorted(p['score'] for p in posts), '| spotted', [p['spotted'] for p in posts])
    print('ISSUES:', issues or 'none'); await b.close()
asyncio.run(run())
