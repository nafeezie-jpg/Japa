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
  - Healthy marks are MARKS = {peace:60, home:50, future:40}, and HOME_CAP = 85. Cash is healthy at 3 months' rent.
  - `scoreOf` gives about 60 when all four meters are healthy and 100 when all are excellent.
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
  - Practice games ("Play more") don't count.
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
- **Home screen.** Your details, then the Today's Landing hero (or the tomorrow card once played), progress tiles, "What is this game?" (openAbout, also /?about), "Play more", and "How it works" (openHow, also /?how).
- **Move my progress.** openMove copies a NYHL1 code between Safari and the home screen app, which keep separate storage on iPhone.
- **Supabase.**
  - Project mydzixaknqldrcfakirn. The publishable key is in index.html.
  - Table `landings` allows insert and select only, with a guard trigger. The boards are Best landing, Most streetwise, Hardest heart, Softest heart, and Most trusting. The board reset time is BOARD_FROM.
  - Table `push_subs` stores push subscriptions. Edge function `daily-push` runs hourly through pg_cron and sends at 8pm local time.
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
- **Chapters.** CHAPTERS lists all six stages. A chapter is playable when it has `scenes`. Built so far:
  1. Months 2 to 3 · Payslip and Rent (lifeCh1)
  2. Month 6 · First Winter and Paperwork (lifeCh2)
  3. Year 1 · The Anniversary (to write)
  4. Year 2 · Promotion, Pressure, and Land (to write)
  5. Year 3+ · Papers, Family, or Japada (to write). Ends the life with a summary built from `log`.
- **Chapter scenes.** Ten slots numbered by `day` 1 to 10, with 9 choices and one auto money event (autoEvent `life1`, `life2`, using lifePay). `label` is the time shown, `art` picks the picture. Versions use pickV keys starting with `L1` or `L2`. inCh() makes showable() show every scene in order.
- **Month one comes back.** lifeCallback picks one flag from earlier play (sibling, guest, farm, loan, house, car) once per chapter and stores it in `S.cbk`. lifeComeback writes that scene.
- **Flags set so far.** upkeep, ajo, assoc, licence, december, guest (notice, paying), farm (sold), loan (plan). Later chapters should pay these off. For example, ajo slot nine pays out around month 11.
- **Saving.** renderLifeEnd saves nyhl-life `{v, rk, place, ch, doneOn, started, S, log}` once per chapter. lifePlay rebuilds R, L, and S from it. nyhl-life is in MOVE_KEYS, and importing keeps the further-along life.
- **Testing.** `python3 tests/life_mode.py` plays 12 lives through every written chapter and must print `ISSUES: none`. Add `shots` to save screenshots in tests/shots/.
- **Still to do.** Write chapters 3 to 5 and the life summary. Add a stage question to the Tally form so players can send stories for a chapter.
