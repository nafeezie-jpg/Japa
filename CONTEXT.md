# Now You Have Landed: context for new sessions

Read this, then read index.html, before changing anything.

## The game
- Browser game about a Nigerian's first 30 days in the US, UK, Canada, or Europe. Live at nowyouhavelanded.com.
- Built by Nafeezie (Nafeesat). The repo is nafeezie-jpg/Japa and is served by GitHub Pages from main. The domain is on Namecheap.
- Everything lives in one file, index.html, written in vanilla JS. Other files: sw.js (push notifications), manifest.json and icons (home screen app), supabase/ (SQL and the daily-push edge function).
- Analytics: GoatCounter site "nowyouhavelanded". Player stories come in through Tally form q5480d.

## Nafeezie's rules
- Writing: no em dashes, no "not X but Y", minimal colons and semicolons, warm and plain. Keep replies short.
- Keep the game witty. People laugh while playing.
- More visuals than words. People hate to read.
- Everything should feel random. No fixed endings.

## How the code works
- **State machine.** render() runs the phases intro, scene, result, and end.
- **Globals.** R is the route, L is the place, S is the game state, and idx is the current scene.
- **Scene shape.** `{day, from, sub, text, choices:[{l, fx:{cash,peace,home,future}, set, r}], when, ask, core, credit, label}`.
  - Version pools are chosen with `pickV(key, n)`. It is seeded by the date for Today's Landing, by duo for two-player games, and otherwise by freshPick, which avoids versions this phone saw recently.
- **Game length.** Each game has 15 questions at most (MAX_Q, isCore, planExtras).
- **Day 30.** `finale()` picks one of 5 endings.
- **Meters.**
  - Healthy marks are MARKS = {peace:80, home:65, future:60}, and HOME_CAP = 85. Cash is healthy at SAFE_RENT, 5 months' rent. Raised on 27 Oct 2026 because scores bunched in the 70s.
  - `scoreOf` gives 70 when all four meters are healthy and 100 when all are excellent. Below a healthy mark, points fall away on a curve (power 1.6). The gauge line sits at 70. Ghost Mode needs home under 35, or 5+ refusals with home under 45.
- **Verdicts and badges.**
  - VERDICTS (10) give one verdict per game.
  - BADGES (7) can be earned several per game.
  - Both are stored in localStorage under nyhl-verdicts. Icons are in VICON.
- **Today's Landing.**
  - One shared game a day: dailyPlan(ds), with DAILY_EPOCH 2026-10-24.
  - It shows the percentile against today's players.
  - The weekly crown (Best Landing) counts daily games only.
- **Japa experience.**
  - Each Today's Landing counts as one "landing lived" (abroadMonths() counts daily days).
  - The titles in ABROAD_BADGES run Just Landed, JJC (2), Still Converting to Naira (7), Knows the Bus Routes (13), Proper Abroad Person (26), Sends Advice Home (52), Weather Complainer (78), Japa Veteran (130).
  - Practice games ("Practice any route", formerly "Play more") don't count.
- **Result screen, top to bottom.**
  - Verdict card
  - "What it cost you" chips (costParts)
  - Tomorrow card (tomorrowHTML: countdown, streak, landings, title, reminders)
  - Score gauge
  - Meter tiles
  - Lesson
  - Leaderboard box
  - Share card and share links
  - Play again buttons
  - Collection
  - Road to making it
- **Home screen.** Your details, then the Today's Landing hero (or the tomorrow card once played), progress tiles, the My Life Abroad card, "What is this game?" (openAbout, also /?about) and "How it works" (openHow, also /?how) side by side, "Practice any route" (id moredet), and "More" (story links, Naija words, move progress).
- **Move my progress.** openMove copies a NYHL1 code between Safari and the home screen app, which keep separate storage on iPhone.
- **Supabase.**
  - Project mydzixaknqldrcfakirn. The publishable key is in index.html.
  - Table `landings` allows insert and select only, with a guard trigger. The boards are Best landing, Most streetwise, Hardest heart, Softest heart, and Most trusting. The board reset time is BOARD_FROM.
  - Table `push_subs` stores push subscriptions. Edge function `daily-push` runs hourly through pg_cron and sends at 10am local time (the hour column; it was 20 until 27 Oct 2026).
- **Family voice.** CULTURES (yoruba, igbo, hausa, general) are chosen from the player's state of origin. Gendered stories use PRO().

