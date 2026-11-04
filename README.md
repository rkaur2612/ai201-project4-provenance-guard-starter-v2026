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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
