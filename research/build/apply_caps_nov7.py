"""Nov 7 rework on Qazi's word: price caps per body style, picks only at or under the cap,
and dealer-site documents (stickers, MSRP, options) merged from research/dealer-dig-20261107."""
import json, os, re
B = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(B); ROOT = os.path.dirname(R)
import subprocess
def load(i):  # always start from the committed Nov 7 build so reruns are clean
    return json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', f'3f7b5a3:searches/{i}.json']))
def save(i, d): json.dump(d, open(f'{ROOT}/searches/{i}.json', 'w'), indent=1, ensure_ascii=False)
def car(d, vin): return next(c for c in d['cars'] if c['vin'] == vin)
def k(n): return f'${n/1000:.0f}k' if n % 1000 == 0 else f'${n:,}'

CAPS = {
 'mclaren-720s-coupe-2026-11': dict(low=230000, max=240000, why="Qazi's cap: $260k to $270k already buys a 720S Spider, so a coupe stops at $240k."),
 'mclaren-720s-spider-2026-11': dict(low=260000, max=270000, why="Qazi's cap for a Spider. 2020-21 Spiders actually sold for $229k to $254k, so the cap is a ceiling, not the target."),
 'mclaren-600lt-spider-2026-11': dict(max=225000, why="Walt's cap from sold cars: 600LT Spiders sold for $195k to $225k this year (median $201k). Every ask today is over it."),
}
PICKS = {
 'mclaren-720s-coupe-2026-11': {'SBM14DCA3KW002482'},
 'mclaren-720s-spider-2026-11': {'SBM14FCA6LW004109', 'SBM14FCA5LW004487'},
 'mclaren-600lt-spider-2026-11': set(),
}
VERDICT_LEAD = {  # {o} = dollars over the cap, filled after dealer prices merge
 # coupe
 'SBM14DCA3KW002482': "<b>Pick: the only clean coupe under the cap.</b> $229,995 on the dealer's site plus a $377.63 doc fee, inside $230k to $240k. ",
 'SBM14DCA1KW002478': "<b>{o} over the cap, and the dealer lists it with a tune and downpipes.</b> A modified engine on a 720S is a warranty and resale problem: only with stock parts back on and at $240k. ",
 'SBM14DCA7NW006975': "<b>{o} over the cap. Out.</b> Clean car, wrong price: that money buys a Spider. ",
 'SBM14DCAXLW005591': "<b>Sold.</b> McLaren Chicago's own site moved it to Previously Sold. ",
 'SBM14DCA8MW006188': "<b>{o} over the cap. Out.</b> ",
 'SBM14DCA6KW002489': "<b>Over the cap and a skip anyway.</b> ",
 'SBM14DCA8KW003563': "<b>{o} over the cap.</b> Only at $240k or less. ",
 'SBM14DCA3KW002501': "<b>Price on request.</b> Worth one call only if they land at $240k. ",
 # spider
 'SBM14FCA6LW004109': "<b>Pick: under the $270k cap.</b> Still push to $250k; 2020 Spiders sold for $229k to $254k. ",
 'SBM14FCA5LW004487': "<b>Under the $270k cap at $264,995.</b> Offer $250k. ",
 'SBM14FCA9MW006325': "<b>{o} over the cap.</b> The local one, with its window sticker on Ilusso's site ($345,600 MSRP). Only at $270k or less. ",
 'SBM14FCA8LW004046': "<b>{o} over the cap.</b> ",
 'SBM14FCA8KW003736': "<b>Under the cap at $269,995, but no service paper in 5 years.</b> ",
 'SBM14FCA0NW006697': "<b>{o} over the cap. Out</b> at 19,578 mi and 3 owners. ",
 'SBM14FCAXLW004940': "<b>{o} over the cap and unserviced. Out.</b> ",
 # 600LT
 'SBM13SAA8LW008113': "<b>{o} over the $225k cap.</b> Best history, $316,027 original MSRP with $43k of options on the dealer's site. Worth it only near $225k. ",
 'SBM13SAA3LW008231': "<b>{o} over the cap. Out.</b> ",
 'SBM13SAA1LW008566': "<b>{o} over the cap.</b> ",
 'SBM13SAA5LW007615': "<b>{o} over the cap at $244,998.</b> Closest real-service car to it. Offer $225k. ",
 'SBM13SAA7LW008233': "<b>{o} over the cap. Out.</b> ",
 'SBM13SAA0LW007683': "<b>{o} over the cap. Out.</b> ",
 'SBM13SAA4LW008254': "<b>{o} over the cap, and 6 owners. Out.</b> ",
}
TEXT = {
 'mclaren-720s-coupe-2026-11': dict(
   facts=[["Cap $230k to $240k", "g"], ["1 clean coupe under it: red 2019, $229,995", "g"], ["Gray 2019 has a tune and downpipes", "b"], ["McLaren Chicago 2020: sold", ""], ["2022 at $299,800 is out", "b"]],
   takeaway="My two cents: Motor Cars of Chicago's red 2019 at $229,995 is the only clean coupe inside your $240k cap. Get its photos and a PPI first: it went through an auction last month. The gray 2019 is off the list: the dealer's own page says tune and downpipes. Everything over $260k is Spider money, so the 2022 at $299,800 is out."),
 'mclaren-720s-spider-2026-11': dict(
   facts=[["Cap $260k to $270k", "g"], ["3 under it: SF $269,991, Tampa $264,995, Chicago $269,995", "g"], ["Ilusso 2021: $9,900 over, sticker $345,600", "w"], ["Spider sales median $246,655", ""], ["Cheapest one is a branded title", "b"]],
   takeaway="My two cents: McLaren San Francisco's one-owner 2020 at $269,991 is the pick inside your cap; push it to $250k since 2020 Spiders sold for $229k to $254k. Ilusso's 2021 is the nicest and the closest, but $279,900 is $9,900 over the cap: only at $270k. Skip the $230k McLaren Chicago car, it has a branded title."),
 'mclaren-600lt-spider-2026-11': dict(
   facts=[["Cap $225k, from sold cars", "w"], ["0 of 7 under the cap", "b"], ["Closest: 1 of 1, $244,998", "w"], ["Sales median $201,000", ""], ["3 of 7 have 5+ owners", "b"]],
   takeaway="My two cents: no 600LT Spider is under the $225k cap today. They sell for $195k to $225k and dealers ask $235k to $295k. Open at $225k on the purple HyperCars car (best history, $316,027 MSRP) and the 1 of 1 car (closest at $244,998), and let them come to you."),
}

