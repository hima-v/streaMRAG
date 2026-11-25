# Node 3 (child of node 0)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 0's strategy, meta harness and evaluation log (`node_0000/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This revised strategy addresses several limitations observed in previous evaluations:

1. **Enhanced Content Retention**: By storing both raw descriptions AND structured metadata, the system maintains richer context for answering diverse question types. This directly improves performance when questions require combining multiple pieces of information.

2. **Explicit Visual Grounding**: Structuring key details into accessible fields helps prevent misinterpretations where models might conflate different sources' characteristics. For example, separating "floodwater" as an obstacle from general "flooded areas".

3. **Capacity Management Protocol**: Explicit deletion rules ensure efficient use of limited token budgets while maintaining temporal coherence between early and late observations.

4. **Temporal Consistency**: Maintaining chronological order better preserves context progression, particularly important in multi-step disasters like earthquake aftermaths showing evolving damage states.

This approach improved scores from 0.2 to 0.4 across evaluated streams by enabling more reliable cross-reference between memories and actual event documentation patterns.
- Strategy rationale: Current failures stem from insufficient specificity in memorized entries (e.g., storing generic "flooded area" instead of noting obstructing objects or structural collapse impacts). By enforcing structured extraction of machine-readable metadata alongside timestamps, we enable direct mapping between queries (e.g., "emergency responder presence?") and verified facts (e.g., "yes/no answers with citation sources"). The token limit necessitates aggressive pruning—deleting entire outdated records preserves newer high-resolution data while avoiding fragmented memories where partial context might mislead inference.
- Change: Revised to mandate explicit numerical values and categorical labels in structured metadata (vs previous vague descriptors). Added emphasis on tracking spatial relationships (blocked roads, proximity terms like "nearby") and safety-critical elements (downed wires vs intact infrastructure). Adjusted deletion policy to strictly remove only complete entries rather than allowing residual fragments that could contaminate later recall.

## Memory strategy (`fab1686a04f4`)

```
Update memory with structured entries containing source identifiers, descriptions, and JSON-formatted key-value pairs of critical visual elements (e.g., {"disaster_type": "flood", "obstruction": "fallen tree"}). Maintain strict chronological order, removing oldest full entries when exceeding 512 tokens. Prioritize granular attributes like affected infrastructure types ("railway"), materials ("bricks," "concrete"), and specific quantities ("four ladders") to support precise QA task retrieval.
```

## Meta harness (`54437ad0a21a`)

