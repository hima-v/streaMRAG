# Node 0 (root)

Archive `run3` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

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

**Node score (mean over streams): 0.12** · correct 3/25 · evidence retained 0.56 · abstained 0.44 · budget fallbacks 13

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.0 | 0/5 | 0.2 | 4 lines, 487 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.4 | 4 lines, 496 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 0.8 | 5 lines, 460 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.2 | 1/5 | 0.8 | 6 lines, 498 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.6 | 7 lines, 470 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `invalid_citation` | no |
| E03 | What type of area is affected? Answer with one or two words. | Residential | flooded area | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | No | `invalid_citation` | no |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m7 [src E07] m7 [src E07 @2017-09-19 18:40 UTC] social media photo (Twitter), posted 2017-09-19 18:40 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
m8 [src E08] social media photo (Twitter), posted 2017-09-19 19:20 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
m9 [src E09] social media photo (Twitter), posted 2017-09-19 19:51 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
m10 [src E10] social media photo (Twitter), posted 2017-09-19 20:20 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Floodwaters | `invalid_citation` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m7 [src E07] m7 [src E07 @2015-12-04 04:24 UTC] A social media photo from Twitter, posted on 2015-12-04 04:24 UTC, depicting a flooded area with a group of people and military personnel in a green boat, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals and soldiers navigating through the floodwaters.
m8 [src E08] m8 [src E08 @2015-12-04 07:54 UTC] A social media photo from Twitter, posted on 2015-12-04 07:54 UTC, depicting a flooded area with a group of people and military personnel in a green boat, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals and soldiers navigating through the floodwaters.
m9 [src E09] m9 [src E09 @2015-12-04 08:05 UTC] A social media photo from Twitter, posted on 2015-12-04 08:05 UTC, depicting a flooded area with a group of people wading through muddy water, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals navigating through the floodwaters.
m10 [src E10] m10 [src E10 @2015-12-04 17:45 UTC] A social media photo from Twitter, posted on 2015-12-04 17:45 UTC, depicting a flooded area with a group of people wading through muddy water, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals navigating through the floodwaters.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `correct` | yes |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m5 [src E06] A social media photo from Twitter, posted on 2017-09-21 at 07:16 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
m6 [src E07] m7 [src E07 @2017-09-21 08:35 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:35 UTC, depicting a collapsed building with a car partially buried in debris in the foreground.
m7 [src E08] m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
m8 [src E09] m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
m9 [src E10] m10 [src E10 @2017-09-21 10:48 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:48 UTC, depicting a collapsed building with a dog navigating through debris and scattered personal items.
```

## Stream `dvqa-wildfire-len10-064` ([evaluation.md](runs/dvqa-wildfire-len10-064/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many people are visible in the image? Select all that apply. | C (Two) | A (None) | `wrong_answer_evidence_missing` | no |
| E06 | What is the primary material burning? Answer with one or two words. | Trees | Dry vegetation | `unsupported` | yes |
| E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | `correct` | yes |
| E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | `unsupported` | yes |
| E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m4 [src E04] A social media photo posted on Twitter on October 12, 2017, at 08:25 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
m5 [src E05] A social media photo posted on Twitter on October 17, 2017, at 16:04 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
m6 [src E06] A social media photo posted on Twitter on October 18, 2017, at 07:23 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
m7 [src E07] A social media photo posted on Twitter on October 18, 2017, at 20:21 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
m9 [src E09] m9 [src E09 @2017-10-19 07:36 UTC] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
m10 [src E10] m10 [src E10 @2017-10-20 11:11 UTC] A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m4 [src E04] social media photo (web), posted 2017-06-25 00:20 UTC
m5 [src E05] social media photo (web), posted 2017-06-25 21:15 UTC
m6 [src E06] social media photo (web), posted 2017-07-21 00:43 UTC
m7 [src E07] m7 [src E07 @2017-08-23 00:46 UTC] social media photo (web), posted 2017-08-23 00:46 UTC
m8 [src E08] m8 [src E08 @2017-08-28 10:43 UTC] social media photo (Twitter), posted 2017-08-28 10:43 UTC
m9 [src E09] m9 [src E09 @2017-09-06 09:22 UTC] social media photo (Twitter), posted 2017-09-06 09:22 UTC
m10 [src E10] m10 [src E10 @2017-09-08 03:41 UTC] social media photo (Twitter), posted 2017-09-08 03:41 UTC
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.0, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.2 of the questions; final memory 4 lines / 487 tokens; budget fallbacks 2).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=3, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* invalid_citation | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence stored at step 1, deleted at step 6
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What type of disaster is depicted in the image? Flood; What is the condition of the roads in the image? Completely flooded
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: flooded area | evidence stored at step 3, deleted at step 10
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* abstained_evidence_missing | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 7
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* invalid_citation | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: No | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* wrong_answer_evidence_in_memory | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 8)
  memory about E08: social media photo (Twitter), posted 2017-09-19 19:20 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/92; 2:2/184; 3:2/256; 4:3/371; 5:4/486; 6:4/461/budget_evict_oldest; 7:2/257; 8:3/372; 9:4/487; 10:4/487/budget_evict_oldest
FINAL MEMORY:
  m7 [src E07] m7 [src E07 @2017-09-19 18:40 UTC] social media photo (Twitter), posted 2017-09-19 18:40 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
  m8 [src E08] social media photo (Twitter), posted 2017-09-19 19:20 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
  m9 [src E09] social media photo (Twitter), posted 2017-09-19 19:51 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.
  m10 [src E10] social media photo (Twitter), posted 2017-09-19 20:20 UTC, depicting a flooded area with submerged buildings, vehicles, and trees, indicating severe flooding. The image shows a large parking lot with cars partially submerged, surrounded by greenery and residential structures in the background. The water appears murky and brown, suggesting possible contamination or sediment. No people are visible in the image.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 496 tokens; budget fallbacks 4).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 7
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Floodwaters | evidence stored at step 4, deleted at step 8
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 10
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* unnecessary_abstention | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: m8 [src E08 @2015-12-04 07:54 UTC] A social media photo from Twitter, posted on 2015-12-04 07:54 UTC, depicting a flooded area with a group of people and military personnel in a green boat, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals and soldiers navigating through the floodwaters.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: m10 [src E10 @2015-12-04 17:45 UTC] A social media photo from Twitter, posted on 2015-12-04 17:45 UTC, depicting a flooded area with a group of people wading through muddy water, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals navigating through the floodwaters.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/98; 2:2/178; 3:2/196; 4:3/294; 5:4/397; 6:5/493; 7:4/448/budget_evict_oldest; 8:4/475/budget_evict_oldest; 9:4/494/budget_evict_oldest; 10:4/496/budget_evict_oldest
FINAL MEMORY:
  m7 [src E07] m7 [src E07 @2015-12-04 04:24 UTC] A social media photo from Twitter, posted on 2015-12-04 04:24 UTC, depicting a flooded area with a group of people and military personnel in a green boat, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals and soldiers navigating through the floodwaters.
  m8 [src E08] m8 [src E08 @2015-12-04 07:54 UTC] A social media photo from Twitter, posted on 2015-12-04 07:54 UTC, depicting a flooded area with a group of people and military personnel in a green boat, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals and soldiers navigating through the floodwaters.
  m9 [src E09] m9 [src E09 @2015-12-04 08:05 UTC] A social media photo from Twitter, posted on 2015-12-04 08:05 UTC, depicting a flooded area with a group of people wading through muddy water, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals navigating through the floodwaters.
  m10 [src E10] m10 [src E10 @2015-12-04 17:45 UTC] A social media photo from Twitter, posted on 2015-12-04 17:45 UTC, depicting a flooded area with a group of people wading through muddy water, surrounded by trees and vegetation. The image shows the aftermath of a natural disaster, with individuals navigating through the floodwaters.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 5 lines / 460 tokens; budget fallbacks 3).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 10
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* wrong_answer_evidence_in_memory | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 8)
  memory about E08: m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: m10 [src E10 @2017-09-21 10:48 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:48 UTC, depicting a collapsed building with a dog navigating through debris and scattered personal items.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/70; 2:2/239; 3:2/290; 4:3/445; 5:3/445; 6:3/222/budget_evict_oldest; 7:4/319; 8:5/416; 9:5/442/budget_evict_oldest; 10:5/460/budget_evict_oldest
FINAL MEMORY:
  m5 [src E06] A social media photo from Twitter, posted on 2017-09-21 at 07:16 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
  m6 [src E07] m7 [src E07 @2017-09-21 08:35 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:35 UTC, depicting a collapsed building with a car partially buried in debris in the foreground.
  m7 [src E08] m8 [src E08 @2017-09-21 08:44 UTC] A social media photo from Twitter, posted on 2017-09-21 at 08:44 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
  m8 [src E09] m9 [src E09 @2017-09-21 10:33 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:33 UTC, depicting a collapsed building with individuals in safety gear and civilians observing the aftermath.
  m9 [src E10] m10 [src E10 @2017-09-21 10:48 UTC] A social media photo from Twitter, posted on 2017-09-21 at 10:48 UTC, depicting a collapsed building with a dog navigating through debris and scattered personal items.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.0; evidence still in memory for 0.8 of the questions; final memory 6 lines / 498 tokens; budget fallbacks 2).
OUTCOMES: correct=1, unsupported=2, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: A (None) | evidence stored at step 1, deleted at step 8
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* unsupported | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: Dry vegetation | evidence in memory (stored at step 6)
  memory about E06: A social media photo posted on Twitter on October 18, 2017, at 07:23 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
  evaluator: unsupported - The evidence states that the primary material burning is trees, not dry vegetation.
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: m9 [src E09 @2017-10-19 07:36 UTC] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: m10 [src E10 @2017-10-20 11:11 UTC] A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/75; 2:2/149; 3:2/149; 4:3/223; 5:4/297; 6:5/370; 7:6/444; 8:6/470/budget_evict_oldest; 9:6/470; 10:6/498/budget_evict_oldest
FINAL MEMORY:
  m4 [src E04] A social media photo posted on Twitter on October 12, 2017, at 08:25 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  m5 [src E05] A social media photo posted on Twitter on October 17, 2017, at 16:04 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  m6 [src E06] A social media photo posted on Twitter on October 18, 2017, at 07:23 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  m7 [src E07] A social media photo posted on Twitter on October 18, 2017, at 20:21 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  m9 [src E09] m9 [src E09 @2017-10-19 07:36 UTC] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.
  m10 [src E10] m10 [src E10 @2017-10-20 11:11 UTC] A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC, depicting a wildfire scene with flames consuming dry vegetation and individuals observing the fire from a distance.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.6 of the questions; final memory 7 lines / 470 tokens; budget fallbacks 2).
OUTCOMES: abstained_evidence_missing=2, correct=1, unnecessary_abstention=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 1, deleted at step 5
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 10
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* unnecessary_abstention | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: social media photo (web), posted 2017-06-25 00:20 UTC
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: social media photo (web), posted 2017-07-21 00:43 UTC
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/88; 2:2/193; 3:2/290; 4:3/435; 5:3/156/budget_evict_oldest; 6:4/208; 7:5/286; 8:6/364; 9:7/442; 10:7/470/budget_evict_oldest
FINAL MEMORY:
  m4 [src E04] social media photo (web), posted 2017-06-25 00:20 UTC
  m5 [src E05] social media photo (web), posted 2017-06-25 21:15 UTC
  m6 [src E06] social media photo (web), posted 2017-07-21 00:43 UTC
  m7 [src E07] m7 [src E07 @2017-08-23 00:46 UTC] social media photo (web), posted 2017-08-23 00:46 UTC
  m8 [src E08] m8 [src E08 @2017-08-28 10:43 UTC] social media photo (Twitter), posted 2017-08-28 10:43 UTC
  m9 [src E09] m9 [src E09 @2017-09-06 09:22 UTC] social media photo (Twitter), posted 2017-09-06 09:22 UTC
  m10 [src E10] m10 [src E10 @2017-09-08 03:41 UTC] social media photo (Twitter), posted 2017-09-08 03:41 UTC
```