FIX = [  # old wording that fought the cap
 ('<b>My pick.</b> ', ''),
 ('Get the CARFAX from the dealer before it can rank.', 'The dealer site now links its CARFAX.'),
 ('Lowest miles of the clean cars, McLaren-serviced', 'Lowest miles, McLaren-serviced'),
 (' Ask for the window sticker PDF and push for $280k: the coupe sales below run $219k to $270k.', ''),
 ('; offer $245k.', '.'),
 ('Fine for a driver at $230k.', 'Fine for a driver at $225k.'),
 (' MSRP from the CARFAX listing where shown; iPacket refused these VINs.', ' MSRP from the CARFAX listing where shown.'),
 (' Window stickers: iPacket refused these VINs; Chicago Motor Cars says the 2022 comes with its original sticker.', ''),
]
OUT = {'SBM14DCA1KW002478','SBM14DCA7NW006975','SBM14DCA8MW006188','SBM14DCA6KW002489','SBM14FCA0NW006697','SBM14FCAXLW004940',
       'SBM13SAA3LW008231','SBM13SAA7LW008233','SBM13SAA0LW007683','SBM13SAA4LW008254'}

MANUAL = {  # read by Walt on mcofchicago.com, Nov 7 (client-rendered pages Codex could not find)
 'SBM14DCA3KW002482': dict(listing_found=True, still_listed=True, dealer_url='https://mcofchicago.com/vehicle-details/?id=2019-mclaren-720s-coupe-sbm14dca3kw002482', price_on_dealer_site=229995, carfax_url='https://www.carfax.com/VehicleHistory/p/Report.cfx?partner=DVW_1&vin=SBM14DCA3KW002482', notes='Dealer site checked: price, doc fee $377.63, specs, history report; no photos, sticker or option list posted yet.'),
 'SBM14DCA1KW002478': dict(listing_found=True, still_listed=True, dealer_url='https://mcofchicago.com/vehicle-details/?id=2019-mclaren-720s-coupe-sbm14dca1kw002478', price_on_dealer_site=249995, msrp=358000, msrp_source='Dealer headline: "Big $358K MSRP" (rounded, no sticker)', carfax_url='https://www.carfax.com/VehicleHistory/p/Report.cfx?partner=DVW_1&vin=SBM14DCA1KW002478', notes='Dealer site checked: headline says $358K MSRP and TUNE & DOWNPIPES; no sticker or option list posted.'),
 'SBM13SAA4LW008254': dict(listing_found=True, still_listed=True, dealer_url='https://mcofchicago.com/vehicle-details/?id=2020-mclaren-600lt-spider-convertible-sbm13saa4lw008254', price_on_dealer_site=234995, notes='Dealer site checked: price and specs; no sticker posted.'),
}

