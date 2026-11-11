#!/usr/bin/env python3
"""
The parts of the five criteria run_eval.py cannot express.  (Unit 8, M3)

    python run_eval_extra.py --label before

Criterion 4  appeal path: submit, appeal the returned content_id, check the
             status, check /log, and appeal a made-up id.
Criterion 5  the non-JSON body, and that /ping still answers afterwards.

Three trials, results written to results/extra_<stamp>_<label>.md.
"""
import argparse
import datetime as dt
import json

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"
TEXT = ("We got to the campsite about four. The pitch was fine, a bit sloped, "
        "but there was a tap nearby and nobody else for miles. We ate beans "
        "straight from the tin and watched the sky go orange.")


def appeal_trial(trial):
    out = []
    for i in range(1, 6):
        cid = f"eval_appeal_{trial}_{i}"
        r = requests.post(f"{URL}/submit", json={"text": TEXT, "creator_id": cid}, timeout=90)
        sub = r.json() if r.content else {}
        content_id = sub.get("content_id")
        a = requests.post(f"{URL}/appeal", json={"content_id": content_id,
                          "reasoning": "I wrote this myself."}, timeout=30)
        body = a.json() if a.content else {}
        log = requests.get(f"{URL}/log", timeout=30).json()["entries"]
        in_log = any(e.get("content_id") == content_id and e.get("event") == "appeal"
                     for e in log)
        out.append({"submit_status": r.status_code, "content_id": content_id,
                    "appeal_status": a.status_code, "status": body.get("status"),
                    "confirmation": bool(body.get("message")), "in_log": in_log,
                    "passed": a.status_code == 200 and body.get("status") == "under_review"
                    and in_log})
    fake = f"does-not-exist-{trial}"
    f = requests.post(f"{URL}/appeal", json={"content_id": fake, "reasoning": "x"}, timeout=30)
    log = requests.get(f"{URL}/log", timeout=30).json()["entries"]
    wrote_appeal = any(e.get("content_id") == fake and e.get("event") == "appeal" for e in log)
    out.append({"fake_id_status": f.status_code, "wrote_appeal_entry": wrote_appeal,
                "passed": f.status_code == 404 and not wrote_appeal})
    return out


def nonjson_trial():
    r = requests.post(f"{URL}/submit", data="this is not json {{{",
                      headers={"Content-Type": "application/json"}, timeout=30)
    try:
        r.json()
        is_json = True
    except ValueError:
        is_json = False
    ping = requests.post(f"{URL}/ping", json={"message": "hi"}, timeout=10)
    return {"status": r.status_code, "json_error_body": is_json, "ping_status": ping.status_code,
            "passed": 400 <= r.status_code < 500 and is_json and ping.status_code == 200}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="")
    ap.add_argument("--trials", type=int, default=3)
    args = ap.parse_args()
    res = {"criterion_4_appeal": [], "criterion_5_nonjson_and_ping": []}
    for t in range(1, args.trials + 1):
        res["criterion_4_appeal"].append(appeal_trial(t))
        res["criterion_5_nonjson_and_ping"].append(nonjson_trial())
        a = sum(x["passed"] for x in res["criterion_4_appeal"][-1])
        print(f"trial {t}: appeal checks passed {a}/6, "
              f"non-json {res['criterion_5_nonjson_and_ping'][-1]['passed']}")
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"extra_{stamp}{label}.md"
    path.write_text("# Extra eval (criteria 4 and 5)\n\n```json\n"
                    + json.dumps(res, indent=2) + "\n```\n", encoding="utf-8")
    print("wrote", path)


if __name__ == "__main__":
    main()
