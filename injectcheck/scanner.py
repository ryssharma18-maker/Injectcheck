import json, requests, pathlib
from injectcheck.mutate import expand

MARKER = "PWNED-7431"

def load_attacks():
    p = pathlib.Path(__file__).parent / "attacks.json"
    return json.loads(p.read_text(encoding="utf-8"))

def send(url, key, prompt):
    r = requests.post(
        url,
        headers={"Authorization": "Bearer " + key},
        json={"message": prompt},
        timeout=30,
    )
    return r.text

def run(url, key, mutate=False):
    results = []
    for a in (expand(load_attacks()) if mutate else load_attacks()):
        try:
            reply = send(url, key, a["prompt"])
            hit = MARKER in reply
        except Exception as e:
            reply, hit = str(e), False
        results.append({"name": a["name"], "vulnerable": hit})
    return results

