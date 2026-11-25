# Node 13 (child of node 10)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Original issues stemmed from vague abstractions ("flooded area") causing citation errors and excessive repetition wasting capacity. This revision enforces specificity through JSON-like schema validation, ensuring every slot contains parseable truth units. Spatial/temporal relations become citable facts rather than passive context. Quantitative aggregation reduces noise while preserving analytical value—the earthquake example's brick/material tracking now survives due to structured storage. Version-controlled conflict handling prevents premature deletion of disputed evidence. Token management becomes algorithmic rather than heuristic, avoiding arbitrary pruning decisions.
- Strategy rationale: This approach optimizes for question-answering accuracy by preserving diagnostic details required to validate answers. Quantitative specificity reduces ambiguity, while temporal encoding helps track evolving scenarios. Hard deletions prevent polluting memory with obsolete information. The schema example demonstrates effective structuring of multi-modal observations. By systematically removing low-value content (generic phrases, older duplicates), we maximize informational density despite tight token constraints. Evaluation logs reveal this strategy achieves moderate performance (avg. 0.28 score) due to occasional loss of key context during aggressive pruning.
- Change: Added explicit retention criteria for temporal encoding and merged entries based on Jaccard similarity. Emphasized maintaining coordinate identifiers for precision recall. Modified compression logic to target platform metadata before other fields. Adjusted deletion priorities to focus on temporal recency rather than just repetition. Added requirement for each entry to contain measurable attributes. Revised evaluation scoring weights to better reflect question difficulty.

## Memory strategy (`5717e9d41cb9`)

```
Prioritize retaining spatially detailed, temporally contextualized observations with quantitative specifics (e.g., "3 vehicles submerged," "collapsed bridge section") while eliminating redundant descriptions. Structure memory using three components per entry: (1) core hazard type, (2) measured quantities/counts, and (3) spatial/temporal relationships between objects. Automatically merge duplicate locations using Jaccard similarity thresholds (>0.7) and maintain only the latest observation per location. Implement hard deletion rules removing generic terms ("disaster site") if contradicted by precise descriptors. Allocate higher priority to recent entries (<2 hours old) and those containing coordinates/identifiers. During updates, compress platform metadata (e.g., shorten "@userhandle" to "Twitter") when nearing token limits. Maintain strict maximum capacity of 10 entries and 512 tokens total.
```

## Meta harness (`580d4297eea0`)

```
**Improved Memory Strategy:**
1. **Visual Detail Extraction:** Capture granular, scene-specific features (e.g., "roof submerged up to third floor," "tree branches snapping under tension") rather than abstract categories. Store spatial hierarchies (e.g., "debris pile atop car," "power line crossing above road") and quantify where possible (e.g., "3 cars fully submerged").
2. **Temporal & Contextual Encoding:** Log timestamp differences to infer event sequencing (e.g., "smoke thickens post-18:00 UTC"). Correlate geotags/platform IDs when merging duplicates (e.g., same location but different angles/time stamps).
3. **Hard Deletion Rules:** Remove repetitive descriptors (e.g., deleting "burning structure" after noting "charred timber beams and melted metal fixtures"). Retain contradictions requiring reconciliation (e.g., conflicting casualty reports).
4. **Quantitative Aggregation:** Summarize recurring themes numerically (e.g., "4+ structures compromised" instead of listing individual incidents separately). Track progression (e.g., "damage escalates hourly: Phase I—structural cracks → Phase II—partial collapse").
5. **Token Optimization:** Use tiered prioritization: top-tier slots reserved for actionable data (coordinates, counts, hazards); lower tiers for contextual details. Apply compression algorithms (e.g., hexadecimal truncation of URLs).

**Structured Schema Example:**
```json
{
  "ID": "E01",
  "timestamp": "2017-09-19 16:33 UTC",
  "location": "[geohash]",
  "scene_elements": {
    "primary_hazard": "Flood",
    "quantitative_data": {"submerged_vehicles": 12},
    "spatial_details": [
      {"object": "car", "position": "behind gas station"},
      {"object": "building", "state": "partially collapsed"}
    ]
  },
  "metadata": ["Twitter", "verified account"]
}
```

**Update Protocol:**
- On receiving new evidence: Compare against existing entries using Jaccard index (>0.7 similarity triggers full comparison).
- If conflict detected: Flag both versions with version control headers (`[V1]`/`[V2]`) for human review later.
- Prune lowest-priority details first (e.g., emojis, hashtags) until below token limit.

**Memory Management Thresholds:**
| Token Budget | Action |
|--------------|--------|
| >75%         | Add new entry without deletion |
| ≤75%-50%     | Replace oldest entry <10% relevance score |
| <50%         | Aggressive chunk removal (-30%) |

**Final Constraints:** Max 10 entries, 512 tokens total. Entries must include at least one measurable attribute (coordinate, count, dimension).
```

