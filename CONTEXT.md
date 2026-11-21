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
  - From the 2 Nov 2026 board (RULES2, newRules(t)): Home above HOME_CAP only costs points when cash is under SAFE_RENT or peace is under 80 (homeOverdone). The four hard-luck story titles (Family ATM, Running on Prayers, Hustle Without Peace, Ghost Mode) apply up to a score of 79. The progress road keeps the best level any five-game stretch reached. History games are scored by their own time g.t, so old games keep old rules.
- **Visuals (31 Oct 2026).**
  - The header shows each change floating over the meter label (`.dl`), bars slide from the old value (data-w), and a meter below its low mark turns red (`.stat.low`).
  - Messages render as a phone chat (`.chat`): typing dots, then the bubble with a time and ticks. Mummy's voice notes sit inside the chat as a waveform bubble (`.vnb`, playVN).
  - A scene with `post:[who, emoji, caption]` shows a status post card instead of a drawing.
  - Day 30 shows "Your 30 days in pictures": S.moves holds [day, landing, icon, label] for each choice, from moveIcon(); recapHTML() draws it.
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

## My Life Abroad chapters
- CHAPTERS and lifeCh1 to lifeCh5 hold the stage scenes (Months 2-3, Month 6, Year 1, Year 2, Year 3+). Since 12 Nov they feed Your story (see below). The old separate mode (lifeCardHTML, lifePlay, renderLifeEnd) is no longer reachable from the home screen.

## Real stories and the monthly update
- Players send stories through Tally form q5480d. It asks when the story happened (first month to year 3+) and has a box for later stories.
- STORIES.md logs every submission read, by ID, with where it lives in the game. Never put emails in the repo.
- A scheduled task, "Now You Have Landed monthly stories", runs at 8:53am New York time on the 1st of each month until May 2027. It turns new stories into scenes, runs both test suites, pushes to main only if both pass, and sends Nafeezie a short note.
- livingLarge() (day 23, core, late) shows only to players who sent money home: the Bernabéu status, the rice-money restaurant, the sibling's lounge, the cousin's Lexus, the uncle in Dubai. oldColleagues() (day 21, extra) covers people back home being promoted. Both start with the 2 Nov board.
- Nafeezie's own scenes carry credit:'Nafeezie', own:1. Scenes added after launch are gated with OWN_FROM, so a Today's Landing already in progress never changes mid-day.

## Hands-off checklist (Nafeezie)
- Namecheap: keep auto-renew on for nowyouhavelanded.com.
- Supabase: if an email warns the project will pause, open the dashboard and press Resume.

## Your story (12 Nov 2026): Today's Landing is now one personal life
- Nafeezie found the shared daily boring: it was not her story, and stages repeated. Now every player lives their own life, Month 1 to Year 5, one chapter a day. The leaderboard is unchanged, and every daily chapter still posts a score.
- **Setup.** Tapping Today's Landing without a story opens phase `setup` (setupHTML, wireSetup): country, city, route, funding, gender, who counts on you (DEPS: parents, siblings, kids, none), and a goal (GOALS: papers, house, family, debt, career, savings). Existing players see it pre-filled and keep their money, meters, title, and streak.
- **The life.** It is saved in localStorage nyhl-daily `{v:2, rk, place, n, done, log, started, S}`, where S.me = {goal, deps}. `n` is landings lived in this life. LIFE_LEN = 19, and STAGES[n] gives the label (Month 1 ... Year 5), the chapter (ch 1 to 5, from CHAPTERS), and months covered (mo).
  - Landing 1 is a normal first month (begin, with S.me set).
  - Landings 2 to 19 use contStart and contScenes: a payday auto covering `mo` months (contPay, including family upkeep from DEPS), then 4 choices. Those are 1 goal scene (goalScenes, by `at:[from,to]` range), a family scene on even landings (depScenes), 1 or 2 chapter scenes, and general scenes (contGeneral plus lateScenes for years 2 to 5).
  - The last landing has 3 picks plus the "where is home now" ending choice from lifeCh5.
