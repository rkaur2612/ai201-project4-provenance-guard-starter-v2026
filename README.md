# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a small local web service. A writing site sends it text and gets back a guess (AI, human or unsure), a confidence score from 0 to 1, a plain-English label and a way for the writer to appeal. Nothing calls a hosted service; the model runs on the laptop.

1. **Arrival.** `POST /submit` receives `{text, creator_id}` in `app.py::submit`.
2. **Validation.** Missing, empty, non-string, too-short or over-20,000-character text gets a JSON 4xx error and a `rejected` audit entry, never a crash.
3. **Signal one.** `detector.model_signal` scores how predictable the text is to GPT-2 (0 to 1, higher = more AI-like).
4. **Signal two.** `stylometry.style_signal` scores the shape of the text: sentence-length spread, vocabulary variety and punctuation (0 to 1, higher = more AI-like).
5. **Combining.** `scoring.combine_signals` merges the two into one confidence score.
6. **Label.** `scoring.score_to_label` maps the score to one of three labels.
7. **Logging and reply.** `audit.log_decision` writes both signal scores, the combined score, the label and status `decided` to `logs/audit.jsonl`, and the response carries the same plus a `content_id`. `POST /appeal` takes that `content_id`, moves the item to `under_review` and logs the writer's reasoning next to the original decision.

**Endpoint contract.**

| Endpoint | In | Out |
|---|---|---|
| `POST /submit` | `{"text": str, "creator_id": str}` | `{content_id, guess ("ai"/"human"/"unsure"), confidence (0-1), label, model_score, style_score, status}` |
| `POST /appeal` | `{"content_id": str, "reasoning": str}` | `{content_id, status: "under_review", message}`; 404 for an unknown `content_id` |



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2 (perplexity), squashed onto 0-1 in `detector.py::model_signal`.

**Why that might differ between human and AI writing:** A language model writes the most likely next word, so its output is easy for another model to predict. People reach for unexpected words more often.

**What it can't see:** Authorship. It rewards common words in short, ordinary sentences, so plain human writing (a second-language writer, a younger writer, anyone writing simply) scores as machine-like. That is a structural false positive, not a bug.

### Signal two — the style signal

**What it measures:** The shape of the text, in `stylometry.py::style_signal`: sentence-length spread (stdev/mean), type-token ratio on the first 100 words, and punctuation density (commas, semicolons, colons, dashes, brackets, quotes per word). Each is scaled to 0-1 and the three are averaged equally.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences, narrower vocabulary and tidy punctuation. Human writing is lumpier.

**What it can't see:** Meaning. It cannot read, so anything that changes shape without changing substance moves it: typos, broken-up sentences, a pasted quotation. That is cheap to do on purpose.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average of the two scores, plus a disagreement rule: if the signals are far apart, the average is pulled halfway back toward 0.5. Two methods disagreeing is itself uncertainty, so neither signal alone can produce an accusation.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`, `DISAGREE_GAP = 0.4`, `DISAGREE_SHRINK = 0.5`, `HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.75`, all in `config.py`. I set the AI threshold higher than the human one's mirror image (0.75, not 0.65) on purpose: a false accusation costs more than a missed AI text.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A casual, punchy human paragraph ("Honestly? I hated my first job...") scored `model_score` 0.7041 (short common words read as predictable) but `style_score` 0.038 (very lumpy sentences, lots of punctuation). The plain average is 0.371; the gap of 0.666 exceeds 0.4, so the rule pulls it to 0.4355, which is "unsure" instead of leaning either way.

**Known weak spot (found while testing):** A plain, simple human paragraph ("I like my town. It is small and quiet...") scored model 0.8588 and style 0.645, combined 0.7519, and was labeled AI. Both signals agree there, so the disagreement rule cannot help. This is the false positive described above and is what unit 8 should probe.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.75 | We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look. |
| high-confidence AI | 0.75 – 1.00 | We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it. |

**Why I worded the "unsure" one this way:**

The person reading it may well have written every word themselves, so it says plainly that the result is not a judgment about them and points to the appeal. The AI label says "may have been" and invites an appeal for the same reason.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Honestly? I hated my first job. The coffee was awful, my boss kept calling me '"'"'kiddo'"'"', and the bus -- don'"'"'t get me started on the bus -- never came on time. But I learned to laugh at it. Mostly.", "creator_id": "tester"}'
```

```json
{
  "content_id": "8d5443bba007",
  "guess": "unsure",
  "confidence": 0.4355,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "model_score": 0.7041,
  "style_score": 0.038,
  "status": "decided"
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "8d5443bba007", "reasoning": "I wrote it."}'
```

```json
{
  "content_id": "8d5443bba007",
  "message": "Thank you. Your appeal has been recorded and a person will review it.",
  "status": "under_review"
}
```

An appeal on an unknown id returns `404 {"error": "unknown_content_id", ...}` and logs a rejection.

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{"timestamp": "2026-11-04T21:33:12+00:00", "content_id": "8d5443bba007", "creator_id": "tester", "guess": "unsure", "model_score": 0.7041, "style_score": 0.038, "combined_score": 0.4355, "label": "We can't tell for sure how this was written. ...", "status": "decided"}
{"timestamp": "2026-11-04T21:33:12+00:00", "content_id": "8d5443bba007", "creator_id": "tester", "event": "appeal", "status": "under_review", "reasoning": "I wrote it."}
```

