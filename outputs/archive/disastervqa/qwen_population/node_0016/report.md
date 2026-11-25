# Node 16 (child of node 5)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 5's strategy, meta harness and evaluation log (`node_0005/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This revision sharpens the original strategy by:
1. Adding **explicit spatial/entity relations** to reduce ambiguity (e.g., distinguishing between "partially blocked roads" and "completely obstructed railways").
2. Introducing **entity reference systems** (`linked_entities`, numeric IDs) to maintain continuity across fragmented memories.
3. Strengthening **token efficiency** via quantifiers ("80% submerged") and standardized formats (JSON arrays/objects).
4. Refining the **replacement policy** to allow redundancy removal first, preserving novel information longer.
5. Emphasizing **validation rules** to prevent illogical associations (e.g., submarines in rivers).
These changes directly address prior failures like misclassifying fire types or losing evacuation ladder counts, ensuring stricter alignment between stored data and ground truth.
- Strategy rationale: This approach improves precision through quantified metrics, explicit spatial encoding, and semantic linking. By replacing vague descriptors with measurable data (e.g., % submerged), recall accuracy increases. Chronological eviction ensures freshness-critical info remains accessible within the 512-token limit. Semantic tags and entity IDs create cross-reference pathways, enabling agents to connect disparate events. Attribute validation prevents nonsensical correlations (e.g., avoiding submarine mentions in land disasters), reducing hallucinations during inference.
- Change: 1. Added explicit damage quantification (e.g., "damage_level": "partial")
- Change: 2. Implemented quantitative tracking (numerical counts/representations)
- Change: 3. Introduced relational nesting for multi-aspect impacts
- Change: 4. Strengthened attribute consistency checks
- Change: 5. Enhanced temporal resolution via precise timestamps

## Memory strategy (`c218b4740f67`)

```
Enhance memory parsing by extracting granular spatial/temporal data (e.g., "infra_impacted": ["railway"], "damage_level": "partial"). Use abbreviations (e.g., "totyp" for disaster type) and compress repetitive terms ("vehicles": ["carriage", "rickshaw"]). Implement strict chronological eviction: retain latest 10 full entries, deleting oldest entire entry upon overflow. Embed contextual tags ([flood_rescue], ref:BLDG-72) and validate attribute consistency (no submarines in floods). Track quantitative details (e.g., "persons_visible": 2) instead of qualitative estimates. Nested structures clarify complex relations (e.g., "impacts": {"railway": "partial"}).
```

## Meta harness (`7d0f135242a6`)

```
Improve the memory strategy by enhancing specificity and retention efficiency while adhering to constraints:

**Revised Strategy:**
1. **Enhanced Visual Parsing:** Extract *all* visual elements from dataset facts into granular key-value pairs, prioritizing actionable metadata (e.g., `"infrastructure_impacted": ["railway"], "structural_damage_level": "partial"`). Add explicit spatial relationships (e.g., `"proximity_to_water": true`, `"obstruction_location": "road_center"`) when inferrable from descriptions.
2. **Token-Optimized Storage:** Use abbreviated keys (e.g., `disaster_typ`, `materials`), compress repetitive phrases via shorthand (e.g., `"vehicles": ["train_carriage", "auto_rickshaw"]`), and encode recurring entities with unique IDs (e.g., `"building_id": "BLDG-72"` for cross-referencing).
3. **Chronological Replacement Policy:** Retain the latest 10 complete entries strictly. If adding an entry would exceed the 512-token budget, delete the oldest *full* entry first, even mid-update sequence. Never truncate individual entries.
4. **Semantic Linking:** Append context tags (e.g., `[flood_rescue]`, `[wildfire_aftermath]`) and entity references (e.g., `ref:BLDG-72`) to enable cross-event reasoning. Include causal links like `[caused_by_previous_disaster]` where applicable.
5. **Structured Metadata Validation:** Ensure attribute consistency (e.g., `vehicle_types` must align with `damage_type`: no submarines in land floods).

**Memory Capacity Management:**
- Token Budget: Enforce hardcap of 512 tokens. Current average usage (~300 tokens) allows buffer for dynamic updates without evictions unless critical.
- Eviction Protocol: Prioritize deletion of redundant entries (e.g., duplicate descriptions) before chronological ones. Maintain a secondary cache of high-priority tags for rapid retrieval.

**Implementation Example (Updated):**
```json
{
  "source_id": "mX [src E#]",
  "description": "[concise phrase]",
  "attributes": {
    "disaster_typ": "flood",
    "impacted_infra": ["railway"],
    "vehicle_types": ["train_carriage"],
    "spatial_relations": {"near_body_of_water": true},
    "linked_entities": ["BLDG-72"]
  },
  "tags": ["[flood_rescue]", "[structural_damage]"]
}
```

**Memory Strategy Enhancements:**
- Replace generic descriptors with quantified metrics (e.g., `"submerged_percentage": "80%"` vs. `"mostly submerged"`).
- Integrate entity tracking (e.g., `"people_count": 2` → `"persons_visible": 2`) for precise recall.
- Use nested objects for complex relations (e.g., `"impacts": {railway: "partial", bridges: "complete"}`).

**Evaluation Log Metrics:**
Track per-stream performance decay over time to identify leakage points. Penalize incorrect citations more heavily than abstentions to discourage guesswork.
```

## Score

