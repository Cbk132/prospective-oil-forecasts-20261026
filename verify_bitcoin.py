"""Check each Bitcoin attestation against the block header from a public explorer (Blockstream API).

An OpenTimestamps Bitcoin attestation commits to the block's merkle root in internal byte order,
i.e. the reverse of the hex shown by explorers.
"""
from pathlib import Path
import datetime
import json
import urllib.request

HERE = Path(__file__).resolve().parent
check = json.loads((HERE / 'timestamps' / 'proof_structure_check.json').read_text(encoding='utf-8'))
API = 'https://blockstream.info/api'


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ots-verify'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode()


out = dict(sha256=check['sha256'], source=API, checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), proofs={})
for name, atts in check['proofs'].items():
    for att in atts:
        if att['kind'] != 'bitcoin':
            continue
        height = att['detail']
        block_hash = get(f'{API}/block-height/{height}').strip()
        block = json.loads(get(f'{API}/block/{block_hash}'))
        root_internal = bytes.fromhex(block['merkle_root'])[::-1].hex()
        out['proofs'][name] = dict(height=height, block_hash=block_hash,
                                   block_time_utc=datetime.datetime.fromtimestamp(block['timestamp'], datetime.timezone.utc).isoformat(),
                                   commitment=att['commitment'], merkle_root_internal=root_internal,
                                   verified=root_internal == att['commitment'])
(HERE / 'timestamps' / 'bitcoin_verification.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, indent=2))
