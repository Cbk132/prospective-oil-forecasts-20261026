"""Upgrade the pending .ots proofs once the calendars have anchored them in Bitcoin (usually a few hours).

For each proof, ask its calendar for the completed timestamp of the pending commitment and splice the
reply in place of the trailing pending attestation. Original files are kept as *.pending.ots.
Run again later if a calendar still answers 404 (not yet anchored).
"""
from pathlib import Path
import json
import shutil
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
check = json.loads((HERE / 'timestamps' / 'proof_structure_check.json').read_text(encoding='utf-8'))
PENDING = bytes.fromhex('83dfe30d2ef90c8e')

for name, atts in check['proofs'].items():
    path = HERE / 'timestamps' / name
    data = path.read_bytes()
    pending = [a for a in atts if a['kind'] == 'pending']
    if len(pending) != 1 or len(atts) != 1:
        print(name, 'already upgraded or not a single pending path; skipped')
        continue
    att = pending[0]
    url = f"{att['detail']}/timestamp/{att['commitment']}"
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/vnd.opentimestamps.v1', 'User-Agent': 'python-opentimestamps'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
    except urllib.error.HTTPError as exc:
        print(name, 'not anchored yet' if exc.code == 404 else exc)
        continue
    uri = att['detail'].encode()
    payload = bytes([len(uri)]) + uri
    tail = b'\x00' + PENDING + bytes([len(payload)]) + payload
    assert data.endswith(tail), 'unexpected proof layout'
    shutil.copy2(path, path.with_suffix('.pending.ots'))
    path.write_bytes(data[:-len(tail)] + body)
    print(name, 'upgraded with calendar reply of', len(body), 'bytes')
print('Re-run ots_check.py to confirm a bitcoin attestation (block height) is now present.')
