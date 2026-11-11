# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 11:09
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `f9fc4ac58a56` | unsure | 0.440 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `2b749a833d16` | unsure | 0.448 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `42f9bd5f4cf6` | unsure | 0.526 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `edfd30f6e922` | unsure | 0.590 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `a8bd982c0abe` | human | 0.297 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `f5e0f8072e75` | unsure | 0.492 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `a03c2e23413f` | unsure | 0.502 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `6e78ba2f0078` | unsure | 0.428 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6a31ea3208d8` | unsure | 0.553 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `91433dd2cee3` | ai | 0.925 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `34015391b5c6` | unsure | 0.640 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `a282b0264553` | ai | 0.767 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `a3f517bf7fa9` | ai | 0.764 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d2a239cfbd45` | unsure | 0.717 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `db4e567ffb48` | ai | 0.844 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `f2189da65560` | unsure | 0.732 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `f8029b0f65c5` | ai | 0.756 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `e8165af388f0` | unsure | 0.417 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `ccd1ace20a3d` | unsure | 0.410 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `81e0d0ba1d1a` | human | 0.254 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a92a1157eb05` | unsure | 0.538 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `d67bc611151e` | unsure | 0.443 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `38ef85ff1540` | unsure | 0.448 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `cf27d3d71b44` | unsure | 0.597 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `b62dbbf0d5ae` | unsure | 0.417 |  |
| MF04 | malformed | text is only punctuation | 200 | `7d6ca402b082` | unsure | 0.503 |  |
| MF05 | malformed | text is a very long single word | 200 | `af56e9a9095b` | ai | 0.832 |  |
| MF06 | malformed | text is emoji only | 200 | `63092ba3e017` | ai | 0.999 |  |
| MF07 | malformed | text is right-to-left script | 200 | `9215e99eecbf` | ai | 0.953 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `25beb2bfee29` | unsure | 0.424 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `629fb5d804c3` | unsure | 0.424 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9224600eafb8` | unsure | 0.424 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `514b034dc125` | unsure | 0.424 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `062b26d0fcf5` | unsure | 0.424 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "f9fc4ac58a56",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4402,
  "model_score": 0.1635,
  "style_score": 0.5973,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "2b749a833d16",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4475,
  "model_score": 0.5943,
  "style_score": 0.3006,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "42f9bd5f4cf6",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5263,
  "model_score": 0.6662,
  "style_score": 0.3864,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "edfd30f6e922",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5901,
  "model_score": 0.6114,
  "style_score": 0.5689,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "a8bd982c0abe",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2971,
  "model_score": 0.3212,
  "style_score": 0.273,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "f5e0f8072e75",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4924,
  "model_score": 0.5727,
  "style_score": 0.4121,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "a03c2e23413f",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5025,
  "model_score": 0.5862,
  "style_score": 0.4187,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "6e78ba2f0078",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4283,
  "model_score": 0.2452,
  "style_score": 0.6114,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "6a31ea3208d8",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5526,
  "model_score": 0.7042,
  "style_score": 0.401,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "91433dd2cee3",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9249,
  "model_score": 0.9792,
  "style_score": 0.8707,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "34015391b5c6",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6396,
  "model_score": 0.6175,
  "style_score": 0.6617,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "a282b0264553",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7667,
  "model_score": 0.7387,
  "style_score": 0.7947,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "a3f517bf7fa9",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7638,
  "model_score": 0.8051,
  "style_score": 0.7224,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "d2a239cfbd45",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7171,
  "model_score": 0.8329,
  "style_score": 0.6013,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "db4e567ffb48",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8438,
  "model_score": 0.8005,
  "style_score": 0.8871,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "f2189da65560",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7319,
  "model_score": 0.8814,
  "style_score": 0.5824,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f8029b0f65c5",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7563,
  "model_score": 0.8816,
  "style_score": 0.631,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "e8165af388f0",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4168,
  "model_score": 0.3223,
  "style_score": 0.5113,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "ccd1ace20a3d",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4103,
  "model_score": 0.4625,
  "style_score": 0.3582,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "81e0d0ba1d1a",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2536,
  "model_score": 0.2044,
  "style_score": 0.3028,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a92a1157eb05",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5385,
  "model_score": 0.5943,
  "style_score": 0.4827,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "d67bc611151e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4427,
  "model_score": 0.4998,
  "style_score": 0.3857,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "38ef85ff1540",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4481,
  "model_score": 0.6401,
  "style_score": 0.1524,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "cf27d3d71b44",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5974,
  "model_score": 0.5583,
  "style_score": 0.6364,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "b62dbbf0d5ae",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.4167,
  "model_score": 0.0,
  "style_score": 0.6667,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "7d6ca402b082",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5028,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "af56e9a9095b",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8321,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "63092ba3e017",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "9215e99eecbf",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this may have been written with the help of an AI tool. We can be wrong, so if you wrote it yourself, please appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "25beb2bfee29",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4238,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "629fb5d804c3",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4238,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "9224600eafb8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4238,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "514b034dc125",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4238,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "062b26d0fcf5",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4238,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "We can't tell for sure how this was written. Our checks gave mixed results, and that is not a judgment about you. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