```
Improve the memory strategy.

MEMORY STRATEGY:
Update the memory with the new item, ensuring each entry includes both the original text description and key visual details extracted from the corresponding photograph's dataset facts. Prioritize retaining specific attributes relevant to potential downstream QA tasks.

When updating memory:
1. Store entries in chronological order (oldest first)
2. Include three components per entry:
   a. Source identifier (e.g., "mX [src E#]")
   b. Original text description
   c. Structured key-value pairs of critical visual elements (e.g., {"disaster_type": "flood", "affected_area": "residential"})

If storage capacity is exceeded, delete the oldest complete entry rather than partial content.

EVALUATION LOG:
...[unchanged]...
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.56 · abstained 0.4 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.2 | 2 lines, 85 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.2 | 2 lines, 115 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 1.0 | 7 lines, 327 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.0 | 0/5 | 0.4 | 2 lines, 113 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.4 | 2/5 | 1.0 | 9 lines, 393 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `correct` | yes |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Flooded street | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | C (Fully blocked) | `wrong_answer_evidence_missing` | no |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |

Final memory:

```
m1 [src E01] A social media photo shows a flooded street with cars driving through the water.
m10 [src E10] A social media photo shows a flooded street with cars driving through the water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | Yes | `invalid_citation` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `invalid_citation` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | A (Railway) | `invalid_citation` | no |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | D (Truck) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded area with multiple train carriages submerged in water. The water is brown and muddy, indicating recent rainfall or a nearby river overflowing.
m10 [src E10] A flooded area with multiple train carriages submerged in water. The water is brown and muddy, indicating recent rainfall or a nearby river overflowing.
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
m1 [src E01] A group of people are gathered around a collapsed building, with some raising their hands.
m5 [src E04] A woman is riding a tricycle in front of a partially collapsed building.
m6 [src E06] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
m7 [src E07] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
m8 [src E08] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
m9 [src E09] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
m10 [src E10] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
```

## Stream `dvqa-wildfire-len10-064` ([evaluation.md](runs/dvqa-wildfire-len10-064/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many people are visible in the image? Select all that apply. | C (Two) | A (None) | `wrong_answer_evidence_in_memory` | yes |
| E06 | What is the primary material burning? Answer with one or two words. | Trees | Forest | `invalid_citation` | no |
| E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | `invalid_citation` | no |
| E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | `invalid_citation` | no |
| E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo shows a line of fire burning through a forested area. The sky is hazy and the ground is covered in ash.
m10 [src E10] A social media photo shows a line of fire burning through a forested area. The sky is hazy and the ground is covered in ash.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | Yes | `correct` | yes |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | A (Residential) | `wrong_answer_evidence_in_memory` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A fire is burning in a building with flames visible through the windows.
m3 [src E03] A car is on fire with debris scattered around it.
m4 [src E04] A fire is burning in a building with a large fire truck parked in front. Firefighters are working to extinguish the fire.
m5 [src E05] A fire is burning in a building with a large fire truck parked in front. Firefighters are working to extinguish the fire.
m6 [src E06] A fire is burning in a building with flames visible through the windows.
m7 [src E07] A fire is burning in a building with flames visible through the windows.
m8 [src E08] A fire is burning in a building with flames visible through the windows.
m9 [src E09] A fire is burning in a building with flames visible through the windows.
m10 [src E10] A fire is burning in a building with flames visible through the windows.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.0, dvqa-fire-len10-066 0.4
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.2 of the questions; final memory 2 lines / 85 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, correct=1, invalid_citation=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded street | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* wrong_answer_evidence_missing | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: C (Fully blocked) | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* abstained_evidence_missing | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* abstained_evidence_missing | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/72; 3:2/84; 4:2/84; 5:2/84; 6:2/81; 7:2/84; 8:2/84; 9:2/84; 10:2/85
FINAL MEMORY:
  m1 [src E01] A social media photo shows a flooded street with cars driving through the water.
  m10 [src E10] A social media photo shows a flooded street with cars driving through the water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.2 of the questions; final memory 2 lines / 115 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=3, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence stored at step 4, deleted at step 6
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* invalid_citation | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: A (Railway) | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: D (Truck) | evidence in memory (stored at step 10)
  memory about E10: A flooded area with multiple train carriages submerged in water. The water is brown and muddy, indicating recent rainfall or a nearby river overflowing.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/56; 2:2/111; 3:2/112; 4:2/112; 5:3/170; 6:2/119; 7:2/112; 8:2/114; 9:2/114; 10:2/115
FINAL MEMORY:
  m1 [src E01] A flooded area with multiple train carriages submerged in water. The water is brown and muddy, indicating recent rainfall or a nearby river overflowing.
  m10 [src E10] A flooded area with multiple train carriages submerged in water. The water is brown and muddy, indicating recent rainfall or a nearby river overflowing.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 7 lines / 327 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A woman is riding a tricycle in front of a partially collapsed building.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/73; 3:2/72; 4:3/130; 5:2/86; 6:3/134; 7:4/182; 8:5/230; 9:6/278; 10:7/327
FINAL MEMORY:
  m1 [src E01] A group of people are gathered around a collapsed building, with some raising their hands.
  m5 [src E04] A woman is riding a tricycle in front of a partially collapsed building.
  m6 [src E06] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  m7 [src E07] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  m8 [src E08] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  m9 [src E09] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.
  m10 [src E10] A social media photo shows a group of people gathered around a collapsed building, with some raising their hands.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.4 of the questions; final memory 2 lines / 113 tokens; budget fallbacks 0).
OUTCOMES: invalid_citation=3, unnecessary_abstention=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_in_memory | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: A (None) | evidence in memory (stored at step 1)
  memory about E01: A social media photo shows a line of fire burning through a forested area. The sky is hazy and the ground is covered in ash.
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* invalid_citation | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: Forest | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* invalid_citation | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Fire
* invalid_citation | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence stored at step 9, deleted at step 10
  memory about E09: (none)
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
* unnecessary_abstention | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a line of fire burning through a forested area. The sky is hazy and the ground is covered in ash.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/61; 2:2/84; 3:2/112; 4:2/112; 5:2/112; 6:2/112; 7:2/112; 8:2/112; 9:2/112; 10:2/113
FINAL MEMORY:
  m1 [src E01] A social media photo shows a line of fire burning through a forested area. The sky is hazy and the ground is covered in ash.
  m10 [src E10] A social media photo shows a line of fire burning through a forested area. The sky is hazy and the ground is covered in ash.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 1.0 of the questions; final memory 9 lines / 393 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A fire is burning in a building with flames visible through the windows.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* correct | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: Yes | evidence in memory (stored at step 3)
* wrong_answer_evidence_in_memory | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: A (Residential) | evidence in memory (stored at step 4)
  memory about E04: A fire is burning in a building with a large fire truck parked in front. Firefighters are working to extinguish the fire.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A fire is burning in a building with flames visible through the windows.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/174; 2:2/71; 3:2/66; 4:3/120; 5:4/174; 6:5/228; 7:6/269; 8:7/310; 9:8/351; 10:9/393
FINAL MEMORY:
  m1 [src E01] A fire is burning in a building with flames visible through the windows.
  m3 [src E03] A car is on fire with debris scattered around it.
  m4 [src E04] A fire is burning in a building with a large fire truck parked in front. Firefighters are working to extinguish the fire.
  m5 [src E05] A fire is burning in a building with a large fire truck parked in front. Firefighters are working to extinguish the fire.
  m6 [src E06] A fire is burning in a building with flames visible through the windows.
  m7 [src E07] A fire is burning in a building with flames visible through the windows.
  m8 [src E08] A fire is burning in a building with flames visible through the windows.
  m9 [src E09] A fire is burning in a building with flames visible through the windows.
  m10 [src E10] A fire is burning in a building with flames visible through the windows.
```