## Europe
- One route (`eu`, currency €). Players pick a country the way they pick a US state. EU_PLACES holds a card per country: language, hello, the appointment everyone dreads (`office`), whether shops close on Sunday or at lunch (`closed`), how people get around (`move`), `fr` for French-speaking, and `en` for Ireland.
- Countries: Germany, France, Italy, Spain, Netherlands, Belgium, Portugal, Austria, Ireland. Add one by adding a card.
- The language barrier carries the route. Ireland (EN()) gets English versions of the language scenes.
- Scenes live in EU(). Pay events, the day 29 moment, and both life chapters have Europe versions.
- Today's Landing only sends everyone to Europe from EU_FROM (2026-10-27), so days already played keep their plan. Move it to the day after merging if that date has passed.
- The leaderboard table only accepted us, uk, and ca. Run the "Europe route" part at the end of supabase/landings.sql once, or Europe games show "Europe joins the leaderboard very soon" instead of a rank.

## Testing
- `python3 tests/full_games.py` plays 24 random full games with the leaderboard mocked. It must print `ISSUES: none`.
- Chromium and Playwright are needed. Check screens with Playwright screenshots at 390px wide.

## My Life Abroad, the continuing story mode
- **What it is.** One continuing life, separate from Today's Landing. Money, meters, and every flag in `S.f` carry from chapter to chapter.
- **Unlock.** The home card (lifeCardHTML) stays locked until JJC, which is 2 Today's Landings (LIFE_UNLOCK). One chapter opens per day.
- **How a life starts.** Chapter 0 is a normal first month played inside the mode (lifeStart calls begin, then sets `S.life = {ch:0}`). Life games never post to the leaderboard and never enter nyhl-history.
- **Chapters.** CHAPTERS lists all six stages, and every one is written:
  1. Months 2 to 3 · Payslip and Rent (lifeCh1)
  2. Month 6 · First Winter and Paperwork (lifeCh2)
  3. Year 1 · The Anniversary (lifeCh3): ajo payout, the anniversary, visiting home or Mummy visiting, the lease, a brother who wants to japa, meeting someone.
  4. Year 2 · Promotion, Pressure, and Land (lifeCh4): graduation or promotion, wedding pressure, land at home, three school fees, mortgage, burnout, being asked to be a guarantor.
  5. Year 3+ · Papers, Family, or Japada (lifeCh5): papers by route, bringing parents, a job offer in Lagos, owning property, helping the next JJC, and the final question, where is home now (ending: stay, pada, both).
- **The end of a life.** After chapter 5, renderLifeEnd shows the ending title, lifeReceipts() lines, and the score from every stage, then "Start a new life".
- **Chapter scenes.** Ten slots, with 9 or 10 choices and one auto money event (autoEvent `life1` to `life5`, using lifePay). From Year 1, lifePay gives everyone at least a survival wage. `label` is the time shown, `art` picks the picture. inCh() makes showable() show every scene in order. A slot can hold two or three scenes with opposite `when` conditions.
- **Month one comes back.** lifeCallback picks one flag from earlier play (sibling, guest, farm, loan, house, car) once per chapter and stores it in `S.cbk`. lifeComeback writes that scene.
- **Flags.** upkeep, ajo, assoc, licence, december, guest, farm, loan, uber30, fanbelt, car (junked), visited, raise, partner, promo, grad, land, house2, papers, family, pada, owner, ending.
- **Saving.** renderLifeEnd saves nyhl-life `{v, rk, place, ch, doneOn, started, S, log}` once per chapter. lifePlay rebuilds R, L, and S from it. nyhl-life is in MOVE_KEYS, and importing keeps the further-along life.
- **Testing.** `python3 tests/life_mode.py` plays 12 whole lives, arrivals to the ending, and must print `ISSUES: none`. Add `shots` to save screenshots in tests/shots/.

## Real stories and the monthly update
- Players send stories through Tally form q5480d. It asks when the story happened (first month to year 3+) and has a box for later stories.
- STORIES.md logs every submission read, by ID, with where it lives in the game. Never put emails in the repo.
- A scheduled task, "Now You Have Landed monthly stories", runs at 8:53am New York time on the 1st of each month until May 2027. It turns new stories into scenes, runs both test suites, pushes to main only if both pass, and sends Nafeezie a short note.
- Nafeezie's own scenes carry credit:'Nafeezie', own:1. Scenes added after launch are gated with OWN_FROM, so a Today's Landing already in progress never changes mid-day.

## Hands-off checklist (Nafeezie)
- Namecheap: keep auto-renew on for nowyouhavelanded.com.
- Supabase: if an email warns the project will pause, open the dashboard and press Resume.
