# Qazi Car Hunt

Qazi's car searches, each run through its full CARFAX. One Cloudflare Worker serves one page: searches grouped by make, and each search expands into its report (repair chart, what changed, ranked car cards with service timelines).

- Live and public: https://qazi-car-hunt.waqasqazi.workers.dev
- Stack: `worker.js` + `app.html` (inline CSS/JS) + `searches/*.json`. No build step.

## Add a search

1. Pull the full CARFAX for each car (carfax.com/vehicle/<VIN> "View FREE CARFAX Report", or the dealer's Autotrader/site link). Save line-by-line notes in `research/<search-id>/<dealer>-<VIN>.txt`.
2. Write `searches/<make>-<model>-<yyyy-mm>.json` in the same shape as `mclaren-650s-spider-2026-10.json`:
   - search: `id, make, model, date, scope, title, lead, facts[[text, g|w|b|""]], takeaway, shift[[headline, line]], sources, cars[]`
   - car: `r` rank, `mv` ("up 1" / "down 4" / "same"), `g` grade, `gc` (a|b|c), `pick`, `name, car, loc, price, mi, own`, `vin`, `listed` (first-listed date from CarGurus daysOnMarket; the page counts days live), `msrp` + `msrpSrc` (original sticker or dealer listing, else null), `carfax` (free report link from carfax.com/vehicle/<VIN> "View FREE CARFAX Report", the dealer site, or iPacket), `sticker` (window sticker PDF, e.g. iPacket "Original MSRP"), `soldOn` when sold, `maj` / `oth` repair counts (null = no report), `auc` auctions, `rep` one-line repair list, `tl[[when, r|w|m|s, html]]`, `verdict`, `url`
   - timeline kinds: `r` repair, `w` gap or check, `m` routine service, `s` owner change or sale
3. Import it in `searches/index.js`.
4. `wrangler deploy`, then open the page and check the new search on a phone width.

## Grading rule of thumb

Rank by how the car has lived, not by price: repairs beyond routine maintenance (engine, gearbox, electrical count as major), repeat repairs, auctions, duplicate titles, short ownerships, and long gaps with no service.
