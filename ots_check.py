"""Parse each detached .ots proof (stdlib only): check the header and digest, replay the ops, and list attestations."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
MAGIC = b'\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94'
PENDING = bytes.fromhex('83dfe30d2ef90c8e')
BITCOIN = bytes.fromhex('0588960d73d71901')


class Reader:
    def __init__(self, data):
        self.d, self.i = data, 0

    def byte(self):
        b = self.d[self.i]; self.i += 1; return b

    def take(self, n):
        b = self.d[self.i:self.i + n]; self.i += n; return b

    def varuint(self):
        v, shift = 0, 0
        while True:
            b = self.byte(); v |= (b & 0x7f) << shift; shift += 7
            if not b & 0x80:
                return v

    def varbytes(self):
        return self.take(self.varuint())


def walk(r, msg, found):
    """Deserialize one timestamp node applied to msg; append (kind, commitment, detail) to found."""
    tag = r.byte()
    while tag == 0xff:
        step(r, r.byte(), msg, found)
        tag = r.byte()
    step(r, tag, msg, found)


def step(r, tag, msg, found):
    if tag == 0x00:
        att_tag = r.take(8); payload = Reader(r.varbytes())
        if att_tag == PENDING:
            found.append(('pending', msg.hex(), payload.varbytes().decode()))
        elif att_tag == BITCOIN:
            found.append(('bitcoin', msg.hex(), payload.varuint()))
        else:
            found.append(('unknown', msg.hex(), att_tag.hex()))
        return
    if tag == 0xf0:
        msg = msg + r.varbytes()
    elif tag == 0xf1:
        msg = r.varbytes() + msg
    elif tag == 0x08:
        msg = hashlib.sha256(msg).digest()
    else:
        raise ValueError(f'unsupported op 0x{tag:02x}')
    walk(r, msg, found)


digest = hashlib.sha256((HERE / 'SHA256SUMS.txt').read_bytes()).digest()
report = {}
for p in sorted((HERE / 'timestamps').glob('*.ots')):
    r = Reader(p.read_bytes())
    assert r.take(len(MAGIC)) == MAGIC and r.varuint() == 1 and r.byte() == 0x08
    assert r.take(32) == digest, 'digest mismatch'
    found = []
    walk(r, digest, found)
    assert r.i == len(r.d), 'trailing bytes'
    report[p.name] = [dict(kind=k, commitment=c, detail=d) for k, c, d in found]
(HERE / 'timestamps' / 'proof_structure_check.json').write_text(json.dumps(dict(sha256=digest.hex(), proofs=report), indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