(Entries copied from `logs/audit.jsonl`; the label is shortened here.)

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude Code to read the brief and RUNNING.md and help me finish the unit 7 build quickly.
- *What came back:* Working `/submit` and `/appeal` routes, the style signal, a combining rule with a disagreement shrink, three labels, and draft acceptance criteria.
- *What I changed:* I reviewed the criteria targets and kept the commit order (criteria first) so the history shows they predate the results.

**Moment 2**

- *What I asked for:* I asked Claude Code to run four calibration texts and the bad-input cases through the app.
- *What came back:* A plain human paragraph was labeled AI at 0.7519, which is the false positive this project is about.
- *What I changed:* The AI threshold went from 0.65 to 0.75 so doubtful cases land in "unsure", and I recorded the case as a known weak spot instead of hiding it.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 100 per day

**Why those numbers and not others:** A real writer submits a few pieces an hour, so 5 a minute leaves room for a quick resubmit or two and 100 a day is far more than any one person writes. A script mapping my thresholds needs hundreds of probes with small edits; 100 a day turns that into several days of work per creator_id, and 5 a minute stops a burst. I did not go lower because a writer who hits a limit while revising is being punished for doing nothing wrong.

**What a caller counts as:** The `creator_id` in the request body, falling back to the caller's address when it is missing or unusable (`rate_limit_key` in `app.py`). The weakness: a script can rotate `creator_id` values to dodge the limit, and the attack set's per-row creator ids will not trip it. Limiting by address would stop that but would lump a household or campus together.

**The run of status codes when I pushed past it:**

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

(`python run_attacks.py --flood 15`; 10 of 15 limited. Rejections are written to `logs/audit.jsonl` with `reason: rate_limited`. Full output in `results/flood_2026-11-11_1102.md`.)

---

## Attack Run — Before

Full per-attack JSON: `results/attack_run_2026-11-11_1109_before.md`. Limits at the time: 5/min, 100/day.

**Marking rule.** Evasion: BROKE if AI-written text did not get the `ai` label (partial = `unsure`, full = `human`). False positive: BROKE if human writing got `ai`. Prompt injection: BROKE if the instruction changed the outcome or the log. Malformed: BROKE if 5xx, crash, or a confident verdict on non-prose.

