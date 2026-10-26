"""Submit the SHA-256 of SHA256SUMS.txt to public OpenTimestamps calendars (no account needed).

Only the 32-byte digest leaves this machine. Each calendar's reply is saved as a standard detached
.ots proof (header, SHA-256 file-hash op, digest, calendar timestamp), which the official client can
later upgrade and verify against the Bitcoin blockchain: `ots upgrade` / `ots verify`.
"""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

HERE = Path(__file__).resolve().parent
TARGET = HERE / 'SHA256SUMS.txt'
CALENDARS = ['https://a.pool.opentimestamps.org', 'https://b.pool.opentimestamps.org',
             'https://a.pool.eternitywall.com', 'https://ots.btc.catallaxy.com']
MAGIC = b'\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94'

digest = hashlib.sha256(TARGET.read_bytes()).digest()
out = HERE / 'timestamps'
out.mkdir(exist_ok=True)
log = dict(file=TARGET.name, sha256=digest.hex(), submitted_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), calendars={})
for url in CALENDARS:
    req = urllib.request.Request(url + '/digest', data=digest, method='POST',
                                 headers={'Accept': 'application/vnd.opentimestamps.v1', 'User-Agent': 'python-opentimestamps'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
        name = url.split('//')[1].replace('.', '_') + '.ots'
        (out / name).write_bytes(MAGIC + b'\x01' + b'\x08' + digest + body)
        log['calendars'][url] = dict(status='ok', response_bytes=len(body), proof=f'timestamps/{name}')
    except Exception as exc:
        log['calendars'][url] = dict(status='failed', error=repr(exc))
(HERE / 'timestamps' / 'submission_log.json').write_text(json.dumps(log, indent=2) + '\n', encoding='utf-8')
print(json.dumps(log, indent=2))