ASK = {  # Qazi Nov 7: who keeps coming up in the newest Google reviews, with contact info
 'Motor Cars of Chicago': dict(basis='218 newest Google reviews, Nov 7', people=[
   dict(name='Dorry Adkins', line='Sales associate. Named in 27 reviews, 26 five-star, 0 bad.', phone='(815) 733-6111', email='dorry@mcofchicago.com', emailNote='pattern from zach@mcofchicago.com, unverified'),
   dict(name='Ray Rehan', line='Managing partner. Named in 22 reviews, 21 five-star, newest a week ago.', phone='(815) 733-6111', email='ray@mcofchicago.com', emailNote='pattern, unverified'),
   dict(name='Imad Khan', line='Sales associate. Named in 15 reviews, all five-star, 3 in the last 90 days.', phone='(815) 733-6111', email='imad@mcofchicago.com', emailNote='pattern, unverified', ig='https://www.instagram.com/imadkhan7/'),
   dict(name='Zach Hashmi', line='Buys cars for the store. 19 five-star reviews. Already emailed with us (R8).', phone='(815) 733-6111', email='zach@mcofchicago.com', emailNote='verified, our own thread'),
 ]),
}
ASK['AutoPark Dallas'] = ASK['Autopark Dallas'] = dict(basis='210 newest Google reviews, Nov 7', people=[
   dict(name='Johnny Siamro', line='Sales. 62 five-star mentions, newest 3 days ago. Emailed Nov 7.', phone='(214) 945-2601', email='info@autoparkdallas.com', emailNote='dealer inbox, ask for Johnny', ig='https://www.instagram.com/lordbaesic/'),
   dict(name='Jay Laith', line='Sales and management. 54 five-star, 14 in the last 90 days, 3 bad.', phone='(214) 945-2601', email='info@autoparkdallas.com', emailNote='dealer inbox', ig='https://www.instagram.com/jayscarstx/'),
   dict(name='Jake (Jacob)', line='Sales. 12 five-star, 6 in the last 90 days.', phone='(214) 945-2601', email='info@autoparkdallas.com', emailNote='dealer inbox'),
 ])
ASK['Miller Motorcars'] = dict(basis='210 newest Google reviews, Miller and McLaren Greenwich, Nov 7', people=[
   dict(name='Nick Leiningen', line='McLaren sales specialist. Most-named on the McLaren Greenwich reviews. Emailed Nov 7.', phone='(475) 253-2707', email='nickleiningen@millermotorcars.com', emailNote='pattern from a contact database, unverified', ig='https://www.instagram.com/mclarensfromnick/'),
   dict(name='Aleksey Katkov', line='McLaren sales associate, older reviews.', phone='(475) 253-2707'),
   dict(name='Dario Torregiani', line='Aston Martin sales, 3 five-star in the last 90 days.', phone='(475) 244-9278', ig='https://www.instagram.com/dariolations/'),
 ])
ASK['West State Motorsport'] = dict(basis='200 newest Google reviews, Nov 7', people=[
   dict(name='McKay Rands', line='Sales. 43 five-star, 9 in the last 90 days, 0 bad. Emailed Nov 7.', phone='(425) 200-5976', email='contact@wsmwa.com', emailNote='dealer inbox, ask for McKay', ig='https://www.instagram.com/mckayrands/', li='https://www.linkedin.com/in/mckay-rands-970419325'),
   dict(name='Luke', line='Sales. 26 five-star, 0 bad.', phone='(425) 200-5976', email='contact@wsmwa.com', emailNote='dealer inbox'),
   dict(name='Kameron', line='Sales. 11 five-star, 5 in the last 90 days, 1 bad.', phone='(425) 200-5976', email='contact@wsmwa.com', emailNote='dealer inbox'),
 ])