- **No repeats.** S.cSeen holds every scene lived in this life. CONT_MEMO fixes a chapter's scenes once picked.
- **Goals.** Choices can carry `gp`, which is added to S.f.gp. goalPct() adds passive progress (savings from cash, career from future) and big moments (owner, papers, loan paid, promo). goalResult: 80+ reached, 55+ almost, else not this time.
- **Result screen.** storyEndHTML shows "Chapter n of 19 done", the goal bar, and the road. At landing 19 it shows the whole-life summary: the ending title, the goal result, lifeReceipts, and scores by stage. The next day offers a new life.
- **Migration.** Older players get lifeN(lf), which maps the month they had reached (two weeks a landing) onto the new road. For example, 15 landings is Month 8, so they carry on at Month 10. On setup, gp starts at n × 2.5.
- The separate My Life Abroad card is gone from the home screen. Its CHAPTERS and lifeCh1 to lifeCh5 now feed the story. Old nyhl-life saves are left untouched.
- Japa again and Japada are hidden in story games and stay in practice games.
- **Testing.** `python3 tests/story.py` lives four whole stories (two new, two migrated) and must print `ISSUES: none`. `tests/full_games.py` still must pass.
- **Fresh content.** The monthly story task should add to lateScenes, goalScenes, depScenes, and contGeneral. Scenes are 4 per chapter, so the pool covers a full life without repeats (about 70 per life today).

