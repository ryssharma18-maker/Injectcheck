import argparse, json
from injectcheck.scanner import run

GREEN = "\033[92m"
RED = "\033[91m"
END = "\033[0m"

def main():
    p = argparse.ArgumentParser(prog="injectcheck")
    p.add_argument("--url", required=True)
    p.add_argument("--key", default="")
    p.add_argument("--mutate", action="store_true")
    p.add_argument("--report", default="")
    a = p.parse_args()

    results = run(a.url, a.key, a.mutate)
    if a.report:
        open(a.report, "w").write(json.dumps(results, indent=2))
    bad = 0
    for r in results:
        if r["vulnerable"]:
            bad += 1
            print(RED + "VULNERABLE  " + r["name"] + END)
        else:
            print(GREEN + "safe        " + r["name"] + END)

    print()
    print(str(bad) + " of " + str(len(results)) + " attacks got through")
    raise SystemExit(1 if bad else 0)

if __name__ == "__main__":
    main()


