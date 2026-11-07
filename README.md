# Qazi Car Hunt

Qazi's car searches, each run through its full CARFAX. One Cloudflare Worker serves one page: searches grouped by make, and each search expands into its report (repair chart, what changed, ranked car cards with service timelines).

- Live and public: https://qazi-car-hunt.waqasqazi.workers.dev
- Stack: `worker.js` + `app.html` (inline CSS/JS) + `searches/*.json`. No build step.

## Add a search

1. Pull the full CARFAX for each car (carfax.com/vehicle/<VIN> "View FREE CARFAX Report", or the dealer's Autotrader/site link). Save line-by-line notes in `research/<search-id>/<dealer>-<VIN>.txt`.
2. Write `searches/<make>-<model>-<yyyy-mm>.json` in the same shape as `mclaren-650s-spider-2026-10.json`:
   - search: `id, make, model, date, scope, title, lead, facts[[text, g|w|b|""]], takeaway, shift[[headline, line]], sources, cars[]`
   - car: `r` rank, `mv` ("up 1" / "down 4" / "same"), `g` grade, `gc` (a|b|c), `pick`, `name, car, loc, price, mi, own`, `vin`, `listed` (first-listed date from CarGurus daysOnMarket; the page counts days live), `msrp` + `msrpSrc` (original sticker or dealer listing, else null), `carfax` (free report link from carfax.com/vehicle/<VIN> "View FREE CARFAX Report", the dealer site, or iPacket), `sticker` (window sticker PDF, e.g. iPacket "Original MSRP"), `soldOn` when sold, `rev` (dealer reputation Yelp first, then DealerRater, Cars.com, BBB, Google last: `tone` g|w|b|"", `scores[[site, value, url]]`, `good`, `bad`), `maj` / `oth` repair counts (null = no report), `auc` auctions, `rep` one-line repair list, `tl[[when, r|w|m|s, html]]`, `verdict`, `url`
   - timeline kinds: `r` repair, `w` gap or check, `m` routine service, `s` owner change or sale
3. Import it in `searches/index.js`.
4. `wrangler deploy`, then open the page and check the new search on a phone width.

## Keep it current

A card is never finished. The same turn a dealer sends anything (CARFAX, sticker, option list, video, price, shop answer), it goes on the card, then deploy. `python3 status_sweep.py` compares every listing's price and sale status against `status.json` through Walt Chrome and prints CHANGE lines. A dealer's CARFAX PDF goes in `carfax/<VIN>.pdf` with a route in `worker.js`.

## Ask for (who to contact)

Every dealer gets an `ask` block on its cards (Qazi, Nov 7): read its Google reviews sorted by Newest (200+ or 12 months), count the staff named, and list the top three salespeople by recent five-star mentions, with role, counts and public contact (direct cell, email, Instagram, LinkedIn, each with its source). A guessed email is marked "pattern, unverified". Shape: `ask: {basis, people: [{name, line, phone, email, emailNote, ig, li}]}`. Research lands in `research/salespeople-<date>/<dealer>.json`.

## Grading rule of thumb

Rank by how the car has lived, not by price: repairs beyond routine maintenance (engine, gearbox, electrical count as major), repeat repairs, auctions, duplicate titles, short ownerships, and long gaps with no service.

## Pictures

Any car photo added to the page gets the 3-step zoom (Qazi, Nov 2: default, 150%, 200% = fit to width). Paste `/Users/waqasqazi/Projects/qazi-os-2/artifacts/walt-zoom3/zoom3.html` before `</body>` in `app.html`, deploy, and test a tap at 390 px.