NEW = {  # cars Qazi saved or sent Nov 7, read by Walt on CARFAX and the dealer pages
 'mclaren-720s-spider-2026-11': [
  dict(g='B-', gc='b', name='AutoPark Dallas (Gray)', car='2020 · Performance, Gray / Black and red Alcantara, electrochromic roof, carbon. Stock 3402', loc='AutoPark Dallas, Lewisville, TX', price=269995, mi='5,793', own='2', maj=0, oth=0, auc=0, vin='SBM14FCA9LW004721', listed='2026-04-16', msrp=None, msrpSrc='Dealer listing: no sticker posted', carfax='https://www.carfax.com/vehiclehistory/ccl/8OkoBzJRP8uKVfbAAKY92CM0Qno_9xBQ_oPJB8f0D49_tI6hqHM77jTBw66MUWxSWcUgSeSW1f26hP1YGNLFbmSteoOrP3ehqu-Q4_mO', sticker=None, stickerNote='Dealer site: no sticker',
       rep='No repairs reported. Serviced only at independent shops (Kwik Kar, a car wash oil change, Pegasus Exotic).',
       tl=[['Nov 2019','s','Owner 1, personal lease, Aubrey TX'],['2021-24','w','Oil changes at Frisco quick-lube shops, never McLaren'],['Apr 2026','s','Offered for sale at AutoPark, 5,793 mi'],['Jun 2026','s','<b>New owner titled</b> in The Colony, TX'],['Oct 2026','w','<b>9,368 mi</b> at Pegasus Exotic, Garland. Listing still says 5,793']],
       verdict='<b>Under the $270k cap, but the listing may be stale.</b> CARFAX shows a new owner in June and 9,368 mi in October. Johnny was asked Nov 7 if it is still for sale and the real miles.',
       url='https://www.autotrader.com/cars-for-sale/vehicle/777738409'),
  dict(g='?', gc='', name='Miller Motorcars (Saros)', car='2020 · Saros / Carbon Black and Jet Black', loc='McLaren Greenwich (Miller Motorcars), Greenwich, CT', price=280699, mi='9,279', own='?', maj=None, oth=None, auc=None, vin='SBM14FCAXLW004596', listed=None, msrp=None, msrpSrc='Asked Nick for the sticker Nov 7', carfax=None, carfaxNote='Not on CARFAX listings', sticker=None, stickerNote='Asked Nick Nov 7',
       rep='No CARFAX listing found for this VIN; history not read yet.', tl=[['Nov 2026','w','Saved by Qazi on Autotrader. CARFAX has no listing for this VIN']],
       verdict='<b>$10,699 over the $270k cap.</b> Nick at McLaren Greenwich was asked Nov 7 for the sticker, records and best out-the-door.',
       url='https://www.autotrader.com/cars-for-sale/vehicle/793669517'),
 ],
 'mclaren-600lt-spider-2026-11': [
  dict(g='B-', gc='b', name='West State Motorsport', car='2020 · Elite Sicilian Yellow / Carbon Black, MSO Clubsport Pack, racing seats, front PPF. Stock WSM2491', loc='West State Motorsport, Federal Way, WA', price=259700, mi='14,601', own='4', maj=0, oth=1, auc=0, vin='SBM13SAA5LW007971', listed='2026-10-05', msrp=309550, msrpSrc='Dealer listing: total original MSRP $309,550 with MSO Clubsport Pack $22,090', carfax='https://www.carfax.com/vehiclehistory/ccl/eOCbVdZOGV8fEoq5dKGhM8u7-XZNVynLxqrjxzHo74o_E2D9rtHiUBMpJoU31NFMRIVH_QStA9M9qUXKoiOPrQj-ifEdYr_evVyECWHY', sticker=None, stickerNote='Dealer site: option list, no sticker',
       rep='Coolant reservoir replaced (Mar 2024). Tires replaced at a dealer PDI (Feb 2026).',
       tl=[['Aug 2019','s','Owner 1, personal lease'],['Apr 2022','s','Owner 2, lease, 6,800 mi'],['Jun 2023','s','Owner 3, 8,368 mi'],['Mar 2024','r','Serviced, coolant reservoir replaced'],['2024-26','w','No service for almost 2 years'],['Mar 2026','s','Owner 4, 10,236 mi'],['Oct 2026','s','Back for sale at 14,525 mi, 4,300 mi in 7 months']],
       verdict='<b>$34,700 over the $225k cap.</b> Best spec here: MSO Clubsport Pack and a $309,550 sticker. Four owners. McKay was asked Nov 7 for records and best out-the-door.',
       url='https://www.wsmwa.com/used-cars-MCLAREN-600LT-2020-007971-YJZPOBJY'),
 ],
}

