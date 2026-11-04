# Acceptance Criteria

Written before any results were seen.

## 1. Area: False positives

**Target:** Of 10 pieces of plain, ordinary human writing (including 3 written in simple, second-language-style English), at most 1 is labeled high-confidence AI.

**Reason:** Calling a real writer an AI is the costly error, and plain writing is exactly what the model signal mistakes for machine text. The test set has to include that writing or the target is too easy.

## 2. Area: Score spread

**Target:** The average combined score of 5 clearly-AI texts is at least 0.30 higher than the average of 5 clearly-human texts.

**Reason:** If the two groups score close together, the system can't tell them apart and the labels are noise. 0.30 is wide enough that the unsure band can't swallow both groups.

## 3. Area: Label coverage

**Target:** Across a set of at least 12 varied inputs, all three labels (human, unsure, AI) each appear at least once, and no input returns a label outside those three.

**Reason:** A label no score can reach means a gap in the ranges or a signal that never moves. This is how I find out.

## 4. Area: Appeal path

**Target:** For 5 appeals on real content_ids, 5 of 5 return a confirmation, 5 of 5 set status to `under_review`, and 5 of 5 appear in `GET /log` after the original decision. An appeal on a made-up content_id returns 404 and writes nothing as an appeal.

**Reason:** An appeal is the only recourse a wrongly-accused writer has, so it must never fail silently.

## 5. Area: Bad input

**Target:** Missing `text`, empty `text`, whitespace-only `text`, non-string `text`, a non-JSON body, and a 200,000-character text each return a 4xx JSON error (never a 500 or crash), and `/ping` still answers afterwards.

**Reason:** A crash on malformed input is one of the most common real failures, and a service that dies on bad input is a service anyone can knock over.
