# Node 18 · stream `dvqa-wildfire-len10-064` · evaluation

wildfire · 10 photos (E01–E10, 2017-10-12 03:11 UTC → 2017-10-20 11:11 UTC) · questions asked after step 10

**Stream score: 0.2** · 1/5 questions correct with valid evidence · evidence still in memory for 0.8 of the questions · abstained on 0.2

## 1. Memory available to the answering agent (after step 10)

5 lines, 211 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m1 | E01 @ 2017-10-12 03:11 UTC | A social media photo shows a wildfire burning in a forested area. |
| m7 | E07 @ 2017-10-18 20:21 UTC | A social media photo shows a wildfire burning in a forested area. |
| m8 | E08 @ 2017-10-19 07:36 UTC | A social media photo shows a wildfire burning in a forested area. |
| m9 | E09 @ 2017-10-19 07:36 UTC | A social media photo shows a wildfire burning in a forested area. |
| m10 | E10 @ 2017-10-20 11:11 UTC | A social media photo shows a wildfire burning in a forested area. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E01 | How many people are visible in the image? Select all that apply. | C (Two) | A (None) | m1 | `wrong_answer_evidence_in_memory` | 0.0 |
| 2 | E06 | What is the primary material burning? Answer with one or two words. | Trees | Forest | m7, m8, m9, m10 | `invalid_citation` | 0.0 |
| 3 | E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | m7 | `correct` | 1.0 |
| 4 | E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | m8, m9 | `unsupported` | 0.0 |
| 5 | E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | m10 | `unnecessary_abstention` | 0.0 |

### Question 1: about E01 (posted 2017-10-12 03:11 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918313136654049281_0.jpg" width="220">

**Question:** About the photo posted 2017-10-12 03:11 UTC (item E01): How many people are visible in the image? Select all that apply.

**Options:** **A.** None · **B.** One · **C.** Two · **D.** Three

- **Gold answer:** C (Two)
- **Agent's answer:** A (None)  (raw: `A`)
- **Cited memory lines:** m1
    - m1 [src E01]: A social media photo shows a wildfire burning in a forested area.
- **Cited photos:** E01 (the question is about E01)
- **Memory about E01:** m1: A social media photo shows a wildfire burning in a forested area.
- **What the photo shows (dataset facts):** Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
- **Checks:** answer correctness 0.0 (exact); citation valid
- **Outcome:** `wrong_answer_evidence_in_memory`: wrong answer although memory had a note about the photo
- **Score:** 0.0

### Question 2: about E06 (posted 2017-10-18 07:23 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920550861343948800_0.jpg" width="220">

**Question:** About the photo posted 2017-10-18 07:23 UTC (item E06): What is the primary material burning? Answer with one or two words.

- **Gold answer:** Trees (accepted: Trees, Vegetation)
- **Agent's answer:** Forest  (raw: `Forest`)
- **Cited memory lines:** m7, m8, m9, m10
    - m7 [src E07]: A social media photo shows a wildfire burning in a forested area.
    - m8 [src E08]: A social media photo shows a wildfire burning in a forested area.
    - m9 [src E09]: A social media photo shows a wildfire burning in a forested area.
    - m10 [src E10]: A social media photo shows a wildfire burning in a forested area.
- **Cited photos:** E07, E08, E09, E10 (the question is about E06)
- **Memory about E06:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
- **Checks:** answer correctness 1.0 (llm:correct); citation invalid
- **Outcome:** `invalid_citation`: correct answer, but it did not cite the question's photo, or cited a memory line that does not exist
- **Score:** 0.0

### Question 3: about E07 (posted 2017-10-18 20:21 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920746714637721600_0.jpg" width="220">

**Question:** About the photo posted 2017-10-18 20:21 UTC (item E07): What type of disaster is depicted in the image? Select all that apply.

**Options:** **A.** Flood · **B.** Fire · **C.** Earthquake · **D.** Tornado

- **Gold answer:** B (Fire)
- **Agent's answer:** B (Fire)  (raw: `B`)
- **Cited memory lines:** m7
    - m7 [src E07]: A social media photo shows a wildfire burning in a forested area.
- **Cited photos:** E07 (the question is about E07)
- **Memory about E07:** m7: A social media photo shows a wildfire burning in a forested area.
- **What the photo shows (dataset facts):** What type of disaster is depicted in the image? Fire
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence supported (The image shows a large plume of black smoke, which is indicative of a fire.)
- **Outcome:** `correct`: correct, cited the right photo, evidence supports it
- **Score:** 1.0

### Question 4: about E09 (posted 2017-10-19 07:36 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920916661519007745_3.jpg" width="220">

**Question:** About the photo posted 2017-10-19 07:36 UTC (item E09): Are these people watching fireworks? Answer with Yes or No.

- **Gold answer:** No
- **Agent's answer:** No  (raw: `No`)
- **Cited memory lines:** m8, m9
    - m8 [src E08]: A social media photo shows a wildfire burning in a forested area.
    - m9 [src E09]: A social media photo shows a wildfire burning in a forested area.
- **Cited photos:** E08, E09 (the question is about E09)
- **Memory about E09:** m9: A social media photo shows a wildfire burning in a forested area.
- **What the photo shows (dataset facts):** Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence unsupported (The image shows a wildfire, not fireworks.)
- **Outcome:** `unsupported`: correct answer text, but the cited photo does not support it
- **Score:** 0.0

### Question 5: about E10 (posted 2017-10-20 11:11 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/921332920840843265_0.jpg" width="220">

**Question:** About the photo posted 2017-10-20 11:11 UTC (item E10): Are there any emergency responders present? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m10
    - m10 [src E10]: A social media photo shows a wildfire burning in a forested area.
- **Cited photos:** E10 (the question is about E10)
- **Memory about E10:** m10: A social media photo shows a wildfire burning in a forested area.
- **What the photo shows (dataset facts):** Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0