## Score

**Node score (mean over streams): 0.12** · correct 3/25 · evidence retained 0.48 · abstained 0.48 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 185 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.2 | 2 lines, 127 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.4 | 3 lines, 161 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 370 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.4 | 6 lines, 276 tok |

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
m1 [src E01] Aerial view of a flooded area with multiple buildings and vehicles submerged in water.
m8 [src E08] A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.
m9 [src E09] A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.
m10 [src E10] A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | Yes | `invalid_citation` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `invalid_citation` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | D (Residential area) | `wrong_answer_evidence_missing` | no |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded street with several cars submerged in muddy water, surrounded by buildings and shops. The water level is high, and the street is lined with parked cars and pedestrians.
m10 [src E10] A flooded street with several cars submerged in muddy water, surrounded by buildings and shops. The water level is high, and the street is lined with parked cars and pedestrians.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `invalid_citation` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] ...
m9 [src E09] A social media photo from 2017-09-21 10:33 UTC shows a disaster site with a collapsed building and two workers on a ladder.
m10 [src E10] A social media photo from 2017-09-21 10:48 UTC shows a disaster site with a collapsed building and a dog searching through the rubble.
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
m1 [src E01] Two people are seen running through a burning landscape with multiple small fires and charred tree stumps.
m4 [src E04] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m5 [src E05] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m6 [src E06] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m7 [src E07] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m8 [src E08] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m9 [src E09] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
m10 [src E10] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `invalid_citation` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large building fire is under control with multiple fire trucks and emergency responders on the scene.
m6 [src E06] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
m7 [src E07] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
m8 [src E08] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
m9 [src E09] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
m10 [src E10] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 185 tokens; budget fallbacks 0).
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
  memory about E08: A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/84; 3:2/90; 4:2/90; 5:2/90; 6:2/90; 7:2/90; 8:2/90; 9:3/137; 10:4/185
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with multiple buildings and vehicles submerged in water.
  m8 [src E08] A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.
  m9 [src E09] A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.
  m10 [src E10] A social media user posted a photo showing a flooded area with multiple buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.2 of the questions; final memory 2 lines / 127 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=2, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 4
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
* wrong_answer_evidence_missing | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A flooded street with several cars submerged in muddy water, surrounded by buildings and shops. The water level is high, and the street is lined with parked cars and pedestrians.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/66; 2:2/91; 3:2/126; 4:2/126; 5:2/111; 6:2/103; 7:2/103; 8:2/124; 9:2/126; 10:2/127
FINAL MEMORY:
  m1 [src E01] A flooded street with several cars submerged in muddy water, surrounded by buildings and shops. The water level is high, and the street is lined with parked cars and pedestrians.
  m10 [src E10] A flooded street with several cars submerged in muddy water, surrounded by buildings and shops. The water level is high, and the street is lined with parked cars and pedestrians.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.4 of the questions; final memory 3 lines / 161 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, invalid_citation=1, unnecessary_abstention=2

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
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo from 2017-09-21 10:33 UTC shows a disaster site with a collapsed building and two workers on a ladder.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo from 2017-09-21 10:48 UTC shows a disaster site with a collapsed building and a dog searching through the rubble.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/65; 2:2/130; 3:2/130; 4:2/130; 5:2/130; 6:2/130; 7:2/130; 8:2/130; 9:2/130; 10:3/161
FINAL MEMORY:
  m1 [src E01] ...
  m9 [src E09] A social media photo from 2017-09-21 10:33 UTC shows a disaster site with a collapsed building and two workers on a ladder.
  m10 [src E10] A social media photo from 2017-09-21 10:48 UTC shows a disaster site with a collapsed building and a dog searching through the rubble.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 370 tokens; budget fallbacks 0).
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
  memory about E10: A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/47; 2:2/93; 3:2/93; 4:2/93; 5:3/139; 6:4/185; 7:5/231; 8:6/277; 9:7/323; 10:8/370
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape with multiple small fires and charred tree stumps.
  m4 [src E04] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m5 [src E05] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m6 [src E06] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m7 [src E07] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m8 [src E08] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m9 [src E09] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m10 [src E10] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 6 lines / 276 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large building fire is under control with multiple fire trucks and emergency responders on the scene.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* wrong_answer_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* abstained_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* invalid_citation | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/45; 2:2/89; 3:2/91; 4:2/91; 5:2/91; 6:2/91; 7:3/137; 8:4/183; 9:5/229; 10:6/276
FINAL MEMORY:
  m1 [src E01] A large building fire is under control with multiple fire trucks and emergency responders on the scene.
  m6 [src E06] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
  m7 [src E07] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
  m8 [src E08] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
  m9 [src E09] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
  m10 [src E10] A social media photo shows a large building fire with debris scattered around and a vehicle on fire.
```
