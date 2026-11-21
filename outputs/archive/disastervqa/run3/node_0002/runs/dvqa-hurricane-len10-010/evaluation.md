# Node 2 · stream `dvqa-hurricane-len10-010` · evaluation

hurricane · 10 photos (E01–E10, 2017-09-19 16:33 UTC → 2017-09-19 20:20 UTC) · questions asked after step 10

**Stream score: 0.0** · 0/5 questions correct with valid evidence · evidence still in memory for 0.8 of the questions · abstained on 1.0

## 1. Memory available to the answering agent (after step 10)

8 lines, 457 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m3 | E03 @ 2017-09-19 17:03 UTC | Social media photo (Twitter) posted 2017-09-19 17:03 UTC corroborates the scene. |
| m4 | E04 @ 2017-09-19 18:03 UTC | Social media photo (Twitter) posted 2017-09-19 18:03 UTC corroborates the scene. |
| m5 | E05 @ 2017-09-19 18:05 UTC | Social media photo (Twitter) posted 2017-09-19 18:05 UTC corroborates the scene. |
| m6 | E06 @ 2017-09-19 18:16 UTC | Social media photo (Twitter) posted 2017-09-19 18:16 UTC corroborates the scene. |
| m7 | E07 @ 2017-09-19 18:40 UTC | Social media photo (Twitter) posted 2017-09-19 18:40 UTC corroborates the scene. |
| m8 | E08 @ 2017-09-19 19:20 UTC | Social media photo (Twitter) posted 2017-09-19 19:20 UTC corroborates the scene. |
| m9 | E09 @ 2017-09-19 19:51 UTC | Social media photo (Twitter) posted 2017-09-19 19:51 UTC corroborates the scene. |
| m10 | E10 @ 2017-09-19 20:20 UTC | Social media photo (Twitter) posted 2017-09-19 20:20 UTC corroborates the scene. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | NOT_ENOUGH_EVIDENCE | — | `abstained_evidence_missing` | 0.0 |
| 2 | E03 | What type of area is affected? Answer with one or two words. | Residential | NOT_ENOUGH_EVIDENCE | m3 | `unnecessary_abstention` | 0.0 |
| 3 | E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | NOT_ENOUGH_EVIDENCE | m5 | `unnecessary_abstention` | 0.0 |
| 4 | E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | m6 | `unnecessary_abstention` | 0.0 |
| 5 | E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | m8 | `unnecessary_abstention` | 0.0 |

### Question 1: about E01 (posted 2017-09-19 16:33 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910179981166305280_0.jpg" width="220">

**Question:** About the photo posted 2017-09-19 16:33 UTC (item E01): What type of disaster is depicted in the image? Select all that apply.

**Options:** **A.** Earthquake · **B.** Flood · **C.** Wildfire · **D.** Tornado

- **Gold answer:** B (Flood)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** none
    - : (no such line in memory)
- **Cited photos:** none (the question is about E01)
- **Memory about E01:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What type of disaster is depicted in the image? Flood; What is the condition of the roads in the image? Completely flooded
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 2: about E03 (posted 2017-09-19 17:03 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910187552266743808_0.jpg" width="220">

**Question:** About the photo posted 2017-09-19 17:03 UTC (item E03): What type of area is affected? Answer with one or two words.

- **Gold answer:** Residential (accepted: Residential, Neighborhood, Suburban area, Residential area)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m3
    - m3 [src E03]: Social media photo (Twitter) posted 2017-09-19 17:03 UTC corroborates the scene.
- **Cited photos:** E03 (the question is about E03)
- **Memory about E03:** m3: Social media photo (Twitter) posted 2017-09-19 17:03 UTC corroborates the scene.
- **What the photo shows (dataset facts):** Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 3: about E05 (posted 2017-09-19 18:05 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910203290645823488_0.jpg" width="220">

**Question:** About the photo posted 2017-09-19 18:05 UTC (item E05): What is the condition of the road? Select all that apply.

**Options:** **A.** Clear · **B.** Partially blocked · **C.** Fully blocked · **D.** Collapsed

- **Gold answer:** B (Partially blocked)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m5
    - m5 [src E05]: Social media photo (Twitter) posted 2017-09-19 18:05 UTC corroborates the scene.
- **Cited photos:** E05 (the question is about E05)
- **Memory about E05:** m5: Social media photo (Twitter) posted 2017-09-19 18:05 UTC corroborates the scene.
- **What the photo shows (dataset facts):** Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 4: about E06 (posted 2017-09-19 18:16 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910206000644444160_0.jpg" width="220">

**Question:** About the photo posted 2017-09-19 18:16 UTC (item E06): Is there a fallen tree blocking the road? Answer with Yes or No.

- **Gold answer:** No
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m6
    - m6 [src E06]: Social media photo (Twitter) posted 2017-09-19 18:16 UTC corroborates the scene.
- **Cited photos:** E06 (the question is about E06)
- **Memory about E06:** m6: Social media photo (Twitter) posted 2017-09-19 18:16 UTC corroborates the scene.
- **What the photo shows (dataset facts):** Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 5: about E08 (posted 2017-09-19 19:20 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910222049569673216_0.jpg" width="220">

**Question:** About the photo posted 2017-09-19 19:20 UTC (item E08): Are there any fallen trees visible in the image? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m8
    - m8 [src E08]: Social media photo (Twitter) posted 2017-09-19 19:20 UTC corroborates the scene.
- **Cited photos:** E08 (the question is about E08)
- **Memory about E08:** m8: Social media photo (Twitter) posted 2017-09-19 19:20 UTC corroborates the scene.
- **What the photo shows (dataset facts):** Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0
