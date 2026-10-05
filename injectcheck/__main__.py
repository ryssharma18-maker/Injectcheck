import argparse, json
from injectcheck.scanner import run

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
END = "\033[0m"

def main():
    p = argparse.ArgumentParser(prog="injectcheck")
    p.add_argument("--url", required=True)
    p.add_argument("--key", default="")
    p.add_argument("--mutate", action="store_true")
    p.add_argument("--report", default="")
    p.add_argument("--provider", default="custom")
    p.add_argument("--model", default="")
    a = p.parse_args()

    results = run(a.url, a.key, a.mutate, a.provider, a.model)
    if a.report:
        open(a.report, "w").write(json.dumps(results, indent=2))

    bad = errs = 0
    for r in results:
        if r["error"]:
            errs += 1
            print(YELLOW + "ERROR       " + r["name"] + END)
        elif r["vulnerable"]:
            bad += 1
            print(RED + "VULNERABLE  " + r["name"] + END)
        else:
            print(GREEN + "safe        " + r["name"] + END)

    print()
    print(str(bad) + " of " + str(len(results)) + " attacks got through, " + str(errs) + " errors")
    if errs:
        first = [r["error"] for r in results if r["error"]][0]
        print(YELLOW + "Scan incomplete. First error: " + first + END)
    raise SystemExit(2 if errs else (1 if bad else 0))

if __name__ == "__main__":
    main()
