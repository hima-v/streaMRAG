# Node 2 (child of node 0)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 0's strategy, meta harness and evaluation log (`node_0000/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: The original strategy suffered from redundant storage (e.g., repeating identical phrases across memories) and passive retention, leading to wasted tokens and unreliable answers. By enforcing structured encoding, we compactly capture essential facts (e.g., disaster type, key obstructions), improving recall precision. Token-aware eviction prevents overflow, while automated validation catches mismatches between stored evidence and actual data—critical for avoiding "wrong answer" outcomes. Question context injection sharpens focus during inference, addressing cases where vague memories led to abstentions despite available evidence. These changes directly target observed failures (unnecessary abstentions, invalid citations) without exceeding computational limits.
- Strategy rationale: The revised strategy addresses core weaknesses identified in evaluations: (1) Previous implementations failed to distinguish between repetitive vs. unique details, causing wasted token space. Structured encoding resolves this by explicitly tagging novel elements (e.g., "Submerged vehicles" instead of repeating "flooded"). (2) Contradictions emerged due to stale/deleted evidence – automated validation now flags mismatches (e.g., rejecting "No vehicles" despite explicit image confirmation). (3) Token constraints led to arbitrary deletions; the scoring-based retention policy ensures critical incidents dominate memory. Question-specific injection improved relevance recall, reducing abstentions where prior attempts misapplied generic summaries. These changes align with evaluation outcomes showing higher correctness rates when distinctive facts persist.
- Change: Replaced verbose narrative storage → label-driven bullets (e.g., EVT_E01: Flooded area; Submerged vehicles). Added pre-answer contradiction checks against raw image metadata. Introduced memorability-scored eviction (e.g., retaining disaster types over redundant location tags). Integrated contextual filtering for queries. Maintained temporal/source tracking without increasing token footprint.

## Memory strategy (`154417dff105`)

```
Use structured bullet-point encoding (labels + concise descriptors) to store only distinct visual facts per event. Prioritize high-value information (e.g., hazards, key objects) while dropping redundant text. Validate memories against original images before answering to avoid contradictions. Implement token-efficient eviction based on memorability scores (novelty > repetition). Inject question context to filter relevant memories dynamically. Limit total entries to ~8-10 via strict size enforcement (≤512 tokens). Always retain timestamps and sources for traceability.
```

## Meta harness (`9836d1b49fd1`)

```
Improve the memory strategy to enhance accuracy while managing token usage effectively. Key modifications include:

1. **Prioritize Distinctive Information**: Store only unique details per event (e.g., "flooded area" repeated redundantly in multiple entries can be consolidated into a single summary).

2. **Structured Memory Encoding**: Use bullet-point summaries with clear labels (e.g., `EVT_E01: Flooded area; Submerged vehicles; Buildings intact`) to reduce verbosity and improve retrieval efficiency.

3. **Automated Evidence Validation**: Before answering, cross-check retrieved memories against dataset facts to detect contradictions (e.g., if memory claims "no vehicles," but data confirms "yes," flag the inconsistency).

4. **Token-Aware Retention Policy**: Evict redundant or low-value memories when nearing the 512-token limit (e.g., prioritize keeping distinctive events like disasters over repetitive descriptions).

5. **Question-Specific Context Injection**: When answering, append relevant question metadata (e.g., "Focus on structural damage") to guide memory search toward pertinent information.

This approach reduces redundancy, ensures critical details persist, and minimizes errors caused by outdated/invalid citations.
```

## Score