## Wahala Week (renamed from Rent Week, 20 Nov 2026): the city-map game at /week/
- Nafeezie found the story game boring and asked for something people come back to, in the spirit of GTA. Rent Week is a separate page, week/index.html, linked from a card on the home screen (rentWeekCard, under the name row).
- **Loop.** Each real day is one game week: Monday to Friday, three slots a day (morning, afternoon, night). You tap a place on a city map. Each visit uses a slot and energy. Friday night pays the week's bill.
- **Cities.** CITIES: houston, london, toronto, each with its own currency factor k (A(v) scales amounts), rent, landlord, lender, roads, and river. The city is picked once. The default comes from the story's country.
- **Bills.** MISSIONS cycle every 6 weeks: rent, car note, visa renewal, rent, owambe season, Detty December. Each cycle is 6% dearer. living() adds food, bus, and phone. A shortfall pays what you have, rolls the gap over with a 10% fee (arrears), and adds a warning. Three warnings means eviction: you restart on a cousin's sofa with your history kept.
- **Aunty Alert.** Stars rise when you leave WhatsApp requests on read or let them pile up, and fall when you send money, call home, or go to the owambe. At five stars a Family Raid costs money and peace.
- **Growth.** Mechanic (week 2+): fix the car for good. Night class (week 3+): four classes lead to an office job. Market stall (week 5+, Mama trust 6): earns every Friday. Eight warehouse shifts get the forklift promotion.
- **Shared luck.** luck(tag) is seeded by the date plus the moment of the week, so the same move gives the same outcome for everyone that day.
- **Saved** in localStorage nyhl-week. One week per day; replay shows the done screen and a countdown. Share text works like Wordle.
- **Balance.** A sensible player passes most weeks with modest savings; careless play fails. Check with a smart-player run before changing pay or bills.
- **Tests.** `python3 tests/rent_week.py` plays seven days in each city and must print `ISSUES: none`. window.__rentweek is a read-only peek for tests.
- **Nigeria (20 Nov 2026).** Seven home cities with ng:1: lagos, abuja, ph, ibadan, kano, enugu, ilorin. Prices are in naira; k is about 100 for Lagos and Abuja and 60 for Kano and Ilorin, rounded to ₦500 (STEP). NG() switches in MISSIONS_HOME (house rent, school fees, light and fuel, owambe, Christmas in the village), Naija FM radio, home requests (Cousin Emeka wants to stay "for small time"), friends-abroad statuses, and home places (9 to 5 closed at night, buka, loan app, filling station, mechanic village, ICAN class, POS stand). ngWork() covers late salaries and staying late. NEPA takes light on most nights; fuel from the filling station covers two nights, and without it you lose peace and energy. Balance: Nigerian pay A(120), bank job A(200), living A(200). A sensible player just makes rent in week 1.
- **Everyday Nigeria (20 Nov 2026).** Nafeezie wants the whole everyday hustle, not only rent. The Nigeria map is a 4 by 3 grid: POS stand, church/mosque, 9 to 5 / buka, Ryde, viewing centre / ICAN class, mechanic, loan app / your room, owambe, filling station. Church or mosque is open Wednesday night and Friday afternoon (offering, or networking that can give a job lead or a building-committee levy). The bet shop has a 1 in 4 stake and a viewing centre. You join the ajo at the buka: A(40) every Friday (ajoDue), with the A(240) pot paid in week turn, then every 6 weeks. Malaria can strike some mornings from week 2 (chemist, hospital, or agbo). Morning go-slow deducts pay in ngWork. Once you own the POS stand, area boys sometimes take "owo ile" on Friday. Home WhatsApp also has bae, the caretaker's borehole levy, and Funke's aso ebi. Nigerian start cash is 850 times k.
- **Yearly rent in Nigeria (20 Nov 2026).** Rent in Nigeria is paid once a year, so MISSIONS_HOME has no weekly rent. The weekly bills rotate through light and fuel, school fees, owambe, hospital bill, phone and data, and Detty December. Every 12th week (RENT_EVERY) is RENT RENEWAL at A(3700), about ₦370,000 in Lagos. The HUD shows a countdown and a bar of how much is saved (#rentline). A careful saver only just makes it.
- **Sound and naming (20 Nov 2026).** The star meter is now called Family pressure (it was Aunty Alert). SND is a synthesised Web Audio engine with no audio files: a light Afrobeat groove at 104 bpm (quieter at night) and effects for taps, cash in and out, WhatsApp pings, rising pressure, the day card, NEPA, the generator, the family raid ringtone, and the Friday win or loss. It starts on the first tap. The 🔊 button mutes, and the choice is saved in nyhl-week-sound.
- **Ryde run (20 Nov 2026).** Driving for Ryde opens drive(): a 20-second, three-lane canvas run (swipe, tap, or arrow keys). It has fares (💵) and city obstacles (Lagos: potholes, okadas, danfos, goats, and a checkpoint row with one gap; abroad: potholes, traffic, and a police car row). The course is seeded by luck, so everyone gets the same road that day. rydeResult(): three knocks means a fan-belt breakdown; otherwise pay is A(25) plus A(6) per fare, a checkpoint or ticket costs money, and a clean run with 7 or more fares gives a tip. 'Let the GPS drive' gives an average result with no tip, for players who skip it and for the tests (tests click #dauto). window.__drive is a read-only peek for tests.
- **Help.** The ❓ button on Wahala Week opens How to play. The main site's About and How it works describe both games.
- **No betting; you as a person (20 Nov 2026).** Nafeezie asked to remove betting. The bet shop is now a viewing centre (`view`), open at night, for watching the match or arguing about football. Players pick who they are after the city (pickMe, P.me: w woman, h woman in hijab, m man; all 🏾). pose(k) gives their look at each place (suit at work, dancing at owambe, in bed at home, 🤒 with malaria). The map marker shows the pose and walks between places. Each place, WhatsApp, and malaria screen shows the person (youHTML). Results show a reaction (moodFx: hands up, facepalm, or shrug). The day card, the car in the Ryde run, and the end screen show them too. P.me is kept through eviction.
- **Not yet.** No leaderboard (it would need its own Supabase table). Ideas: a weekly leaderboard, more places, city-specific radio lines.

## Next up (agreed 31 Oct 2026, Nafeezie returns about 15-16 Nov)
Continuity shipped early, on 3 Nov. The Return Ticket should now be a later-month storyline inside the continuing life. When she opens a new chat with "Return ticket and teen demo":
1. Check two weeks of play since the 2 Nov board (GoatCounter: finishes, return visits, story-form taps) against the weeks before.
2. **The Return Ticket.** Add a special storyline to Now You Have Landed: twelve years abroad, a good salary, little saved, family expects support, and going home means starting over. It tests her "the life people see" idea with existing players. Track plays, finishes, and shares.
3. **Teen demo.** A 10-minute standalone demo of a money game for ages 10-16 (pocket money, a first small hustle, family pressure, Nigerian prices and inflation), for her to show five parents or teachers. No accounts, no open text, no names on boards, no ads. It is the seed of First Paycheck (the Gen Z version), which shares the same engine. Don't call it Monopoly anything.
4. December: decide. If parents or schools lean in, the teen game and First Paycheck become the next product. If not, Now You Have Landed stays the focus.
