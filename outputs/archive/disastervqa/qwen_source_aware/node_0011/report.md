# Node 11 (child of node 10)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Current strategy fails due to insufficient contextual specificity and poor temporal management. Modifications add: 
1. Timestamp-based overwriting logic to resolve contradictions (fixes hurricane/flood case where recent photos showed intact roads contradicting earlier reports)
2. Structured JSON formatting enabling precise field extraction (addresses earthquake example's missing debris material tracking)
3. Tiered summarization preventing token bloat (explains better performance in wildfire scenario with complex sequences)
4. Conflict validation reducing false negatives (would have caught misattributed railway/residential classification in flood test)

These changes align with evaluation failures showing sensitivity to timing/order discrepancies and difficulty aggregating quantitative details across iterations. The proposed framework would maintain higher fidelity evidence traces while meeting strict memory constraints.
- Strategy rationale: This strategy improves upon prior implementations by explicitly codifying conflict resolution criteria (timestamp priority → spatial proximity), enforcing numerical aggregation for quantitative consistency, and enhancing contextual linkage for downstream reasoning. Structured JSON formatting ensures machine-readable persistence of critical fields. Validation steps prevent contradictory data accumulation, addressing past failures where incorrect evidence persisted (e.g., misattributing flood effects to earthquakes). Token efficiency gains stem from eliminating redundant qualitative descriptors while preserving quantified truths. Spatial-temporal indexing aligns with evaluation outcomes showing improved question alignment post-correction (e.g., correctly identifying earthquake-affected materials despite initial noise).
- Change: 1. Added explicit timestamp/spatial priority hierarchy for overwrites
- Change: 2. Implemented numerical vs. descriptive aggregation distinction based on observation type
- Change: 3. Enhanced multi-modal indexing requirements (e.g., combining structural damage with environmental patterns)
- Change: 4. Strengthened validation checks to flag contradicting entries pre-merging
- Change: 5. Refined spatial ambiguity resolution protocol (earliest version retained without clear proximity winner)
- Change: 6. Reduced descriptive detail threshold from <20 to <15 tokens for aggressive pruning
- Change: 7. Introduced location adjacency scoring system for spatial conflict scenarios

## Memory strategy (`e882d6133cb8`)

```
Explicitly handle timestamp-based conflict resolution by retaining temporally latest or spatially closest versions of recurring observations. For quantitative data, enforce stricter aggregation rules requiring identical observation_type and location to merge quantities numerically rather than descriptively. Enhance spatial-temporal indexing to prioritize multi-modal context (e.g., linking roof damage to debris patterns). Structure entries as JSON-like objects with mandatory fields: id, src, timestamp, observation_type, location, quantity, description. During updates, compare new observations against existing entries: overwrite if newer timestamp overrides older data, but preserve unique spatial features unless fully superseded. Discard redundant descriptions under 20 tokens; aggregate quantitative data into consolidated entries. Validate additions by checking for conflicting information (e.g., differing disaster types between versions of the same event) before merging. Prioritize retention of quantitative metrics (e.g., counts, measurements) and temporal sequence integrity. Cap memory at ~8 concise entries (~512 tokens) via hierarchical summarization, deleting intermediate tiers while preserving raw visual details and validated aggregates. Use location proximity thresholds to resolve spatial ambiguities, favoring the earliest entry if no clear closest match exists.
```

## Meta harness (`665ed7408d3b`)

```
Improve the memory strategy by adding explicit handling of timestamp-based conflict resolution, stricter aggregation rules for quantitative data, and enhanced spatial-temporal indexing. Retain only temporally latest or spatially closest versions of recurring observations. Structure entries as JSON-like objects with fields: {id, src, timestamp, observation_type, location, quantity, description}. Implement tiered summarization: keep raw visual details (<20 tokens) + aggregated stats (>20 tokens merged), delete intermediate summaries. Add explicit validation step comparing current observation against existing entries before storage—discard identical entries unless new data (quantities, locations, timestamps) alters conclusions. Prioritize multi-modal context preservation (e.g., "roof damage + debris distribution pattern").
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.72 · abstained 0.52 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 365 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 326 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.2 | 2 lines, 129 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.2 | 1/5 | 1.0 | 9 lines, 433 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 481 tok |

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
m1 [src E01] Aerial view of flooded area with multiple buildings and vehicles submerged in water.
m4 [src E04] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
m5 [src E05] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
m6 [src E06] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
m7 [src E07] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
m8 [src E08] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
m9 [src E09] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
m10 [src E10] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `correct` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | D (Residential area) | `wrong_answer_evidence_in_memory` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A flooded campsite with multiple RVs submerged in muddy water.
m4 [src E04] A flooded campsite with multiple RVs submerged in muddy water.
m5 [src E05] A man is swimming in the water holding a rope.
m6 [src E06] A flooded campsite with multiple RVs submerged in muddy water.
m7 [src E07] A flooded campsite with multiple RVs submerged in muddy water.
m8 [src E08] A flooded campsite with multiple RVs submerged in muddy water.
m9 [src E09] A flooded campsite with multiple RVs submerged in muddy water.
m10 [src E10] A flooded campsite with multiple RVs submerged in muddy water.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `invalid_citation` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo from 2017-09-21 04:40 UTC shows a scene of a collapsed building with two workers on a ladder.
m10 [src E10] A social media photo from 2017-09-21 10:48 UTC shows a scene of a collapsed building with two workers on a ladder.
```

## Stream `dvqa-wildfire-len10-064` ([evaluation.md](runs/dvqa-wildfire-len10-064/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many people are visible in the image? Select all that apply. | C (Two) | A (None) | `wrong_answer_evidence_in_memory` | yes |
| E06 | What is the primary material burning? Answer with one or two words. | Trees | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | `correct` | yes |
| E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | `unsupported` | yes |
| E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A social media photo (Twitter), posted 2017-10-12 03:11 UTC.
m3 [src E03] A social media photo shows a burning landscape with flames and smoke.
m4 [src E04] A social media photo shows a burning landscape with flames and smoke.
m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
m9 [src E09] ...
m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | C (High-rise) | `wrong_answer_evidence_in_memory` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large fire has broken out in a multi-story building, with multiple fire trucks and emergency responders on the scene. The building is surrounded by smoke and flames, and several fire trucks are extended with ladders to the building's windows and balconies. There are many firefighters and paramedics present, working to extinguish the fire and provide medical assistance. The scene is chaotic and intense, with lights flashing and sirens blaring.
m4 [src E04] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
m5 [src E05] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
m6 [src E06] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
m7 [src E07] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
m8 [src E08] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
m9 [src E09] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
m10 [src E10] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 365 tokens; budget fallbacks 0).
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
  memory about E05: A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/88; 3:2/88; 4:2/88; 5:3/134; 6:4/180; 7:5/226; 8:6/272; 9:7/318; 10:8/365
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with multiple buildings and vehicles submerged in water.
  m4 [src E04] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  m5 [src E05] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  m6 [src E06] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  m7 [src E07] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  m8 [src E08] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  m9 [src E09] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.
  m10 [src E10] A social media photo from Twitter shows a flooded area with multiple buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 326 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A flooded campsite with multiple RVs submerged in muddy water.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: A flooded campsite with multiple RVs submerged in muddy water.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A flooded campsite with multiple RVs submerged in muddy water.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/79; 3:2/82; 4:2/82; 5:3/120; 6:4/161; 7:5/202; 8:6/243; 9:7/284; 10:8/326