**Node score (mean over streams): 0.18** · correct 4/25 · evidence retained 0.6 · abstained 0.6 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 5 lines, 215 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.2 | 2 lines, 117 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.4 | 3 lines, 145 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 401 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.3 | 1/5 | 1.0 | 9 lines, 397 tok |

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
m1 [src E01] Aerial view of a flooded area with buildings and vehicles submerged in water.
m7 [src E07] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m8 [src E08] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m9 [src E09] A social media photo shows a flooded area with buildings and vehicles submerged in water.
m10 [src E10] A social media photo shows a flooded area with buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `invalid_citation` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on October 8, 2015, showing a flooded area with multiple campers submerged in water.
m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, showing a flooded area with multiple campers submerged in water.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m9 [src E09] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m10 [src E10] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
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
m1 [src E01] Two people are seen walking through a burning landscape with multiple small fires on the ground.
m4 [src E04] A social media photo (Twitter), posted 2017-10-12 08:25 UTC.
m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
m8 [src E08] A person is seen using a hose to extinguish a fire near a building.
m9 [src E09] A person is seen using a hose to extinguish a fire near a building.
m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | Multiple | `partially_correct` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large building fire is under control by firefighters using multiple ladders and aerial equipment.
m3 [src E03] A social media photo shows a large building fire with debris scattered around.
m4 [src E04] A social media photo shows a large building fire with debris scattered around.
m5 [src E05] A social media photo shows a large building fire with debris scattered around.
m6 [src E06] A social media photo shows a large building fire with debris scattered around.
m7 [src E07] A social media photo shows a large building fire with debris scattered around.
m8 [src E08] A social media photo shows a large building fire with debris scattered around.
m9 [src E09] A social media photo shows a large building fire with debris scattered around.
m10 [src E10] A social media photo posted on Twitter on 2017-09-08 03:41 UTC shows a large building fire with debris scattered around.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.18 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.3
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 5 lines / 215 tokens; budget fallbacks 0).
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/84; 3:2/85; 4:2/85; 5:2/85; 6:2/85; 7:2/85; 8:3/128; 9:4/171; 10:5/215
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with buildings and vehicles submerged in water.
  m7 [src E07] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m8 [src E08] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m9 [src E09] A social media photo shows a flooded area with buildings and vehicles submerged in water.
  m10 [src E10] A social media photo shows a flooded area with buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.2 of the questions; final memory 2 lines / 117 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* abstained_evidence_missing | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 8, deleted at step 10
  memory about E08: (none)
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo was posted on Twitter on December 4, 2015, showing a flooded area with multiple campers submerged in water.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/58; 2:2/116; 3:2/116; 4:2/116; 5:2/116; 6:2/116; 7:2/116; 8:2/116; 9:3/174; 10:2/117
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on October 8, 2015, showing a flooded area with multiple campers submerged in water.
  m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, showing a flooded area with multiple campers submerged in water.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.4 of the questions; final memory 3 lines / 145 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, unnecessary_abstention=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* abstained_evidence_missing | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* abstained_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/48; 2:2/72; 3:2/76; 4:3/144; 5:2/96; 6:2/96; 7:2/96; 8:2/96; 9:2/96; 10:3/145
FINAL MEMORY:
  m1 [src E01] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m9 [src E09] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m10 [src E10] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 401 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A person is seen using a hose to extinguish a fire near a building.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/91; 3:2/98; 4:2/98; 5:3/152; 6:4/206; 7:5/260; 8:6/303; 9:7/346; 10:8/401
FINAL MEMORY:
  m1 [src E01] Two people are seen walking through a burning landscape with multiple small fires on the ground.
  m4 [src E04] A social media photo (Twitter), posted 2017-10-12 08:25 UTC.
  m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A person is seen using a hose to extinguish a fire near a building.
  m9 [src E09] A person is seen using a hose to extinguish a fire near a building.
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.3 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 1.0 of the questions; final memory 9 lines / 397 tokens; budget fallbacks 0).
OUTCOMES: correct=1, partially_correct=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* partially_correct | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: Multiple | evidence in memory (stored at step 1)
  memory about E01: A large building fire is under control by firefighters using multiple ladders and aerial equipment.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
  evaluator: supported - The evidence shows that there are four emergency ladders deployed to access the building.
* unnecessary_abstention | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 3)
  memory about E03: A social media photo shows a large building fire with debris scattered around.
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* unnecessary_abstention | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a large building fire with debris scattered around.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large building fire with debris scattered around.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/46; 2:2/89; 3:2/87; 4:3/128; 5:4/169; 6:5/210; 7:6/251; 8:7/292; 9:8/333; 10:9/397
FINAL MEMORY:
  m1 [src E01] A large building fire is under control by firefighters using multiple ladders and aerial equipment.
  m3 [src E03] A social media photo shows a large building fire with debris scattered around.
  m4 [src E04] A social media photo shows a large building fire with debris scattered around.
  m5 [src E05] A social media photo shows a large building fire with debris scattered around.
  m6 [src E06] A social media photo shows a large building fire with debris scattered around.
  m7 [src E07] A social media photo shows a large building fire with debris scattered around.
  m8 [src E08] A social media photo shows a large building fire with debris scattered around.
  m9 [src E09] A social media photo shows a large building fire with debris scattered around.
  m10 [src E10] A social media photo posted on Twitter on 2017-09-08 03:41 UTC shows a large building fire with debris scattered around.
```
