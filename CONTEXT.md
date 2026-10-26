# Now You Have Landed: context for new sessions

Read this, then read index.html, before changing anything.

## The game
- Browser game about a Nigerian's first 30 days in the US, UK, or Canada. Live at nowyouhavelanded.com.
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

## Testing
- `python3 tests/full_games.py` plays 24 random full games with the leaderboard mocked. It must print `ISSUES: none`.
- Chromium and Playwright are needed. Check screens with Playwright screenshots at 390px wide.

## Next task: "My Life Abroad", the continuing story mode
- A separate mode from Today's Landing.
- One continuing life. Each chapter is a later stage, and meters carry over between chapters.
- One chapter unlocks per day. Possible unlock condition: reaching JJC.
- Possible stages:
  1. Months 2 to 3: first payslip and rent
  2. Month 6: first winter and paperwork
  3. Year 1: the anniversary, and whether to visit home
  4. Year 2: promotion, wedding pressure, land at home
  5. Year 3 and later: PR or citizenship, bringing family over, japada
- About 8 to 10 scenes per chapter, with versions. Nafeezie's and players' real stories make it authentic, so add a stage question to the Tally form.
- Save the life in localStorage and include it in the move code.
- End the life with a summary.
