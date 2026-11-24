# Node 1 · stream `dvqa-flood-len10-024` · evaluation

flood · 10 photos (E01–E10, 2015-10-08 23:05 UTC → 2015-12-04 17:45 UTC) · questions asked after step 10

**Stream score: 0.0** · 0/5 questions correct with valid evidence · evidence still in memory for 0.8 of the questions · abstained on 1.0

## 1. Memory available to the answering agent (after step 10)

8 lines, 411 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m1 | E01 @ 2015-10-08 23:05 UTC | A social media photo was posted on Twitter on December 4, 2015, at 03:05 UTC. |
| m4 | E04 @ 2015-12-03 17:20 UTC | A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC. |
| m5 | E05 @ 2015-12-03 17:45 UTC | A man is swimming in a river, holding onto a rope. |
| m6 | E06 @ 2015-12-04 03:38 UTC | A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC. |
| m7 | E07 @ 2015-12-04 04:24 UTC | A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC. |
| m8 | E08 @ 2015-12-04 07:54 UTC | A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC. |
| m9 | E09 @ 2015-12-04 08:05 UTC | A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC. |
| m10 | E10 @ 2015-12-04 17:45 UTC | A man is swimming in a river, holding onto a rope. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | m4, m5, m6, m7, m8, m9, m10 | `abstained_evidence_missing` | 0.0 |
| 2 | E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | m4 | `unnecessary_abstention` | 0.0 |
| 3 | E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | m6 | `unnecessary_abstention` | 0.0 |
| 4 | E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | m8 | `unnecessary_abstention` | 0.0 |
| 5 | E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | m10 | `unnecessary_abstention` | 0.0 |

### Question 1: about E03 (posted 2015-12-03 16:52 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672458294959607808_0.jpg" width="220">

**Question:** About the photo posted 2015-12-03 16:52 UTC (item E03): Are there any vehicles submerged in water? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m4, m5, m6, m7, m8, m9, m10
    - m4 [src E04]: A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
    - m5 [src E05]: A man is swimming in a river, holding onto a rope.
    - m6 [src E06]: A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
    - m7 [src E07]: A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
    - m8 [src E08]: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
    - m9 [src E09]: A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
    - m10 [src E10]: A man is swimming in a river, holding onto a rope.
- **Cited photos:** E04, E05, E06, E07, E08, E09, E10 (the question is about E03)
- **Memory about E03:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 2: about E04 (posted 2015-12-03 17:20 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672465551357255680_0.jpg" width="220">

**Question:** About the photo posted 2015-12-03 17:20 UTC (item E04): What is the primary obstacle on the road? Answer with one or two words.

- **Gold answer:** Floodwater (accepted: Floodwater, Water, Flooding, Floods, Flood, Water flood, Flood water, Flooded road)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m4
    - m4 [src E04]: A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
- **Cited photos:** E04 (the question is about E04)
- **Memory about E04:** m4: A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
- **What the photo shows (dataset facts):** What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 3: about E06 (posted 2015-12-04 03:38 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672620846309965824_0.jpg" width="220">

**Question:** About the photo posted 2015-12-04 03:38 UTC (item E06): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.

- **Gold answer:** No
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m6
    - m6 [src E06]: A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
- **Cited photos:** E06 (the question is about E06)
- **Memory about E06:** m6: A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
- **What the photo shows (dataset facts):** Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 4: about E08 (posted 2015-12-04 07:54 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672685451426295813_1.jpg" width="220">

**Question:** About the photo posted 2015-12-04 07:54 UTC (item E08): What infrastructure is affected by the flooding? Select all that apply.

**Options:** **A.** Railway · **B.** Airport · **C.** Highway · **D.** Residential area

- **Gold answer:** A (Railway)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m8
    - m8 [src E08]: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
- **Cited photos:** E08 (the question is about E08)
- **Memory about E08:** m8: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
- **What the photo shows (dataset facts):** What infrastructure is affected by the flooding? Railway
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 5: about E10 (posted 2015-12-04 17:45 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672834059966349312_1.jpg" width="220">

**Question:** About the photo posted 2015-12-04 17:45 UTC (item E10): What type of vehicle is partially submerged in the water? Select all that apply.

**Options:** **A.** Car · **B.** Bus · **C.** Auto-rickshaw · **D.** Truck

- **Gold answer:** C (Auto-rickshaw)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m10
    - m10 [src E10]: A man is swimming in a river, holding onto a rope.
- **Cited photos:** E10 (the question is about E10)
- **Memory about E10:** m10: A man is swimming in a river, holding onto a rope.
- **What the photo shows (dataset facts):** Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0
