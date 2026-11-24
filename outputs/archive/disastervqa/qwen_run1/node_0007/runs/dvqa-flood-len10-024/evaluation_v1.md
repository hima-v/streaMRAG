# Node 7 · stream `dvqa-flood-len10-024` · evaluation

flood · 10 photos (E01–E10, 2015-10-08 23:05 UTC → 2015-12-04 17:45 UTC) · questions asked after step 10

**Stream score: 0.0** · 0/5 questions correct with valid evidence · evidence still in memory for 0.4 of the questions · abstained on 0.2

## 1. Memory available to the answering agent (after step 10)

4 lines, 173 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m1 | E01 @ 2015-10-08 23:05 UTC | A flooded street with vehicles partially submerged in water. |
| m8 | E08 @ 2015-12-04 07:54 UTC | A social media photo (Twitter) of a flooded street with vehicles partially submerged in water. |
| m9 | E09 @ 2015-12-04 08:05 UTC | A social media photo (Twitter) of a flooded street with vehicles partially submerged in water. |
| m10 | E10 @ 2015-12-04 17:45 UTC | A social media photo (Twitter) of a flooded street with vehicles partially submerged in water. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | NOT_ENOUGH_EVIDENCE | `wrong_answer_evidence_missing` | 0.0 |
| 2 | E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | m8, m9, m10 | `invalid_citation` | 0.0 |
| 3 | E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | m8, m9, m10 | `abstained_evidence_missing` | 0.0 |
| 4 | E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | C (Highway) | m8, m9, m10 | `wrong_answer_evidence_in_memory` | 0.0 |
| 5 | E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | m10 | `wrong_answer_evidence_in_memory` | 0.0 |

### Question 1: about E03 (posted 2015-12-03 16:52 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672458294959607808_0.jpg" width="220">

**Question:** About the photo posted 2015-12-03 16:52 UTC (item E03): Are there any vehicles submerged in water? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** No  (raw: `No`)
- **Cited memory lines:** NOT_ENOUGH_EVIDENCE
    - NOT_ENOUGH_EVIDENCE: (no such line in memory)
- **Cited photos:** none (the question is about E03)
- **Memory about E03:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
- **Checks:** answer correctness 0.0 (exact); citation invalid
- **Outcome:** `wrong_answer_evidence_missing`: wrong answer; memory had no note about the photo
- **Score:** 0.0

### Question 2: about E04 (posted 2015-12-03 17:20 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672465551357255680_0.jpg" width="220">

**Question:** About the photo posted 2015-12-03 17:20 UTC (item E04): What is the primary obstacle on the road? Answer with one or two words.

- **Gold answer:** Floodwater (accepted: Floodwater, Water, Flooding, Floods, Flood, Water flood, Flood water, Flooded road)
- **Agent's answer:** Flooded  (raw: `Flooded`)
- **Cited memory lines:** m8, m9, m10
    - m8 [src E08]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
    - m9 [src E09]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
    - m10 [src E10]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
- **Cited photos:** E08, E09, E10 (the question is about E04)
- **Memory about E04:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
- **Checks:** answer correctness 1.0 (accepted_match); citation invalid
- **Outcome:** `invalid_citation`: correct answer, but it did not cite the question's photo
- **Score:** 0.0

### Question 3: about E06 (posted 2015-12-04 03:38 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672620846309965824_0.jpg" width="220">

**Question:** About the photo posted 2015-12-04 03:38 UTC (item E06): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.

- **Gold answer:** No
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m8, m9, m10
    - m8 [src E08]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
    - m9 [src E09]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
    - m10 [src E10]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
- **Cited photos:** E08, E09, E10 (the question is about E06)
- **Memory about E06:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 4: about E08 (posted 2015-12-04 07:54 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672685451426295813_1.jpg" width="220">

**Question:** About the photo posted 2015-12-04 07:54 UTC (item E08): What infrastructure is affected by the flooding? Select all that apply.

**Options:** **A.** Railway · **B.** Airport · **C.** Highway · **D.** Residential area

- **Gold answer:** A (Railway)
- **Agent's answer:** C (Highway)  (raw: `C`)
- **Cited memory lines:** m8, m9, m10
    - m8 [src E08]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
    - m9 [src E09]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
    - m10 [src E10]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
- **Cited photos:** E08, E09, E10 (the question is about E08)
- **Memory about E08:** m8: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
- **What the photo shows (dataset facts):** What infrastructure is affected by the flooding? Railway
- **Checks:** answer correctness 0.0 (exact); citation valid
- **Outcome:** `wrong_answer_evidence_in_memory`: wrong answer although memory had a note about the photo
- **Score:** 0.0

### Question 5: about E10 (posted 2015-12-04 17:45 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672834059966349312_1.jpg" width="220">

**Question:** About the photo posted 2015-12-04 17:45 UTC (item E10): What type of vehicle is partially submerged in the water? Select all that apply.

**Options:** **A.** Car · **B.** Bus · **C.** Auto-rickshaw · **D.** Truck

- **Gold answer:** C (Auto-rickshaw)
- **Agent's answer:** A (Car)  (raw: `A`)
- **Cited memory lines:** m10
    - m10 [src E10]: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
- **Cited photos:** E10 (the question is about E10)
- **Memory about E10:** m10: A social media photo (Twitter) of a flooded street with vehicles partially submerged in water.
- **What the photo shows (dataset facts):** Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
- **Checks:** answer correctness 0.0 (exact); citation valid
- **Outcome:** `wrong_answer_evidence_in_memory`: wrong answer although memory had a note about the photo
- **Score:** 0.0
