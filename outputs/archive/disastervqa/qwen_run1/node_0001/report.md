# Node 1 (child of node 0)

Archive `qwen_run1` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 0's strategy, meta harness and evaluation log (`node_0000/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Current issues include excessive redundancy (e.g., repeating "A social media photo..." for multiple similar images) and failure to filter out non-critical details (e.g., timestamps without contextual value). By enforcing deduplication and focusing on atomic facts tied to answerability, we reduce token usage while preserving actionable data. Tags prevent repetition penalties, and semantic filtering ensures relevance. This aligns with evaluation failures caused by bloated memory (e.g., 9/10 steps storing identical entries) and misaligned retrieval logic.
- Strategy rationale: The original strategy aimed to minimize redundancy while preserving critical details. However, it failed to enforce strict deduplication rules—many entries retained verbatim repetition despite identical content (e.g., seven consecutive identical entries in some streams). By mandating explicit duplicate tagging and stricter extraction criteria ("high-value," temporally ordered), we ensure memory compactness without losing uniqueness. This aligns better with token limits and improves retrieval reliability by reducing noise.
- Change: Added explicit requirement to group identical content into one canonical entry + use tags. Replaced vague "avoid redundancies" with precise instruction to store only "distinct critical details." Clarified focus on entity-based extraction (actions/hazards/damage) vs. sentence-level retention. Emphasized temporal ordering and deletion tracking for accuracy. Removed ambiguous phrasing ("redundant") to standardize implementation.

## Memory strategy (`aae2edb5a2b8`)

```
For each incoming data point, extract and retain **unique, high-value details** (specific entities, actions, outcomes) instead of full sentences. Group identical event descriptions into a single canonical entry (earliest timestamp) and reference duplicates via tags (`~duplicate~`). Avoid storing repetitive phrases (e.g., "social media photo..."). Maintain temporal order but discard non-critical repetitions. Track deletions explicitly if needed. Prioritize actionable facts (e.g., hazards, casualties, damage types) over generic descriptors. Limit entries to 512 tokens total.
```

## Meta harness (`e5dc23a55010`)

```
**Meta Harness:**  
"Optimize the memory storage strategy by prioritizing unique, high-value information per event while avoiding redundant verbatim copies. For each incoming data point, extract and retain only distinct critical details (e.g., specific entities like 'flood', 'collapsed', 'emergency responders') rather than full sentences. If multiple events share identical content (e.g., repeated descriptions of a fire), store them once under the earliest timestamp and reference subsequent instances via tags (e.g., `m10 ~duplicate~`). When retrieving memories, cross-check against question context to avoid citations where evidence was later deleted or deemed irrelevant."
```

## Score

**Node score (mean over streams): 0.12** · correct 3/25 · evidence retained 0.56 · abstained 0.68 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 171 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.8 | 8 lines, 411 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.4 | 3 lines, 136 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 376 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.2 | 4 lines, 173 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `correct` | yes |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Flooded area | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Aerial view of flooded area with buildings and vehicles submerged in water.
m8 [src E08] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m9 [src E09] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m10 [src E10] A social media photo shows a flooded area with buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 03:05 UTC.
m4 [src E04] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
m5 [src E05] A man is swimming in a river, holding onto a rope.
m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m10 [src E10] A man is swimming in a river, holding onto a rope.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `invalid_citation` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Two workers are seen on a ladder amidst the rubble of a collapsed building.
m9 [src E09] A social media photo shows two workers on a ladder amidst the rubble of a collapsed building.
m10 [src E10] A social media photo shows two workers on a ladder amidst the rubble of a collapsed building.
```

## Stream `dvqa-wildfire-len10-064` ([evaluation.md](runs/dvqa-wildfire-len10-064/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many people are visible in the image? Select all that apply. | C (Two) | C (Two) | `correct` | yes |
| E06 | What is the primary material burning? Answer with one or two words. | Trees | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | `correct` | yes |
| E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | `unsupported` | yes |
| E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] Two individuals are seen walking through a burning landscape with multiple flames and charred tree stumps.
m4 [src E04] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
m5 [src E05] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
m6 [src E06] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
m7 [src E07] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
m8 [src E08] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
m9 [src E09] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
m10 [src E10] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |

Final memory:

```
m1 [src E01] A social media photo shows a scene of destruction with a burning vehicle and debris.
m8 [src E08] A social media photo shows a scene of destruction with a burning vehicle and debris.
m9 [src E09] A social media photo shows a scene of destruction with a burning vehicle and debris.
m10 [src E10] A social media photo shows a scene of destruction with a burning vehicle and debris.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 171 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, correct=1, invalid_citation=1, unnecessary_abstention=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* abstained_evidence_missing | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* abstained_evidence_missing | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a flooded area with buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/82; 3:2/84; 4:2/84; 5:2/84; 6:2/84; 7:2/84; 8:2/84; 9:3/127; 10:4/171
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with buildings and vehicles submerged in water.
  m8 [src E08] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m9 [src E09] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m10 [src E10] A social media photo shows a flooded area with buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.8 of the questions; final memory 8 lines / 411 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* unnecessary_abstention | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* unnecessary_abstention | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A man is swimming in a river, holding onto a rope.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:3/150; 6:4/205; 7:5/260; 8:6/315; 9:7/370; 10:8/411
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 03:05 UTC.
  m4 [src E04] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  m5 [src E05] A man is swimming in a river, holding onto a rope.
  m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m10 [src E10] A man is swimming in a river, holding onto a rope.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 3 lines / 136 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* invalid_citation | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* wrong_answer_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows two workers on a ladder amidst the rubble of a collapsed building.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows two workers on a ladder amidst the rubble of a collapsed building.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/87; 3:2/89; 4:2/89; 5:2/89; 6:2/89; 7:2/89; 8:2/89; 9:2/89; 10:3/136
FINAL MEMORY:
  m1 [src E01] Two workers are seen on a ladder amidst the rubble of a collapsed building.
  m9 [src E09] A social media photo shows two workers on a ladder amidst the rubble of a collapsed building.
  m10 [src E10] A social media photo shows two workers on a ladder amidst the rubble of a collapsed building.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 376 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/46; 2:2/93; 3:2/93; 4:2/93; 5:3/140; 6:4/187; 7:5/234; 8:6/281; 9:7/328; 10:8/376
FINAL MEMORY:
  m1 [src E01] Two individuals are seen walking through a burning landscape with multiple flames and charred tree stumps.
  m4 [src E04] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  m5 [src E05] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  m6 [src E06] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  m7 [src E07] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  m8 [src E08] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  m9 [src E09] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.
  m10 [src E10] A social media photo from Twitter shows a burning landscape with multiple flames and charred tree stumps.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.2 of the questions; final memory 4 lines / 173 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=4, unnecessary_abstention=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A social media photo shows a scene of destruction with a burning vehicle and debris.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* abstained_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* abstained_evidence_missing | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* abstained_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/37; 2:2/79; 3:2/86; 4:2/86; 5:2/86; 6:2/86; 7:2/86; 8:2/86; 9:3/129; 10:4/173
FINAL MEMORY:
  m1 [src E01] A social media photo shows a scene of destruction with a burning vehicle and debris.
  m8 [src E08] A social media photo shows a scene of destruction with a burning vehicle and debris.
  m9 [src E09] A social media photo shows a scene of destruction with a burning vehicle and debris.
  m10 [src E10] A social media photo shows a scene of destruction with a burning vehicle and debris.
```
