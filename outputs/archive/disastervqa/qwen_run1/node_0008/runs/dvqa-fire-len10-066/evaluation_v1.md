# Node 8 · stream `dvqa-fire-len10-066` · evaluation

fire · 10 photos (E01–E10, 2017-02-25 03:14 UTC → 2017-09-08 03:41 UTC) · questions asked after step 10

**Stream score: 0.2** · 1/5 questions correct with valid evidence · evidence still in memory for 0.6 of the questions · abstained on 0.6

## 1. Memory available to the answering agent (after step 10)

7 lines, 493 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m4 | E04 @ 2017-06-25 00:20 UTC | A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building. |
| m5 | E05 @ 2017-06-25 21:15 UTC | A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building. |
| m6 | E06 @ 2017-07-21 00:43 UTC | A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building. |
| m7 | E07 @ 2017-08-23 00:46 UTC | A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building. |
| m8 | E08 @ 2017-08-28 10:43 UTC | A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building. |
| m9 | E09 @ 2017-09-06 09:22 UTC | A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building. |
| m10 | E10 @ 2017-09-08 03:41 UTC | A social media photo shows a large fire burning in a multi-story building. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | m4, m5, m6, m7, m8, m9, m10 | `abstained_evidence_missing` | 0.0 |
| 2 | E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | m4, m5, m6, m7, m8, m9, m10 | `abstained_evidence_missing` | 0.0 |
| 3 | E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | C (High-rise) | m4 | `wrong_answer_evidence_in_memory` | 0.0 |
| 4 | E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | m5 | `correct` | 1.0 |
| 5 | E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | m6 | `unnecessary_abstention` | 0.0 |

### Question 1: about E01 (posted 2017-02-25 03:14 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-02-25_03-14-47.jpg" width="220">

**Question:** About the photo posted 2017-02-25 03:14 UTC (item E01): How many emergency ladders are deployed? Answer with one or two words.

- **Gold answer:** Four (accepted: Four, 4, Four ladders, Four deployed)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m4, m5, m6, m7, m8, m9, m10
    - m4 [src E04]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m5 [src E05]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m6 [src E06]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m7 [src E07]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m8 [src E08]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m9 [src E09]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m10 [src E10]: A social media photo shows a large fire burning in a multi-story building.
- **Cited photos:** E04, E05, E06, E07, E08, E09, E10 (the question is about E01)
- **Memory about E01:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 2: about E03 (posted 2017-06-01 13:57 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/suicidebombing_2017-06-01_13-57-59.jpg" width="220">

**Question:** About the photo posted 2017-06-01 13:57 UTC (item E03): Are there damaged vehicles in the image? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m4, m5, m6, m7, m8, m9, m10
    - m4 [src E04]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m5 [src E05]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m6 [src E06]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m7 [src E07]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m8 [src E08]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m9 [src E09]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
    - m10 [src E10]: A social media photo shows a large fire burning in a multi-story building.
- **Cited photos:** E04, E05, E06, E07, E08, E09, E10 (the question is about E03)
- **Memory about E03:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 3: about E04 (posted 2017-06-25 00:20 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-06-25_00-20-19.jpg" width="220">

**Question:** About the photo posted 2017-06-25 00:20 UTC (item E04): What type of building is affected by the fire? Select all that apply.

**Options:** **A.** Residential · **B.** Commercial · **C.** High-rise · **D.** Town house

- **Gold answer:** B (Commercial)
- **Agent's answer:** C (High-rise)  (raw: `C`)
- **Cited memory lines:** m4
    - m4 [src E04]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
- **Cited photos:** E04 (the question is about E04)
- **Memory about E04:** m4: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
- **What the photo shows (dataset facts):** Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
- **Checks:** answer correctness 0.0 (exact); citation valid
- **Outcome:** `wrong_answer_evidence_in_memory`: wrong answer although memory had a note about the photo
- **Score:** 0.0

### Question 4: about E05 (posted 2017-06-25 21:15 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-06-25_21-15-49.jpg" width="220">

**Question:** About the photo posted 2017-06-25 21:15 UTC (item E05): What is the condition of the buildings in the image? Select all that apply.

**Options:** **A.** Collapsed · **B.** Intact with smoke · **C.** Flooded · **D.** Damaged by wind

- **Gold answer:** B (Intact with smoke)
- **Agent's answer:** B (Intact with smoke)  (raw: `B`)
- **Cited memory lines:** m5
    - m5 [src E05]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
- **Cited photos:** E05 (the question is about E05)
- **Memory about E05:** m5: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
- **What the photo shows (dataset facts):** What is the condition of the buildings in the image? Intact with smoke
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence supported (The evidence states that the buildings are intact with smoke, which matches the answer given.)
- **Outcome:** `correct`: correct, cited the right photo, evidence supports it
- **Score:** 1.0

### Question 5: about E06 (posted 2017-07-21 00:43 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-07-21_00-43-25.jpg" width="220">

**Question:** About the photo posted 2017-07-21 00:43 UTC (item E06): Are there residential buildings near the fire? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m6
    - m6 [src E06]: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
- **Cited photos:** E06 (the question is about E06)
- **Memory about E06:** m6: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
- **What the photo shows (dataset facts):** Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0
