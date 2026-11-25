# Node 0 (root)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

Root node: seed strategy `configs/strategies/seeds/minimal.md`, seed meta harness `configs/meta/minimal.md`.

## Memory strategy (`2c0dda390240`)

```
Update the memory with the new item.
```

## Meta harness (`f692b318db8e`)

```
Improve the memory strategy.
```

## Score

**Node score (mean over streams): 0.2** · correct 5/25 · evidence retained 0.92 · abstained 0.64 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 341 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 1.0 | 9 lines, 362 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 1.0 | 9 lines, 379 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 322 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 382 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `correct` | yes |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Flooded area | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Aerial view of a flooded area with buildings and vehicles submerged in water.
m4 [src E04] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m5 [src E05] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m6 [src E06] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m7 [src E07] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m8 [src E08] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m9 [src E09] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m10 [src E10] A social media photo shows a damaged building with debris scattered around.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A man is swimming in a river, holding onto a rope.
m3 [src E03] ...
m4 [src E04] Social media photo (Twitter), posted 2015-12-03 17:20 UTC.
m5 [src E05] A man is swimming in a river, holding onto a rope.
m6 [src E06] A man is swimming in a river, holding onto a rope.
m7 [src E07] A man is swimming in a river, holding onto a rope.
m8 [src E08] A man is swimming in a river, holding onto a rope.
m9 [src E09] A man is swimming in a river, holding onto a rope.
m10 [src E10] A man is swimming in a river, holding onto a rope.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `correct` | yes |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
m3 [src E03] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
m4 [src E04] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
m5 [src E05] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
m6 [src E06] ...
m7 [src E07] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
m8 [src E08] ...
m9 [src E09] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
m10 [src E10] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
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
m1 [src E01] Two people are seen running through a burning field during a wildfire.
m4 [src E04] A social media photo shows a wildfire burning through a field.
m5 [src E05] A social media photo shows a wildfire burning through a field.
m6 [src E06] A social media photo shows a wildfire burning through a field.
m7 [src E07] A social media photo shows a wildfire burning through a field.
m8 [src E08] A social media photo shows a wildfire burning through a field.
m9 [src E09] A social media photo shows a wildfire burning through a field.
m10 [src E10] A social media photo shows a wildfire burning through a field.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large building fire is being fought by firefighters using ladders and hoses.
m4 [src E04] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
m5 [src E05] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
m6 [src E06] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
m7 [src E07] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
m8 [src E08] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
m9 [src E09] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
m10 [src E10] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.2 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 341 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* unnecessary_abstention | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 5)
  memory about E05: A social media photo shows a flooded area with buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded area with buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a flooded area with buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/84; 3:2/85; 4:2/85; 5:3/128; 6:4/171; 7:5/214; 8:6/257; 9:7/300; 10:8/341
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with buildings and vehicles submerged in water.
  m4 [src E04] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m5 [src E05] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m6 [src E06] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m7 [src E07] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m8 [src E08] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m9 [src E09] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m10 [src E10] A social media photo shows a damaged building with debris scattered around.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 9 lines / 362 tokens; budget fallbacks 0).
OUTCOMES: unnecessary_abstention=4, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_in_memory | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 3)
  memory about E03: ...
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* unnecessary_abstention | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: Social media photo (Twitter), posted 2015-12-03 17:20 UTC.
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A man is swimming in a river, holding onto a rope.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* unnecessary_abstention | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A man is swimming in a river, holding onto a rope.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A man is swimming in a river, holding onto a rope.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/57; 2:2/114; 3:2/56; 4:3/135; 5:4/161; 6:5/201; 7:6/241; 8:7/281; 9:8/321; 10:9/362
FINAL MEMORY:
  m1 [src E01] A man is swimming in a river, holding onto a rope.
  m3 [src E03] ...
  m4 [src E04] Social media photo (Twitter), posted 2015-12-03 17:20 UTC.
  m5 [src E05] A man is swimming in a river, holding onto a rope.
  m6 [src E06] A man is swimming in a river, holding onto a rope.
  m7 [src E07] A man is swimming in a river, holding onto a rope.
  m8 [src E08] A man is swimming in a river, holding onto a rope.
  m9 [src E09] A man is swimming in a river, holding onto a rope.
  m10 [src E10] A man is swimming in a river, holding onto a rope.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 9 lines / 379 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: ...
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/68; 3:2/74; 4:3/120; 5:4/184; 6:5/194; 7:6/258; 8:7/268; 9:8/332; 10:9/379
FINAL MEMORY:
  m1 [src E01] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  m3 [src E03] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  m4 [src E04] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  m5 [src E05] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  m6 [src E06] ...
  m7 [src E07] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  m8 [src E08] ...
  m9 [src E09] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.
  m10 [src E10] A social media photo shows a scene of a collapsed building with rescue workers and onlookers.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 322 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a wildfire burning through a field.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a wildfire burning through a field.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a wildfire burning through a field.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/81; 3:2/81; 4:2/81; 5:3/121; 6:4/161; 7:5/201; 8:6/241; 9:7/281; 10:8/322
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning field during a wildfire.
  m4 [src E04] A social media photo shows a wildfire burning through a field.
  m5 [src E05] A social media photo shows a wildfire burning through a field.
  m6 [src E06] A social media photo shows a wildfire burning through a field.
  m7 [src E07] A social media photo shows a wildfire burning through a field.
  m8 [src E08] A social media photo shows a wildfire burning through a field.
  m9 [src E09] A social media photo shows a wildfire burning through a field.
  m10 [src E10] A social media photo shows a wildfire burning through a field.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.8 of the questions; final memory 8 lines / 382 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large building fire is being fought by firefighters using ladders and hoses.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* unnecessary_abstention | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/45; 2:2/93; 3:2/93; 4:2/93; 5:3/141; 6:4/189; 7:5/237; 8:6/285; 9:7/333; 10:8/382
FINAL MEMORY:
  m1 [src E01] A large building fire is being fought by firefighters using ladders and hoses.
  m4 [src E04] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  m5 [src E05] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  m6 [src E06] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  m7 [src E07] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  m8 [src E08] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  m9 [src E09] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
  m10 [src E10] A social media photo shows a firefighter standing on top of a fire truck during a large building fire.
```
