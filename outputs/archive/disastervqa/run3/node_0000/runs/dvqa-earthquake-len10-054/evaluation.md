# Node 0 · stream `dvqa-earthquake-len10-054` · evaluation

earthquake · 10 photos (E01–E10, 2017-09-21 04:40 UTC → 2017-09-21 10:48 UTC) · questions asked after step 10

**Stream score: 0.2** · 1/5 questions correct with valid evidence · evidence still in memory for 0.8 of the questions · abstained on 0.6

## 1. Memory available to the answering agent (after step 10)

5 lines, 460 / 512 tokens. This is everything the answering agent sees, besides the question; it never sees the photos.

| line | sources (item @ posted) | text |
|---|---|---|
| m5 | E06 @ 2017-09-21 07:16 UTC | A social media photo from Twitter, posted on 2017-09-21 at 07:16 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath. |
| m6 | E07 @ 2017-09-21 08:35 UTC | m7 [src E07 @2017-09-21 08:35 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:35 UTC, depicting a collapsed building with a car partially buried in debris in the foreground. |
| m7 | E08 @ 2017-09-21 08:44 UTC | m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath. |
| m8 | E09 @ 2017-09-21 10:33 UTC | m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath. |
| m9 | E10 @ 2017-09-21 10:48 UTC | m10 [src E10 @2017-09-21 10:48 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:48 UTC, depicting a collapsed building with a dog navigating through debris and scattered personal items. |

## 2. Questions, answers and evaluation

| # | item | question | gold answer | agent's answer | cited lines | outcome | score |
|---|---|---|---|---|---|---|---|
| 1 | E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | — | `abstained_evidence_missing` | 0.0 |
| 2 | E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | m6, m7 | `correct` | 1.0 |
| 3 | E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | m7, m8 | `wrong_answer_evidence_in_memory` | 0.0 |
| 4 | E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | m8, m9 | `unnecessary_abstention` | 0.0 |
| 5 | E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | E10 | `unnecessary_abstention` | 0.0 |

### Question 1: about E04 (posted 2017-09-21 06:50 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910758076579491840_0.jpg" width="220">

**Question:** About the photo posted 2017-09-21 06:50 UTC (item E04): What is the primary material of the debris? Answer with one or two words.

- **Gold answer:** Bricks (accepted: Bricks, Wood, Brick, Concrete)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** none
    - : (no such line in memory)
- **Cited photos:** none (the question is about E04)
- **Memory about E04:** none (the photo is not in memory)
- **What the photo shows (dataset facts):** Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
- **Checks:** abstained, so no answer to check
- **Outcome:** `abstained_evidence_missing`: abstained; memory had no note about the photo
- **Score:** 0.0

### Question 2: about E07 (posted 2017-09-21 08:35 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910784474337574912_0.jpg" width="220">

**Question:** About the photo posted 2017-09-21 08:35 UTC (item E07): What is the condition of the building in the image? Select all that apply.

**Options:** **A.** Intact · **B.** Partially damaged · **C.** Collapsed · **D.** Under construction

- **Gold answer:** C (Collapsed)
- **Agent's answer:** C (Collapsed)  (raw: `C`)
- **Cited memory lines:** m6, m7
    - m6 [src E07]: m7 [src E07 @2017-09-21 08:35 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:35 UTC, depicting a collapsed building with a car partially buried in debris in the foreground.
    - m7 [src E08]: m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
- **Cited photos:** E07, E08 (the question is about E07)
- **Memory about E07:** m6: m7 [src E07 @2017-09-21 08:35 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:35 UTC, depicting a collapsed building with a car partially buried in debris in the foreground.
- **What the photo shows (dataset facts):** Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
- **Checks:** answer correctness 1.0 (exact); citation valid; evaluator: evidence supported (The evidence shows that the building is collapsed, which matches the answer.)
- **Outcome:** `correct`: correct, cited the right photo, evidence supports it
- **Score:** 1.0

### Question 3: about E08 (posted 2017-09-21 08:44 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910786811164635136_0.jpg" width="220">

**Question:** About the photo posted 2017-09-21 08:44 UTC (item E08): Is there heavy machinery present in the image? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** No  (raw: `No`)
- **Cited memory lines:** m7, m8
    - m7 [src E08]: m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
    - m8 [src E09]: m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
- **Cited photos:** E08, E09 (the question is about E08)
- **Memory about E08:** m7: m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
- **What the photo shows (dataset facts):** Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
- **Checks:** answer correctness 0.0 (exact); citation valid
- **Outcome:** `wrong_answer_evidence_in_memory`: wrong answer although memory had a note about the photo
- **Score:** 0.0

### Question 4: about E09 (posted 2017-09-21 10:33 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910814140192526336_0.jpg" width="220">

**Question:** About the photo posted 2017-09-21 10:33 UTC (item E09): Is the debris mostly concrete? Answer with Yes or No.

- **Gold answer:** Yes
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** m8, m9
    - m8 [src E09]: m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
    - m9 [src E10]: m10 [src E10 @2017-09-21 10:48 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:48 UTC, depicting a collapsed building with a dog navigating through debris and scattered personal items.
- **Cited photos:** E09, E10 (the question is about E09)
- **Memory about E09:** m8: m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
- **What the photo shows (dataset facts):** Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0

### Question 5: about E10 (posted 2017-09-21 10:48 UTC)

<img src="../../../../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910818046683631616_0.jpg" width="220">

**Question:** About the photo posted 2017-09-21 10:48 UTC (item E10): What is the primary material visible in the debris? Select all that apply.

**Options:** **A.** Wood · **B.** Metal · **C.** Concrete · **D.** Glass

- **Gold answer:** C (Concrete)
- **Agent's answer:** NOT_ENOUGH_EVIDENCE  (raw: `NOT_ENOUGH_EVIDENCE`)
- **Cited memory lines:** E10
    - E10: (no such line in memory)
- **Cited photos:** none (the question is about E10)
- **Memory about E10:** m9: m10 [src E10 @2017-09-21 10:48 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:48 UTC, depicting a collapsed building with a dog navigating through debris and scattered personal items.
- **What the photo shows (dataset facts):** What is the primary material visible in the debris? Concrete; How many dogs are visible? One
- **Checks:** abstained, so no answer to check
- **Outcome:** `unnecessary_abstention`: abstained although memory had a note about the photo
- **Score:** 0.0