FINAL MEMORY:
  m1 [src E01] A flooded campsite with multiple RVs submerged in muddy water.
  m4 [src E04] A flooded campsite with multiple RVs submerged in muddy water.
  m5 [src E05] A man is swimming in the water holding a rope.
  m6 [src E06] A flooded campsite with multiple RVs submerged in muddy water.
  m7 [src E07] A flooded campsite with multiple RVs submerged in muddy water.
  m8 [src E08] A flooded campsite with multiple RVs submerged in muddy water.
  m9 [src E09] A flooded campsite with multiple RVs submerged in muddy water.
  m10 [src E10] A flooded campsite with multiple RVs submerged in muddy water.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.2 of the questions; final memory 2 lines / 129 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, invalid_citation=1, unnecessary_abstention=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* invalid_citation | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* abstained_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* abstained_evidence_missing | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 9, deleted at step 10
  memory about E09: (none)
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo from 2017-09-21 10:48 UTC shows a scene of a collapsed building with two workers on a ladder.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/64; 2:2/128; 3:2/128; 4:2/128; 5:2/128; 6:2/128; 7:2/128; 8:2/128; 9:2/128; 10:2/129
FINAL MEMORY:
  m1 [src E01] A social media photo from 2017-09-21 04:40 UTC shows a scene of a collapsed building with two workers on a ladder.
  m10 [src E10] A social media photo from 2017-09-21 10:48 UTC shows a scene of a collapsed building with two workers on a ladder.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 9 lines / 433 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_in_memory | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: A (None) | evidence in memory (stored at step 1)
  memory about E01: A social media photo (Twitter), posted 2017-10-12 03:11 UTC.
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: ...
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/81; 3:2/81; 4:3/121; 5:4/175; 6:5/229; 7:6/283; 8:7/337; 9:8/352; 10:9/433
FINAL MEMORY:
  m1 [src E01] A social media photo (Twitter), posted 2017-10-12 03:11 UTC.
  m3 [src E03] A social media photo shows a burning landscape with flames and smoke.
  m4 [src E04] A social media photo shows a burning landscape with flames and smoke.
  m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m9 [src E09] ...
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 481 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire has broken out in a multi-story building, with multiple fire trucks and emergency responders on the scene. The building is surrounded by smoke and flames, and several fire trucks are extended with ladders to the building's windows and balconies. There are many firefighters and paramedics present, working to extinguish the fire and provide medical assistance. The scene is chaotic and intense, with lights flashing and sirens blaring.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_in_memory | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: C (High-rise) | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/116; 2:2/168; 3:2/168; 4:2/168; 5:3/220; 6:4/272; 7:5/324; 8:6/376; 9:7/428; 10:8/481
FINAL MEMORY:
  m1 [src E01] A large fire has broken out in a multi-story building, with multiple fire trucks and emergency responders on the scene. The building is surrounded by smoke and flames, and several fire trucks are extended with ladders to the building's windows and balconies. There are many firefighters and paramedics present, working to extinguish the fire and provide medical assistance. The scene is chaotic and intense, with lights flashing and sirens blaring.
  m4 [src E04] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  m5 [src E05] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  m6 [src E06] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  m7 [src E07] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  m8 [src E08] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  m9 [src E09] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
  m10 [src E10] A social media photo shows the fire scene with a firefighter standing on top of a fire truck, observing the blaze.
```
