# Node 3 · stream `dvqa-wildfire-len10-064` · evaluation

wildfire · 10 photos (E01–E10, 2017-10-12 03:11 UTC → 2017-10-20 11:11 UTC) · questions asked after step 10

**Stream score: 0.2** · 1/5 questions correct with valid evidence · evidence still in memory for 0.2 of the questions · abstained on 0.2

## 1. Memory available to the answering agent (after step 10)

5 lines, 460 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m3 | E03 @ 2017-10-12 03:22 UTC | Social media photo from Twitter, timestamp 2017-10-12 03:22 UTC, depicting active wildfire with visible flames and smoke. Two individuals in casual attire standing at a distance, observing the fire. Environment includes charred vegetation and embers. Location details unspecified. |
| m4 | E04 @ 2017-10-12 08:25 UTC | Social media photo from Twitter, timestamp 2017-10-12 08:25 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards the fire. Environment includes charred vegetation and embers. Location details unspecified. |
| m5 | E05 @ 2017-10-17 16:04 UTC | Social media photo from Twitter, timestamp 2017-10-17 16:04 UTC, depicting a fire truck with all emergency lights activated, positioned near a wildfire. The truck's headlights and roof lights are on, illuminating the area. The background shows a mountain partially obscured by smoke, with trees and vegetation visible around the vehicle. Location details unspecified. |
| m6 | E08 @ 2017-10-19 07:36 UTC | Social media photo from Twitter, timestamp 2017-10-19 07:36 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified. |
| m7 | E10 @ 2017-10-20 11:11 UTC | Social media photo from Twitter, timestamp 2017-10-20 11:11 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E01 | How many people are visible in the image? Select all that apply. | C (Two) | C (Two) | m3 | `invalid_citation` | 0.0 |
| 2 | E06 | What is the primary material burning? Answer with one or two words. | Trees | NOT_ENOUGH_EVIDENCE | — | `abstained_evidence_missing` | 0.0 |
| 3 | E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | m4, m6, m7 | `invalid_citation` | 0.0 |
| 4 | E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | m6, m7 | `invalid_citation` | 0.0 |
| 5 | E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | Yes | m7 | `correct` | 1.0 |

### Question 1: about E01 (posted 2017-10-12 03:11 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918313136654049281_0.jpg" width="220">

**Question:** About the photo posted 2017-10-12 03:11 UTC (item E01): How many people are visible in the image? Select all that apply.

**Options:** **A.** None · **B.** One · **C.** Two · **D.** Three

- **Gold answer:** C (Two)
- **Agent's answer:** C (Two)  (raw: `C`)
- **Cited memory lines:** m3
    - m3 [src E03]: Social media photo from Twitter, timestamp 2017-10-12 03:22 UTC, depicting active wildfire with visible flames and smoke. Two individuals in casual attire standing at a distance, observing the fire. Environment includes charred vegetation and embers. Location details unspecified.
- **Cited photos:** E03 (the question is about E01)
- **Memory about E01:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
- **Checks:** answer correctness 1.0 (exact); citation invalid
- **Outcome:** `invalid_citation`: correct answer, but it did not cite the question's photo
- **Score:** 0.0

### Question 2: about E06 (posted 2017-10-18 07:23 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920550861343948800_0.jpg" width="220">

**Question:** About the photo posted 2017-10-18 07:23 UTC (item E06): What is the primary material burning? Answer with one or two words.

- **Gold answer:** Trees (accepted: Trees, Vegetation)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** none
    - : (no such line in memory)
- **Cited photos:** none (the question is about E06)
- **Memory about E06:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 3: about E07 (posted 2017-10-18 20:21 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920746714637721600_0.jpg" width="220">

**Question:** About the photo posted 2017-10-18 20:21 UTC (item E07): What type of disaster is depicted in the image? Select all that apply.

**Options:** **A.** Flood · **B.** Fire · **C.** Earthquake · **D.** Tornado

- **Gold answer:** B (Fire)
- **Agent's answer:** B (Fire)  (raw: `B`)
- **Cited memory lines:** m4, m6, m7
    - m4 [src E04]: Social media photo from Twitter, timestamp 2017-10-12 08:25 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards the fire. Environment includes charred vegetation and embers. Location details unspecified.
    - m6 [src E08]: Social media photo from Twitter, timestamp 2017-10-19 07:36 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
    - m7 [src E10]: Social media photo from Twitter, timestamp 2017-10-20 11:11 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
- **Cited photos:** E04, E08, E10 (the question is about E07)
- **Memory about E07:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** What type of disaster is depicted in the image? Fire
- **Checks:** answer correctness 1.0 (exact); citation invalid
- **Outcome:** `invalid_citation`: correct answer, but it did not cite the question's photo
- **Score:** 0.0

### Question 4: about E09 (posted 2017-10-19 07:36 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920916661519007745_3.jpg" width="220">

**Question:** About the photo posted 2017-10-19 07:36 UTC (item E09): Are these people watching fireworks? Answer with Yes or No.

- **Gold answer:** No
- **Agent's answer:** No  (raw: `No`)
- **Cited memory lines:** m6, m7
    - m6 [src E08]: Social media photo from Twitter, timestamp 2017-10-19 07:36 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
    - m7 [src E10]: Social media photo from Twitter, timestamp 2017-10-20 11:11 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
- **Cited photos:** E08, E10 (the question is about E09)
- **Memory about E09:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
- **Checks:** answer correctness 1.0 (exact); citation invalid
- **Outcome:** `invalid_citation`: correct answer, but it did not cite the question's photo
- **Score:** 0.0

### Question 5: about E10 (posted 2017-10-20 11:11 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/921332920840843265_0.jpg" width="220">

**Question:** About the photo posted 2017-10-20 11:11 UTC (item E10): Are there any emergency responders present? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** Yes  (raw: `Yes`)
- **Cited memory lines:** m7
    - m7 [src E10]: Social media photo from Twitter, timestamp 2017-10-20 11:11 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
- **Cited photos:** E10 (the question is about E10)
- **Memory about E10:** m7: Social media photo from Twitter, timestamp 2017-10-20 11:11 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
- **What the photo shows (dataset facts):** Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence supported (The image shows emergency responders and a fire, which supports the answer.)
- **Outcome:** `correct`: correct, cited the right photo, evidence supports it
- **Score:** 1.0
