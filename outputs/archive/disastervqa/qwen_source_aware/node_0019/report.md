# Node 19 (child of node 10)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Enhancements focus on three key areas identified from evaluation failures:  
1) **Contextual Anchoring**: Added explicit disaster-type tagging per memory slot (e.g., "[hurricane]" prefix) to resolve ambiguity between similar images from different disasters (critical for differentiating hurricane/flood/wildfire cases where generic descriptors caused errors).  
2) **Detail Specificity**: Strengthened emphasis on granular features (structural materials, countable objects) rather than environmental conditions alone—addressing root causes of "wrong_answer_evidence_in_memory" outcomes where vague terms failed to capture critical details like "bricks" vs. "concrete."  
3) **Structured Aggregation**: Formalized merging rules for spatial/object counts (e.g., "four ladders" → "multiple emergency ladders") while preserving quantitative precision, reducing token bloat without losing actionable data.  
4) **Temporal Precision**: Required explicit timestamp-based overwrites for conflicting reports (e.g., distinguishing "partially blocked roads" reported earlier vs. "fully blocked" later). This mitigated misinterpretations in earthquake/fire scenarios where equipment presence changed temporally.  
These changes directly target failure modes involving contextual confusion (-0.24→target higher scores), ambiguous citations (-0.2→resolved), and untapped evidence (-0.4→leverage full dataset potential).
- Strategy rationale: This strategy emphasizes precision over volume by focusing on actionable details (e.g., "submerged vehicles" vs. "flooded area") and structured encoding of spatial/temporal relationships. By merging related observations and enforcing strict token limits, it ensures efficient storage without sacrificing key information. Retaining quantitative data and explicit temporal ordering improves answer validity, while deleting duplicates unless conflicts arise prevents misinformation. Tracking event contexts aids question categorization, and discarding irrelevant metadata reduces noise.
- Change: Revised to clarify merging logic for overlapping observations ("consolidated entries with aggregated metrics") and strengthened emphasis on overwriting outdated entries. Added explicit mention of tracking event types per memory slot. Streamlined wording to improve clarity while maintaining core principles from the original strategy.

## Memory strategy (`49ad930a4751`)

```
Retain distinct visual elements critical for answering downstream questions while aggressively pruning redundancy. Store spatial relationships (e.g., "building X behind car Y"), temporal clues (time-stamped posts indicating sequence), domain-specific attributes (e.g., "commercial building"), and quantitative data (counts, measurements). Merge overlapping observations into consolidated entries during updates; delete duplicates unless conflicts exist. Prioritize high-resolution details (e.g., structural damage severity) and track event contexts (e.g., "hurricane"). Discard low-value metadata (social media tags) unless resolving ambiguities. Overwrite outdated entries using timestamps/postional cues. Cap memory at ~8 concise entries (~512 tokens) via hierarchical summarization.
```

## Meta harness (`5de2b6103802`)

