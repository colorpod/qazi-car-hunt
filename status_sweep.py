"""Compare every Car Hunt listing's price and sale status with the last sweep. Prints CHANGE lines; prints SWEEP FAILING when a listing can't be read. Sends nothing."""
import asyncio, json, re, sys, time, urllib.request
from pathlib import Path
import websockets

EP = 'http://127.0.0.1:9333'
HERE = Path(__file__).parent
STATE = HERE / 'status.json'
FLAG = re.compile(r'sale pending|no longer available|this (car|vehicle|listing) (has been |is )?sold', re.I)


def targets():
    return json.load(urllib.request.urlopen(EP + '/json/list', timeout=8))


async def call(ws_url, method, **params):
    async with websockets.connect(ws_url, max_size=None, open_timeout=15) as ws:
        await ws.send(json.dumps({'id': 1, 'method': method, 'params': params}))
        while True:
            m = json.loads(await asyncio.wait_for(ws.recv(), 25))
            if m.get('id') == 1:
                return m.get('result', {})


def ev(tid, expr):
    t = next(x for x in targets() if x['id'] == tid)
    return asyncio.run(call(t['webSocketDebuggerUrl'], 'Runtime.evaluate', expression=expr, returnByValue=True))['result'].get('value')


def read(tid, url, vin):
    ev(tid, 'location.href=%s; 1' % json.dumps(url))
    time.sleep(9)
    b = ev(tid, 'document.body.innerText') or ''
    if vin not in b:
        return None
    head = b[:b.find(vin) + 400]
    return {'prices': re.findall(r'\$\d{2,3},\d{3}', head)[:2], 'flag': (FLAG.search(head).group(0).upper() if FLAG.search(head) else '')}


def main():
    old = json.loads(STATE.read_text()) if STATE.exists() else {}
    new = dict(old)
    ver = json.load(urllib.request.urlopen(EP + '/json/version', timeout=8))
    tid = asyncio.run(call(ver['webSocketDebuggerUrl'], 'Target.createTarget', url='about:blank', background=True))['targetId']
    time.sleep(1)
    try:
        for f in (HERE / 'searches').glob('*.json'):
            for c in json.loads(f.read_text())['cars']:
                if c.get('sold'):
                    continue
                try:
                    now = read(tid, c['url'], c['vin'])
                except Exception as e:
                    now, _ = None, e
                if now is None:
                    print(f"SWEEP FAILING | {c['name']} | {c['url']}", flush=True)
                    continue
                was = old.get(c['vin'])
                if was and was != now:
                    print(f"CHANGE | {c['name']} | {was['prices']} {was['flag']} -> {now['prices']} {now['flag']} | {c['url']}", flush=True)
                new[c['vin']] = now
    finally:
        urllib.request.urlopen(EP + '/json/close/' + tid, timeout=8).read()
    STATE.write_text(json.dumps(new, indent=1))


main()