| ID | Attack | Model / Style / Score | Label | Verdict |
|---|---|---|---|---|
| EV01 | typos added to AI text | 0.16 / 0.60 / 0.440 | unsure | BROKE (partial) |
| EV02 | broken-up sentences | 0.59 / 0.30 / 0.448 | unsure | BROKE (partial) |
| EV03 | pasted quotation | 0.67 / 0.39 / 0.526 | unsure | BROKE (partial) |
| EV04 | unusual words | 0.61 / 0.57 / 0.590 | unsure | BROKE (partial) |
| EV05 | heavy human edit | 0.32 / 0.27 / 0.297 | human | BROKE (full), arguably fair: text is mostly human now |
| EV06 | one very long + one very short sentence | 0.57 / 0.41 / 0.492 | unsure | BROKE (partial) |
| EV07 | punctuation padding | 0.59 / 0.42 / 0.503 | unsure | BROKE (partial) |
| EV08 | text below token window | 0.25 / 0.61 / 0.428 | unsure | BROKE (partial) |
| EV09 | human opening bolted on | 0.70 / 0.40 / 0.553 | unsure | BROKE (partial) |
| EV10 | repeated stanza structure | 0.98 / 0.87 / 0.925 | ai | HELD |
| FP01 | plain human writing | 0.62 / 0.66 / 0.640 | unsure | HELD |
| FP02 | formal human register | 0.74 / 0.79 / 0.767 | ai | BROKE |
| FP03 | non-native speaker | 0.81 / 0.72 / 0.764 | ai | BROKE |
| FP04 | rubric student essay | 0.83 / 0.60 / 0.717 | unsure | HELD |
| FP05 | human technical docs | 0.80 / 0.89 / 0.844 | ai | BROKE |
| FP06 | formal letter template | 0.88 / 0.58 / 0.732 | unsure | HELD |
| FP07 | deliberate repetition | 0.88 / 0.63 / 0.756 | ai | BROKE |
| FP08 | very short human text | 0.32 / 0.51 / 0.417 | unsure | HELD |
| PI01 | "ignore all previous instructions" | 0.46 / 0.36 / 0.410 | unsure | HELD |
| PI02 | fake SYSTEM message | 0.20 / 0.30 / 0.254 | human | HELD (score came from the text statistics, not obeying the instruction; the injected prose just reads as human to both signals) |
| PI03 | note to the reviewing system | 0.59 / 0.48 / 0.539 | unsure | HELD |
| PI04 | HTML/script in text | 0.50 / 0.39 / 0.443 | unsure | HELD (label is a fixed string; response is JSON) |
| PI05 | fake JSON in text to poison the log | 0.64 / 0.15 / 0.448 | unsure | HELD (log line is `json.dumps` of my own fields; the text is never logged) |
| PI06 | instruction + real human text | 0.56 / 0.64 / 0.597 | unsure | HELD |
| MF01 | whitespace only | n/a | 400 | HELD |
| MF02 | single character | n/a | 422 | HELD |
| MF03 | control characters | 0.00 / 0.67 / 0.417 | unsure | HELD |
| MF04 | punctuation only | 0.01 / 1.00 / 0.503 | unsure | HELD |
| MF05 | 4,000-char single word | 1.00 / 0.67 / 0.832 | ai | BROKE (confident verdict on non-prose) |
| MF06 | emoji only | 1.00 / 1.00 / 0.999 | ai | BROKE (confident verdict on non-prose) |
| MF07 | right-to-left script | 0.95 / ? / 0.953 | ai | BROKE (confident verdict on text the signals can't read) |
| MF08 | 60,000 chars | n/a | 413 | HELD |
| RQ01-RQ09, RQ12 | missing/non-string fields, bad JSON, array body, empty body, nested JSON | n/a | 400 | HELD (no 5xx) |
| RQ10, RQ11 | form-encoded body; JSON sent as text/plain | n/a | 429 in the run | INCONCLUSIVE in the run, then HELD: the sender's address had already used its 5/min on earlier malformed rows, so they never reached my route. Re-sent after the window they each returned 400 |
| FL01_01-05 | 12 rapid submissions, one creator | 0.03 / 0.67 / 0.424 | unsure | HELD (allowed) |
| FL01_06-12 | same creator, over the limit | n/a | 429 | HELD (7 rejected, logged) |

**Count:** 10 evasion (9 BROKE, 1 HELD), 8 false positives (4 BROKE), 6 injection (0 BROKE), 8 MF (3 BROKE), 12 RQ (0 BROKE, 2 inconclusive in-run), 12 flood (0 BROKE). Total BROKE: 16 of 56. No 5xx and no crash.

**Ten audit log entries from the run** (12 shown: ten decisions, then a rate-limit rejection and a route rejection; also in `results/audit_extract_before.jsonl`; the `label` text is truncated here for width)

```json
{"timestamp": "2026-11-11T19:08:45+00:00", "content_id": "a3f517bf7fa9", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7224, "combined_score": 0.7638, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:08:49+00:00", "content_id": "db4e567ffb48", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.8871, "combined_score": 0.8438, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:08:44+00:00", "content_id": "a282b0264553", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.7947, "combined_score": 0.7667, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:08:56+00:00", "content_id": "f8029b0f65c5", "creator_id": "attacker_FP07", "guess": "ai", "model_score": 0.8816, "style_score": 0.631, "combined_score": 0.7563, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:08:24+00:00", "content_id": "f9fc4ac58a56", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.5973, "combined_score": 0.4402, "label": "We can't tell for sure how this was writ...", "status": "decided"}
{"timestamp": "2026-11-11T19:09:23+00:00", "content_id": "63092ba3e017", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.9985, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:09:19+00:00", "content_id": "af56e9a9095b", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6667, "combined_score": 0.8321, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:08:35+00:00", "content_id": "6a31ea3208d8", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.401, "combined_score": 0.5526, "label": "We can't tell for sure how this was writ...", "status": "decided"}
{"timestamp": "2026-11-11T19:08:36+00:00", "content_id": "91433dd2cee3", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.8707, "combined_score": 0.9249, "label": "We think this may have been written with...", "status": "decided"}
{"timestamp": "2026-11-11T19:09:03+00:00", "content_id": "81e0d0ba1d1a", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3028, "combined_score": 0.2536, "label": "We think this was probably written by a ...", "status": "decided"}
{"timestamp": "2026-11-11T19:09:40+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-11T19:09:11+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "bad_text"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it: FP03. A person describing their first month in a new country, writing carefully in simple English, got the `ai` label at 0.764 (model 0.81, style 0.72). Both signals read careful, plain, second-language prose as machine-like, so they agree and my disagreement rule does nothing. The writer can appeal, but the first thing they see is an accusation.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