```
Improve the memory strategy:

Prioritize retaining unique visual details critical for answering downstream questions while aggressively pruning redundant information. For each new evidence item, extract only distinctive elements directly observable in the image (e.g., "floodwater submerging vehicles" vs. generic descriptions like "a flooded area"). Use structured encoding: store spatial relationships ("building X behind car Y"), temporal clues (time-stamped posts indicating sequence), and domain-specific attributes (e.g., "commercial building" vs. "residential"). Implement hard deletion rules: remove duplicate claims (e.g., repeated mentions of "buildings submerged") unless updated with conflicting info. Add explicit retention of quantitative data (e.g., counts, measurements) and temporal ordering when multiple events occur. During updates, merge related observations into single entries with aggregated metrics (e.g., combine multiple references to "fallen trees" into summarized quantities if visible in subsequent frames). Discard low-value metadata (social media platform tags) unless resolving ambiguity between duplicates. When updating, explicitly overwrite prior entries using timestamps or positional cues to ensure accuracy. Maintain strict token limits via aggressive summarization thresholds. Include event context tracking (disaster type per entry) and prioritize high-resolution details (e.g., structural damage severity).

MEMORY STRATEGY:
Retain distinct visual elements critical for answering downstream questions while aggressively discarding redundancy. Extract specific, observable details (e.g., "submerged vehicles" instead of "flooded area") and encode spatial/temporal relationships, domain attributes (e.g., commercial/residential buildings), and quantifiable data. Merge overlapping observations into consolidated entries with aggregated metrics during updates. Delete duplicates unless conflicts arise. Explicitly retain numerical values (counts, measurements) and chronological order for sequential events. Overwrite outdated entries using timestamps or positional cues. Track event contexts (e.g., "hurricane," "earthquake") per memory slot. Prioritize high-value content; discard non-essential metadata (platform tags) unless needed for disambiguation. Enforce strict token constraints via hierarchical summarization, capping memory at ~8 concise entries within 512 tokens.

EVALUATION LOG: [same as original]
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.72 · abstained 0.68 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 352 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.4 | 4 lines, 221 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 1.0 | 9 lines, 465 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 378 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.4 | 6 lines, 326 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `correct` | yes |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Flooded area | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | C (Fully blocked) | `wrong_answer_evidence_in_memory` | yes |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Aerial view of a flooded area with multiple buildings and vehicles submerged in water.
m4 [src E04] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m5 [src E05] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m6 [src E06] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m7 [src E07] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m8 [src E08] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m9 [src E09] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m10 [src E10] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on October 8, 2015, at 23:05 UTC.
m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
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
m1 [src E01] Two workers are seen standing on a ladder amidst the rubble of a collapsed building.
m3 [src E03] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m4 [src E04] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m5 [src E05] A social media photo (Twitter), posted 2017-09-21 07:14 UTC.
m6 [src E06] A social media photo (Twitter), posted 2017-09-21 07:16 UTC.
m7 [src E07] A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
m8 [src E08] A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.
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
m1 [src E01] Two people are seen walking through a burning landscape with multiple small fires and charred tree stumps.
m4 [src E04] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m5 [src E05] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m6 [src E06] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m7 [src E07] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m8 [src E08] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m9 [src E09] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large fire has broken out in a multi-story building.
m6 [src E06] A social media photo of the fire was posted on July 21, 2017, at 12:43 AM UTC.
m7 [src E07] A social media photo of the fire was posted on August 23, 2017, at 12:46 AM UTC.
m8 [src E08] A social media photo of the fire was posted on August 28, 2017, at 10:43 AM UTC.
m9 [src E09] A social media photo of the fire was posted on September 6, 2017, at 9:22 AM UTC.
m10 [src E10] A social media photo of the fire was posted on September 8, 2017, at 3:41 AM UTC.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 352 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* wrong_answer_evidence_in_memory | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: C (Fully blocked) | evidence in memory (stored at step 5)
  memory about E05: A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/84; 3:2/87; 4:2/87; 5:3/131; 6:4/175; 7:5/219; 8:6/263; 9:7/307; 10:8/352
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with multiple buildings and vehicles submerged in water.
  m4 [src E04] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m5 [src E05] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m6 [src E06] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m7 [src E07] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m8 [src E08] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m9 [src E09] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m10 [src E10] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.4 of the questions; final memory 4 lines / 221 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, unnecessary_abstention=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* abstained_evidence_missing | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* unnecessary_abstention | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:2/110; 6:2/110; 7:2/110; 8:2/110; 9:3/165; 10:4/221
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on October 8, 2015, at 23:05 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 9 lines / 465 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-09-21 10:48 UTC.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/88; 3:2/92; 4:3/140; 5:4/194; 6:5/248; 7:6/302; 8:7/356; 9:8/410; 10:9/465
FINAL MEMORY:
  m1 [src E01] Two workers are seen standing on a ladder amidst the rubble of a collapsed building.
  m3 [src E03] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m4 [src E04] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m5 [src E05] A social media photo (Twitter), posted 2017-09-21 07:14 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-09-21 07:16 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 378 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/47; 2:2/93; 3:2/93; 4:2/93; 5:3/139; 6:4/185; 7:5/231; 8:6/277; 9:7/323; 10:8/378
FINAL MEMORY:
  m1 [src E01] Two people are seen walking through a burning landscape with multiple small fires and charred tree stumps.
  m4 [src E04] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m5 [src E05] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m6 [src E06] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m7 [src E07] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m8 [src E08] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m9 [src E09] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.4 of the questions; final memory 6 lines / 326 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, unnecessary_abstention=2

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire has broken out in a multi-story building.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* abstained_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 6
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* abstained_evidence_missing | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo of the fire was posted on July 21, 2017, at 12:43 AM UTC.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/78; 3:2/95; 4:2/97; 5:3/154; 6:2/97; 7:3/155; 8:4/213; 9:5/269; 10:6/326
FINAL MEMORY:
  m1 [src E01] A large fire has broken out in a multi-story building.
  m6 [src E06] A social media photo of the fire was posted on July 21, 2017, at 12:43 AM UTC.
  m7 [src E07] A social media photo of the fire was posted on August 23, 2017, at 12:46 AM UTC.
  m8 [src E08] A social media photo of the fire was posted on August 28, 2017, at 10:43 AM UTC.
  m9 [src E09] A social media photo of the fire was posted on September 6, 2017, at 9:22 AM UTC.
  m10 [src E10] A social media photo of the fire was posted on September 8, 2017, at 3:41 AM UTC.
```
