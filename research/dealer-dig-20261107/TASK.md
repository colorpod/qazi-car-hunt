# Dealer-site dig, McLaren Car Hunt (read-only)

Qazi, Nov 7: "Why don't you go and search the actual dealer site and then find all the additional information, not just saying 'no sticker posted'? It took me two seconds to find it."

For EACH car below, open the selling dealer's OWN website (not CARFAX/Autotrader/CarGurus), find the exact listing by VIN, and click through every document/button on it: "Window Sticker", "Original MSRP / Options Info", iPacket, "Build Sheet", "CARFAX", "Vehicle Video", option list in the description. Example of what was missed: Ilusso's 720S Spider listing had an iPacket "Original MSRP" PDF (window sticker, $345,600 MSRP).

Read-only. Do NOT submit any form, chat, lead, phone or email to a dealer. Do NOT sign in. Never solve a CAPTCHA (skip that site and say so). Do not change any browser settings or cookies.

Write /Users/waqasqazi/Projects/qazi-car-hunt/research/dealer-dig-20261107/RESULTS.json: a list of objects, one per VIN:
{vin, dealer_url (the exact listing page on the dealer site), listing_found (true/false), still_listed (true/false), price_on_dealer_site, msrp (number or null), msrp_source, sticker_url (direct PDF/image URL of window sticker or MSRP sheet, or null), carfax_url (free CARFAX link on dealer site, or null), options (list of option names with prices when shown), video_url, other_docs (list of {label,url}), notes (one line: what was checked, e.g. "dealer site has no sticker; checked iPacket, documents tab, description")}

Also download each sticker PDF/image you find to /Users/waqasqazi/Projects/qazi-car-hunt/research/dealer-dig-20261107/stickers/<VIN>.<ext>.

Cars:
- SBM14DCA7NW006975 | Chicago Motor Cars | 2022 · Performance, Black / Black, lift, sport exhaust, B&W  | $300,511 | 8,879 mi
- SBM14DCAXLW005591 | McLaren Chicago | 2020 · Performance, Black / Black. Stock P1263 | $265,300 | 8,621 mi
- SBM14DCA1KW002478 | Motor Cars of Chicago (Gray) | 2019 · Luxury, Sarthe Grey / Gray. Stock 10635 | $250,372 | 5,715 mi
- SBM14DCA3KW002482 | Motor Cars of Chicago (Red) | 2019 · Memphis Red / Black, carbon, Opti-Coat. Stock 11153 | $230,372 | 15,753 mi
- SBM14DCA3KW002501 | McLaren Scottsdale | 2019 · price on request | $0 | 1,899 mi
- SBM14DCA8MW006188 | Long Island Sports Cars | 2021 · Performance, Red / Black, carbon ceramics, soft-close | $288,063 | 8,795 mi
- SBM14DCA6KW002489 | Autopark Dallas | 2019 · Luxury, Black / Black, carbon aero, lift, aftermarket | $241,995 | 10,554 mi
- SBM14DCA8KW003563 | European Exotic Center | 2019 · Onyx Black / Black Alcantara, carbon interior, forged | $259,995 | 5,505 mi
- SBM14FCA6LW004109 | McLaren San Francisco | 2020 · Luxury, Volcano Yellow / Black, MSO Black Pack, carbo | $269,991 | 6,969 mi
- SBM14FCA5LW004487 | European Exotic Center Tampa | 2020 · Pearl White / Tan, carbon pack, carbon interior | $265,994 | 10,513 mi
- SBM14FCA8LW004046 | Holman Motorcars | 2020 · White / Black | $281,348 | 4,755 mi
- SBM14FCA8KW003736 | Motor Cars of Chicago (2019 Black) | 2019 · Performance, Black / Black | $270,372 | 5,552 mi
- SBM14FCA0NW006697 | McLaren Chicago (2022) | 2022 · Performance, Gray / Black | $280,300 | 19,578 mi
- SBM14FCAXLW004940 | Autopark Dallas (Yellow) | 2020 · Performance, Yellow / Black | $279,995 | 11,821 mi
- SBM13SAA8LW008113 | HyperCars | 2020 · Purple / Black | $270,189 | 13,393 mi
- SBM13SAA1LW008566 | Chicago Motor Cars | 2020 · MSO Cirrus Grey / Carbon Black, Luxury Pack, carbon l | $260,511 | 15,205 mi
- SBM13SAA5LW007615 | 1 of 1 Motorsports | 2020 · White / Red | $246,493 | 18,132 mi
- SBM13SAA0LW007683 | One Exotics | 2020 · Saros / Carbon Black, MSO carbon, exhaust | $259,813 | 15,825 mi
- SBM13SAA4LW008254 | Motor Cars of Chicago (Blue) | 2020 · Blue / Black | $235,372 | 12,454 mi

Known dealer sites: chicagomotorcars.com, mclarenchicago.com, motorcarsofchicago.com (Joliet), mclarenscottsdale.com, longislandsportscars.com, autoparkdallas.com, europeanexoticcenter.com (and exoticsgroup.com), mclarensanfrancisco.com, holmanmotorcars.com, hypercars (Indiana), 1of1motorsports.com, oneexoticstampa.com.
Done = RESULTS.json has all 19 VINs with notes for each.
