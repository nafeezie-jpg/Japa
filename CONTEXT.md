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
- **Saturday and mini-games (21 Nov 2026).** Nafeezie wants it to speak to many people (her mum likes cooking-task games; men play 5-aside, Ayo, ludo, draft, and PS). The week is now Monday to Saturday (SAT = 5), and the bill is due Saturday night. On Saturday, 5-aside is in the morning, the owambe is in the afternoon (moved from Thursday), and Nigerian offices are closed. Both maps are a 5 by 3 grid (x 18/50/82, y 11/30/49/68/87), and PL entries can be undefined (filtered in pins()). Mini-games share mgFrame (full screen, with a skip button #mgauto that gives an average result): cook('buka'|'cater') is a cooking rush (orders from DISHES, ingredient buttons ING, served when the plate matches); ayo() is real Ayo against Baba Sule (greedy AI, capture 2s and 3s); penalties('pitch'|'ps') is 5 kicks each with tap-to-aim and tap-to-dive. Ludo and draft are quick luck outcomes. Abroad has 'Naija hangout' (Ayo, ludo, draft) and FIFA on your own PS at home at night. Balance after Saturday: living A(230) at home and A(280) abroad; yearly Nigerian rent A(6000), about ₦600,000 in Lagos.
- **Not yet.** No leaderboard (it would need its own Supabase table). Ideas: a weekly leaderboard, more places, city-specific radio lines.

## Next up (agreed 31 Oct 2026, Nafeezie returns about 15-16 Nov)
Continuity shipped early, on 3 Nov. The Return Ticket should now be a later-month storyline inside the continuing life. When she opens a new chat with "Return ticket and teen demo":
1. Check two weeks of play since the 2 Nov board (GoatCounter: finishes, return visits, story-form taps) against the weeks before.
2. **The Return Ticket.** Add a special storyline to Now You Have Landed: twelve years abroad, a good salary, little saved, family expects support, and going home means starting over. It tests her "the life people see" idea with existing players. Track plays, finishes, and shares.
3. **Teen demo.** A 10-minute standalone demo of a money game for ages 10-16 (pocket money, a first small hustle, family pressure, Nigerian prices and inflation), for her to show five parents or teachers. No accounts, no open text, no names on boards, no ads. It is the seed of First Paycheck (the Gen Z version), which shares the same engine. Don't call it Monopoly anything.
4. December: decide. If parents or schools lean in, the teen game and First Paycheck become the next product. If not, Now You Have Landed stays the focus.

### Wahala Week: its own front door and a gentle start (22 Nov)
- /week is now its own game. Title "Wahala Week", no back link in the top bar, only a small "Also from us: Now You Have Landed" link at the end of a week and in How to play. A wahalaweek domain can point here later.
- First-time players see a welcome screen (#wgo) before city and character (Step 1 of 2, Step 2 of 2). Tests must click #wgo before .city.
- Week 1 shows only home, work, buka/market and Ryde. UNLOCK in week/index.html opens the rest: week 2 hall, pray, fuel, loan (mechanic too); week 3 viewing centre, Ayo, pitch (school too); stall from week 5. New places glow and are listed in the week intro under "New on your map this week". NEPA nights start in week 2.
- Next: test with 5 to 10 real people (Nafeezie's mum and mother-in-law included) for a week before adding more.

### Sound and a guided first week (22 Nov)
- Both games ask iPhones for `navigator.audioSession.type = 'playback'` and play a tiny silent clip on the first tap, so sound plays even with the ring switch on silent. Sound also wakes on pointerdown, touchend, and click.
- Wahala Week top bar is one target: cash / Saturday total, a bar, and "Earn X more by Saturday night". The yearly rent line and intro row show from week 3.
- Nigerian cities start with 350 × k (was 850), so week 1 needs real earning.
- Week 1 coaching: coachPin() makes work (or the buka when energy is low) glow, and coachText() replaces the idle hint. After tapping a place, showSheet() scrolls the choices into view; idle() scrolls back to the map.

### Wahala Week on the home screen (23 Nov)
- week/manifest.json (scope /week/, start /week/?source=homescreen) and its own icons (week/icon-192.png, icon-512.png, apple-touch-icon.png). Installs as "Wahala Week", separate from Landed.
- A "Put Wahala Week on your phone" card shows on the end-of-week and played-today screens and in How to play. Android gets a real install button; iPhone gets Share, then Add to Home Screen.
- iPhone home screen apps keep their own storage, so progress moves with a code (WW1. + base64 of the nyhl-week save). Copy it in How to play or on the iPhone tip card; paste it from the welcome screen link or How to play.

### Hustles (25 Nov)
- New 🛠️ Hustles pin (x82, y87), open from week 1, every slot. GIGS_HOME and GIGS_ABROAD hold 20+ small jobs each: [id, icon, name, slots, pay, energy, usual, great, wahala]. gigsNow() shows 5 (4 at night), reshuffled every slot by shared luck. doGig: 20% wahala (half pay), 20% great (+A(40)), else normal. P.gigs counts each job; the third time you become "a regular".
- Pay per slot is close to the main job, so balance holds. The welcome card no longer lists jobs.

### Every state, county and province (25 Nov)
- Abroad, the city picker now shows United States, United Kingdom and Canada. Tapping one opens a dropdown with every state (51), county (94, grouped by nation) or province and territory (13), copied from Landed's lists.
- P.place holds the pick. cityFor(key, place) reshapes the base city (Houston, London, Toronto): name becomes the main town, costs and rent scale by Landed's cost tier, and roads, river and hall become generic. Texas, Greater London and Ontario keep the original cities exactly, so old saves are unchanged.
- Tests click #placego after .city for abroad picks.
- Nigeria too (25 Nov): one "Nigeria" button with a dropdown of all 36 states and the FCT (NG_STATES, from Landed's ORIGIN_LIST). Lagos, FCT, Rivers, Oyo, Kano, Enugu and Kwara play their original cities exactly. Every other state plays on the nearest home city (NG_BASE) renamed to its main town, with its own price level (NG_K). Nigeria now sits above the abroad countries in the picker.

### One job a day, Ryde on the way, and home life (25 Nov)
- One earning job per day: work, one hustle, the buka kitchen shift, or the owambe caterer. W.jobDay marks it; the rest show "you already worked today". Pay is roughly a full day: NG work A(200), abroad A(220) day / A(270) night, office A(320)/A(340); hustles pay 1.7x their listed base; kitchen A(20)/A(28) a plate.
- The Ryde pin is gone (Hustles took its spot at x50, y30). startJob() offers "Turn on Ryde on the way" before the job, and done() offers "Turn on Ryde on the way home" after it. rydeCommute(): A(3) a fare, -10 energy, knocks, checkpoint, fan belt if the car is old.
- Step 2 now asks home life too (P.fam: single, married, kids, solo) and needs #mego to start. famCost() adds to living; famShare() is the partner's Saturday share; famRequests() adds in-law, spouse, and school messages; kids bring morning school-run hits; married players get the odd "talk about money" night.
- Careful-bot weekly savings: Lagos single about ₦55k, Lagos with kids about ₦44k, Kano single parent about ₦23k, Texas with kids about $350.
- Ryde is back as its own pin (x82, y87): "Drive all day" is a full day's job (A(80) + A(18) a fare, -45 energy), for players whose main hustle is Ryde. Commute Ryde still runs before and after other jobs.
- No coaching (her call: let people choose, fewer words). coachPin and coachText return nothing, the week 1 guide line and "Where to?" hints are gone, and the welcome cards are one line each.

### Two jobs a day, surprises, and a visible week (25 Nov)
- Her model: you leave home in the morning, hustle all day, and go home. People (in the US too) work two jobs, and surprise costs keep eating the savings.
- Each day: one main job (work, Ryde all day, kitchen shift, or caterer; W.jobDay) plus one hustle (W.gigDay). Ryde on the way is offered before the first job of the day; Ryde home once a day (W.rodeHome).
- Pay now: NG work A(185), abroad A(175) day / A(210) night, office A(300)/A(280); hustles 1.1x base. 
- Surprises: snagFor() gives a 35% chance each part of the day of an "Unexpected" cost card (SNAGS_HOME, SNAGS_ABROAD, plus SNAGS_KIDS).
- No visiting parents. Home has sleep, Call Mummy (NG) or video call (abroad), and an evening with your spouse or children.
- A Monday to Saturday strip sits under the bill bar with the part of the day (🌅 ☀️ 🌙). Each new day opens with a big day card ("MONDAY / MORNING").
- Careful bot: Lagos single about ₦48k saved a week, Kano about ₦28k, Texas about $300.

### Seven days, morning and night, men's and women's jobs (25 Nov)
- The week is Monday to Sunday with two parts a day (SLOTS MORNING, NIGHT; NIGHT = 1). The bill is due Sunday night (lastSlot()). A new day restores 45 energy, so the night's sleep is implied.
- Weekend: offices closed Saturday and Sunday (NG and office jobs); owambe Saturday morning; 5-aside Saturday and Sunday mornings; church or mosque Wednesday night, Friday morning, and Sunday morning.
- Gender: GIG_SEX marks hustles as women's (braiding, make-up, small chops, bread, corn, babysitting, jollof, laundry, cleaning) or men's (dispatch, phone repair, site, moving, DJ, barbing, inverter, security, hype man, kitchen porter, flat-pack). Men don't get the buka kitchen shift or caterer cooking; they set up canopies at the owambe instead. Women don't see 5-aside, the viewing centre, or FIFA at home.
- The drive's skip is now a small "Skip" link under "Start driving".
- Pay now: NG work A(165), abroad A(135) day / A(160) night, office A(280)/A(250); hustles 0.75x base; commute Ryde A(2) a fare; surprises 40% a part of the day at 1.3x listed cost. Careful bot: Lagos about ₦47k saved a week, Kano about ₦27k, Texas about $240.

### Organised map, energy has a price, rarer surprises, context checks (25 Nov)
- Every place has one group (KIND) with a ring colour and a key under the map: Earn (work, Hustles, Ryde), Food and home (home, buka), Faith and parties (church or mosque, owambe), Play (Ayo spot, viewing centre, 5-aside), Errands (fuel, mechanic, loan), Grow (classes, stall). LAYOUT puts each group on its own row. Each place sheet shows its group tag.
- The buka is food and gist only. The cooking game is now a women's hustle ("Kitchen shift at the buka") in Hustles.
- Energy: the bar pulses red under 25 with a warning line. Working while exhausted costs 30% of the pay (W.tiredJob). Hitting zero triggers collapse(): a clinic bill (A(120) NG, A(150) abroad, doubling with each collapse that week), -15 peace, and the rest of the day lost.
- Surprises: at most two a week (nextSnag). One comes when you first have enough for the bill ("Just when things were looking up", 2.5x cost); one when you are struggling from Wednesday on ("As if this week was not hard enough", 1.2x); a Friday-night one if none has come. NEPA 30% of nights, malaria 5%, school-run hits 15%.
- FIFA on the PS (her choice over PES). Men can play it at home at night in Nigeria too.
- Context: woman in hijab gets the Mosque (Wednesday night, Friday Jumat), Alfa Ibrahim in place of Pastor Sunday, the women's circle. "Bae" messages only for single players, and they differ for men and women. Ludo with the boys or the girls. Middle-belt states use Mama Put, Baba Landlord, and Oga Danjuma.
- Home screen: besides the 📲 top-bar button, the welcome screen and the week 1 and 2 intros have an "Add to your home screen" link. Landed links to Wahala Week from its home card and from the done-for-today panel.

### Landed gets Wahala Week's feel (25 Nov)
- Her husband loved how interactive Wahala Week is (music, little reading). She chose: same story and leaderboard, WW feel.
- Music: SFX now runs a soft highlife-Afrobeat loop (startGroove) under the whole game, muted with the same 🔊 button.
- You as a person: youL() puts your avatar (woman, man, or neutral from S.gender) with a prop on every scene picture; moodL() shows a big happy, meh, or facepalm reaction on every result.
- Fewer words: narration fades in line by line; the "about this landing" notes fold into one "ℹ️ About this landing" line; the result screen is just your reaction, the outcome, and the chips (no repeated picture, scene, or "You chose").
- Three tap games in the 30-day game (MINIS, scenes with auto:'mini', so they never count toward the 15 questions): Day 1 baggage carousel (tap your two 🎀 bags), Day 8 run for the bus (tap fast for 5 seconds), Day 13 the African shop (tap only what is on your list). Each has a Skip with an average result. Tests click #mskip.
