# Node 18 · stream `dvqa-wildfire-len10-064` · evaluation

wildfire · 10 photos (E01–E10, 2017-10-12 03:11 UTC → 2017-10-20 11:11 UTC) · questions asked after step 10

**Stream score: 0.4** · 2/5 questions correct with valid evidence · evidence still in memory for 1.0 of the questions · abstained on 0.2

## 1. Memory available to the answering agent (after step 10)

8 lines, 409 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m1 | E01 @ 2017-10-12 03:11 UTC | Two people are seen walking through a burning landscape with multiple small fires on the ground. |
| m4 | E04 @ 2017-10-12 08:25 UTC | A social media photo shows two people walking through a burning landscape with multiple small fires on the ground. |
| m5 | E05 @ 2017-10-17 16:04 UTC | A social media photo shows two people walking through a burning landscape with multiple small fires on the ground. |
| m6 | E06 @ 2017-10-18 07:23 UTC | A social media photo (Twitter), posted 2017-10-18 07:23 UTC. |
| m7 | E07 @ 2017-10-18 20:21 UTC | A social media photo (Twitter), posted 2017-10-18 20:21 UTC. |
| m8 | E08 @ 2017-10-19 07:36 UTC | A social media photo (Twitter), posted 2017-10-19 07:36 UTC. |
| m9 | E09 @ 2017-10-19 07:36 UTC | A social media photo (Twitter), posted 2017-10-19 07:36 UTC. |
| m10 | E10 @ 2017-10-20 11:11 UTC | A social media photo (Twitter), posted 2017-10-20 11:11 UTC. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E01 | How many people are visible in the image? Select all that apply. | C (Two) | C (Two) | m1 | `correct` | 1.0 |
| 2 | E06 | What is the primary material burning? Answer with one or two words. | Trees | NOT_ENOUGH_EVIDENCE | m6 | `unnecessary_abstention` | 0.0 |
| 3 | E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | m4, m5, m7, m8, m9, m10 | `correct` | 1.0 |
| 4 | E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | m1, m4, m5, m6, m7, m8, m9, m10 | `unsupported` | 0.0 |
| 5 | E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | No | m10 | `wrong_answer_evidence_in_memory` | 0.0 |

### Question 1: about E01 (posted 2017-10-12 03:11 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918313136654049281_0.jpg" width="220">

**Question:** About the photo posted 2017-10-12 03:11 UTC (item E01): How many people are visible in the image? Select all that apply.

**Options:** **A.** None · **B.** One · **C.** Two · **D.** Three

- **Gold answer:** C (Two)
- **Agent's answer:** C (Two)  (raw: `C`)
- **Cited memory lines:** m1
    - m1 [src E01]: Two people are seen walking through a burning landscape with multiple small fires on the ground.
- **Cited photos:** E01 (the question is about E01)
- **Memory about E01:** m1: Two people are seen walking through a burning landscape with multiple small fires on the ground.
- **What the photo shows (dataset facts):** Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence supported (The evidence shows that there are two people visible in the image.)
- **Outcome:** `correct`: correct, cited the right photo, evidence supports it
- **Score:** 1.0

### Question 2: about E06 (posted 2017-10-18 07:23 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920550861343948800_0.jpg" width="220">

**Question:** About the photo posted 2017-10-18 07:23 UTC (item E06): What is the primary material burning? Answer with one or two words.

- **Gold answer:** Trees (accepted: Trees, Vegetation)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m6
    - m6 [src E06]: A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
- **Cited photos:** E06 (the question is about E06)
- **Memory about E06:** m6: A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
- **What the photo shows (dataset facts):** What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 3: about E07 (posted 2017-10-18 20:21 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920746714637721600_0.jpg" width="220">

**Question:** About the photo posted 2017-10-18 20:21 UTC (item E07): What type of disaster is depicted in the image? Select all that apply.

**Options:** **A.** Flood · **B.** Fire · **C.** Earthquake · **D.** Tornado

- **Gold answer:** B (Fire)
- **Agent's answer:** B (Fire)  (raw: `B`)
- **Cited memory lines:** m4, m5, m7, m8, m9, m10
    - m4 [src E04]: A social media photo shows two people walking through a burning landscape with multiple small fires on the ground.
    - m5 [src E05]: A social media photo shows two people walking through a burning landscape with multiple small fires on the ground.
    - m7 [src E07]: A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
    - m8 [src E08]: A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
    - m9 [src E09]: A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
    - m10 [src E10]: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
- **Cited photos:** E04, E05, E07, E08, E09, E10 (the question is about E07)
- **Memory about E07:** m7: A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
- **What the photo shows (dataset facts):** What type of disaster is depicted in the image? Fire
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence supported (The image shows a large plume of black smoke, which is indicative of a fire.)
- **Outcome:** `correct`: correct, cited the right photo, evidence supports it
- **Score:** 1.0

### Question 4: about E09 (posted 2017-10-19 07:36 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920916661519007745_3.jpg" width="220">

**Question:** About the photo posted 2017-10-19 07:36 UTC (item E09): Are these people watching fireworks? Answer with Yes or No.

- **Gold answer:** No
- **Agent's answer:** No  (raw: `No`)
- **Cited memory lines:** m1, m4, m5, m6, m7, m8, m9, m10
    - m1 [src E01]: Two people are seen walking through a burning landscape with multiple small fires on the ground.
    - m4 [src E04]: A social media photo shows two people walking through a burning landscape with multiple small fires on the ground.
    - m5 [src E05]: A social media photo shows two people walking through a burning landscape with multiple small fires on the ground.
    - m6 [src E06]: A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
    - m7 [src E07]: A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
    - m8 [src E08]: A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
    - m9 [src E09]: A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
    - m10 [src E10]: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
- **Cited photos:** E01, E04, E05, E06, E07, E08, E09, E10 (the question is about E09)
- **Memory about E09:** m9: A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
- **What the photo shows (dataset facts):** Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence unsupported (The image shows a wildfire, not fireworks.)
- **Outcome:** `unsupported`: correct answer text, but the cited photo does not support it
- **Score:** 0.0

### Question 5: about E10 (posted 2017-10-20 11:11 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/921332920840843265_0.jpg" width="220">

**Question:** About the photo posted 2017-10-20 11:11 UTC (item E10): Are there any emergency responders present? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** No  (raw: `No`)
- **Cited memory lines:** m10
    - m10 [src E10]: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
- **Cited photos:** E10 (the question is about E10)
- **Memory about E10:** m10: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
- **What the photo shows (dataset facts):** Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
- **Checks:** answer correctness 0.0 (exact); citation valid
- **Outcome:** `wrong_answer_evidence_in_memory`: wrong answer although memory had a note about the photo
- **Score:** 0.0
