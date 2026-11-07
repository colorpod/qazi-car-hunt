# Motor Cars of Chicago: who are the top salespeople (read-only)

Qazi, Nov 7: "Just go through Google reviews, sort by newest, and see... the top three people... whose name keeps popping up, who's crushing it. Those are the people that we should reach out to, ideally. If you can find their contact information or their cell, that would be perfect."

Use Walt Chrome (CDP 9333) through scripts/walt_browser.py, background_page only, signed-in Google. Read-only: do not write, like, or reply to any review; do not submit any dealer form, chat, call or text; do not change any setting. Never solve a CAPTCHA.

1. Open this Google Maps place (Motor Cars of Chicago, 3301 Essington Rd, Joliet IL): https://www.google.com/maps/place/Motor+Cars+of+Chicago/@41.5865183,-88.1659021,17z/data=!4m8!3m7!1s0x880e61659ce9cba1:0x4df4091906cbbc3e!8m2!3d41.5865143!4d-88.1633272!9m1!1b1!16s%2Fg%2F11l2wc6qnt
2. Reviews tab, Sort = Newest. Scroll and expand ("More") until you have read at least the 200 newest reviews (or everything back 12 months, whichever is more).
3. For each review record: date (relative is fine), stars, every staff first/last name mentioned, and the role if stated (sales, finance, manager, detail). Count mentions per person, split by: total, 5-star mentions, mentions in the last 90 days, and any negative mentions (1-2 stars).
4. Top three salespeople = most recent 5-star mentions in sales roles. For each one, find contact info from public sources: the dealer's own site staff page (mcofchicago.com "About Us"/team), their LinkedIn, Instagram, dealer bio, email signature formats, and any review or post that quotes a direct cell or email. Record the source URL for every phone/email. Do not guess an email pattern unless you mark it "pattern, unverified".
5. Write /Users/waqasqazi/Projects/qazi-car-hunt/research/salespeople-20261107/mcoc.json:
{"dealer":"Motor Cars of Chicago","reviews_read":N,"oldest_read":"...","sort":"Newest",
 "people":[{"name","role","mentions","five_star","last_90d","negative","latest_mention_date","quotes":[up to 2 short quotes, under 20 words each],"phone","phone_src","email","email_src","instagram","linkedin","notes"}],
 "top3":["name","name","name"], "method":"one line"}
Sort people by five_star desc. Include everyone mentioned 2+ times.
Done = mcoc.json written with reviews_read >= 200 and top3 filled.
