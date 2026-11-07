# AutoPark Dallas and Miller Motorcars: top salespeople (read-only)

Qazi, Nov 7: "Just go through Google reviews, sort by newest, and see... the top three people... whose name keeps popping up, who's crushing it. Those are the people that we should reach out to, ideally. If you can find their contact information or their cell, that would be perfect."

Use Walt Chrome (CDP 9333) through scripts/walt_browser.py, background_page only, signed-in Google. Read-only: do not write, like, or reply to any review; do not submit any dealer form, chat, call or text; do not change any setting. Never solve a CAPTCHA.

Do this for TWO dealers, one file each:
A. AutoPark Dallas, 1201 N Stemmons Fwy / Lewisville TX area (autoparkdallas.com). Find its Google Maps place by searching "AutoPark Dallas Lewisville".
B. Miller Motorcars, 342 W Putnam Ave, Greenwich CT (millermotorcars.com). It is a multi-brand store (McLaren, Pagani, Aston, Bugatti...): use the main Miller Motorcars Google place; note if McLaren Greenwich has its own place and read that too.

For each dealer:
1. Google Maps place, Reviews, Sort = Newest. Scroll and expand until at least 200 newest reviews (or 12 months, whichever is more).
2. Per review: date, stars, every staff name mentioned, role if stated. Count per person: total, five_star, last_90d, negative (1-2 stars).
3. Top three salespeople = most recent five-star mentions in sales roles. For each, find public contact: dealer staff page (autoparkdallas.com team/about, millermotorcars.com staff), DealerRater employee pages, LinkedIn, Instagram, dealer bios, any review or post quoting a direct cell or email. Source URL for every phone/email. Mark guessed emails "pattern, unverified".
4. Write /Users/waqasqazi/Projects/qazi-car-hunt/research/salespeople-20261107/autopark.json and miller.json in this shape:
{"dealer","reviews_read","oldest_read","sort":"Newest","people":[{"name","role","mentions","five_star","last_90d","negative","latest_mention_date","quotes":[<=2 short quotes under 20 words],"phone","phone_src","email","email_src","instagram","linkedin","notes"}],"top3":[...],"method"}
Sort by five_star desc, include everyone mentioned 2+ times.
Done = both files written with top3 filled.