def merge_dig(d):
    p = f'{R}/dealer-dig-20261107/RESULTS.json'
    if not os.path.exists(p): return 0
    rows = {r['vin']: r for r in json.load(open(p))}
    for v, m in MANUAL.items(): rows[v] = {**rows.get(v, {'vin': v}), **m}
    n = 0
    for c in d['cars']:
        r = rows.get(c['vin'])
        if not r: continue
        n += 1
        if r.get('dealer_url') and r.get('listing_found'): c['dealerUrl'] = r['dealer_url']
        if r.get('listing_found') and not r.get('still_listed'):
            c['sold'] = 'per dealer site, Nov 7'; c['soldOn'] = '2026-11-07'
        pr = r.get('price_on_dealer_site')
        if pr and r.get('still_listed') and int(pr) != c['price']: c['priceWas'] = c['price']; c['price'] = int(pr)
        if r.get('sticker_url'):
            c['sticker'] = r['sticker_url']
            if not r.get('msrp'): c['stickerLabel'] = 'Dealer spec sheet'
        if r.get('msrp') and not c.get('msrp'):
            c['msrp'] = int(r['msrp']); c['msrpSrc'] = r.get('msrp_source') or 'Dealer site'
        if r.get('carfax_url') and not c.get('carfax'): c['carfax'] = r['carfax_url']
        if r.get('video_url') and not c.get('video'): c['video'] = r['video_url']
        if not c.get('sticker'):
            c['stickerNote'] = 'Dealer site: no sticker' if r.get('listing_found') else 'No live dealer listing'
            c['msrpSrc'] = (c.get('msrpSrc') or '') + (' · ' if c.get('msrpSrc') else '') + (r.get('notes') or 'Checked the dealer site; no sticker posted')
        if r.get('options'): c['opts'] = r['options']
    return n

for i, cap in CAPS.items():
    d = load(i); d['cap'] = cap
    for n in NEW.get(i, []):
        c = dict(n); c.setdefault('pick', False); c['r'] = len(d['cars']) + 1; c['mv'] = 'new'; d['cars'].append(c)
    m = merge_dig(d)
    for c in d['cars']:
        c['pick'] = c['vin'] in PICKS[i]
        v = re.sub(r'^<b>(Pick: |\$[\d,]+ over|At the cap|Under the|Over the cap|Price on request)[^<]*</b>[^<]*?(?=<b>|[A-Z])', '', c['verdict'])
        for a, b in FIX: v = v.replace(a, b)
        o = (c['price'] or 0) - cap['max']
        c['verdict'] = VERDICT_LEAD.get(c['vin'], '').replace('{o}', f'${o:,}') + v
    d['facts'] = TEXT[i]['facts']; d['takeaway'] = TEXT[i]['takeaway']
    # rank: under cap first, then by how far over, grade breaks ties
    for a, b in FIX: d['sources'] = d['sources'].replace(a, b)
    order = sorted(d['cars'], key=lambda c: (bool(c.get('sold')), not c['pick'], c['vin'] in OUT, max(0, (c['price'] or cap['max'] + 1) - cap['max'])))
    for n, c in enumerate(order, 1):
        old = int(c['r'])
        if c.get('mv') == 'new': c['r'] = n; continue
        c['mv'] = 'same' if old == n else (f'up {old-n}' if old > n else f'down {n-old}'); c['r'] = n
    d['cars'] = order
    if i == 'mclaren-720s-spider-2026-11':
        c = car(d, 'SBM14FCA9MW006325')
        c['sticker'] = 'https://s3.amazonaws.com/cdn.autoipacket.com/data/1574/8959/2169454084/msrp/2169454084.20260915.200933-msrp-01.pdf'
        c['msrp'] = 345600; c['msrpSrc'] = 'Original window sticker on Ilusso iPacket: $315,000 base + Performance Plus Pack $6,370, By McLaren Performance $5,840, B&W 12-speaker $4,420, electric memory seats $3,510, 360 park assist $3,100, red calipers $1,720'
        c['video'] = c.get('video') or 'https://www.youtube.com/embed/616CPqfMO5Y'
    d['sources'] = re.sub(r'Window stickers?:[^.]*\.( Chicago Motor Cars says[^.]*\.)?|Window stickers from iPacket where the dealer posted one\.', '', d['sources']).strip() + ' Window stickers and option lists: every dealer site checked VIN by VIN Nov 7 (iPacket, documents, description); a card says "Dealer site: no sticker" only after that check.'
    for c in d['cars']:
        for dealer, a in ASK.items():
            if c['name'].startswith(dealer): c['ask'] = a
    save(i, d); print(i, 'cap', cap['max'], 'picks', [c['name'] for c in d['cars'] if c['pick']], 'dig rows', m)