**Node score (mean over streams): 0.24** · correct 6/25 · evidence retained 0.68 · abstained 0.48 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 176 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.4 | 2/5 | 0.8 | 8 lines, 399 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.4 | 3 lines, 128 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 346 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 369 tok |

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
m8 [src E08] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m9 [src E09] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
m10 [src E10] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `correct` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | A (Railway) | `correct` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] Flooded vehicles in a forested area. Trees and vegetation partially submerged. Water level high, covering the ground and vehicles.
m4 [src E04] A flooded street with people walking through the water. The water level is high, covering the street and people.
m5 [src E05] A man is swimming in the water holding onto a rope.
m6 [src E06] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
m7 [src E07] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
m8 [src E08] A social media photo shows a flooded railway yard with trains submerged in water.
m9 [src E09] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
m10 [src E10] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
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
m1 [src E01] Two workers are seen on a ladder amidst the rubble of a collapsed building.
m9 [src E09] A social media photo shows a ladder being used to access a collapsed building.
m10 [src E10] A social media photo shows a ladder being used to access a collapsed building.
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
m1 [src E01] Two people are seen running through a burning landscape with flames and smoke in the background.
m4 [src E04] A social media photo shows a burning landscape with flames and smoke in the background.
m5 [src E05] A social media photo shows a burning landscape with flames and smoke in the background.
m6 [src E06] A social media photo shows a burning landscape with flames and smoke in the background.
m7 [src E07] A social media photo shows a burning landscape with flames and smoke in the background.
m8 [src E08] A social media photo shows a burning landscape with flames and smoke in the background.
m9 [src E09] A social media photo shows a burning landscape with flames and smoke in the background.
m10 [src E10] A social media photo shows a burning landscape with flames and smoke in the background.
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
m1 [src E01] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m4 [src E04] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m5 [src E05] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m6 [src E06] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m7 [src E07] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m8 [src E08] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m9 [src E09] Emergency response at night in front of a multi-story building with fire trucks and ladders.
m10 [src E10] Emergency response at night in front of a multi-story building with fire trucks and ladders.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.24 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.4, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 176 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/87; 3:2/87; 4:2/87; 5:2/87; 6:2/87; 7:2/87; 8:2/87; 9:3/131; 10:4/176
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with multiple buildings and vehicles submerged in water.
  m8 [src E08] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m9 [src E09] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m10 [src E10] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 8 lines / 399 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* correct | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: A (Railway) | evidence in memory (stored at step 8)
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/52; 2:2/101; 3:2/101; 4:2/101; 5:3/140; 6:4/194; 7:5/248; 8:6/290; 9:7/344; 10:8/399
FINAL MEMORY:
  m1 [src E01] Flooded vehicles in a forested area. Trees and vegetation partially submerged. Water level high, covering the ground and vehicles.
  m4 [src E04] A flooded street with people walking through the water. The water level is high, covering the street and people.
  m5 [src E05] A man is swimming in the water holding onto a rope.
  m6 [src E06] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
  m7 [src E07] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
  m8 [src E08] A social media photo shows a flooded railway yard with trains submerged in water.
  m9 [src E09] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.
  m10 [src E10] A social media photo shows a flooded street with people walking through the water. The water level is high, covering the street and people.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.4 of the questions; final memory 3 lines / 128 tokens; budget fallbacks 0).
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
  memory about E09: A social media photo shows a ladder being used to access a collapsed building.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a ladder being used to access a collapsed building.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/84; 3:2/85; 4:2/85; 5:2/85; 6:2/85; 7:2/85; 8:2/85; 9:2/85; 10:3/128
FINAL MEMORY:
  m1 [src E01] Two workers are seen on a ladder amidst the rubble of a collapsed building.
  m9 [src E09] A social media photo shows a ladder being used to access a collapsed building.
  m10 [src E10] A social media photo shows a ladder being used to access a collapsed building.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 346 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a burning landscape with flames and smoke in the background.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a burning landscape with flames and smoke in the background.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a burning landscape with flames and smoke in the background.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/87; 3:2/87; 4:2/87; 5:3/130; 6:4/173; 7:5/216; 8:6/259; 9:7/302; 10:8/346
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape with flames and smoke in the background.
  m4 [src E04] A social media photo shows a burning landscape with flames and smoke in the background.
  m5 [src E05] A social media photo shows a burning landscape with flames and smoke in the background.
  m6 [src E06] A social media photo shows a burning landscape with flames and smoke in the background.
  m7 [src E07] A social media photo shows a burning landscape with flames and smoke in the background.
  m8 [src E08] A social media photo shows a burning landscape with flames and smoke in the background.
  m9 [src E09] A social media photo shows a burning landscape with flames and smoke in the background.
  m10 [src E10] A social media photo shows a burning landscape with flames and smoke in the background.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 369 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: Emergency response at night in front of a multi-story building with fire trucks and ladders.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_in_memory | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: C (High-rise) | evidence in memory (stored at step 4)
  memory about E04: Emergency response at night in front of a multi-story building with fire trucks and ladders.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: Emergency response at night in front of a multi-story building with fire trucks and ladders.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/46; 2:2/92; 3:2/92; 4:2/92; 5:3/138; 6:4/184; 7:5/230; 8:6/276; 9:7/322; 10:8/369
FINAL MEMORY:
  m1 [src E01] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m4 [src E04] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m5 [src E05] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m6 [src E06] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m7 [src E07] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m8 [src E08] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m9 [src E09] Emergency response at night in front of a multi-story building with fire trucks and ladders.
  m10 [src E10] Emergency response at night in front of a multi-story building with fire trucks and ladders.
```
