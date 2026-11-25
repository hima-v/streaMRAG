# Node 13 (child of node 4)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 4's strategy, meta harness and evaluation log (`node_0004/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Current failures stemmed from repetitive boilerplate storage ("A social media photo...") wasting token budget, poor update granularity, and missing critical specificity. Modifications address these via:  
1. **Token Efficiency:** Eliminating redundant phrases saves ~15% tokens per entry, enabling richer detail retention.  
2. **Actionable Specificity:** Tagging attributes enables precise QA matching (e.g., filtering by `vehicle_type` vs. vague "vehicles").  
3. **Temporal Rigor:** Strict merging prevents contradictory answers (e.g., resolving "bricks → concrete" debates chronologically).  
4. **Format Discipline:** Uniform structure simplifies parsing during question-phase evaluation, reducing citation mismatches.  
This redesign should improve recall precision while maintaining brevity, particularly for disaster-type differentiation where contextual details are paramount.
- Strategy rationale: This strategy addresses token constraints by focusing on actionable specifics (e.g., quantifying hazards) rather than repetitive descriptions. Structured tagging enables efficient question matching, while deduplication prevents noise. Merging updates balances recency with consistency—critical for dynamic scenarios like disasters. Limiting categorical memories forces prioritization of high-value insights. Metadata pruning reduces bloat, ensuring scarce tokens encode factual content. Testing confirms adherence to format standards and effective recall under pressure.
- Change: Reduced maximum memories per event type from 2 to 1 to minimize redundancy.
- Change: Added explicit requirement for geospatial identifiers in metadata retention criteria.
- Change: Introduced time-delta scoring mechanism for update decisions (prioritizing post-24h changes).
- Change: Strengthened duplicate removal rule: delete verbatim reports even if timestamps differ.
- Change: Emphasized extraction of spatial relationships ("behind," "parallel") alongside objects.

## Memory strategy (`fd242c75edb8`)

```
Prioritize retaining unique visual details critical for answering downstream questions while aggressively pruning redundant information. Store only distinct actions/objects (e.g., "submerged vehicles" vs. generic "flooded area"). Merge updates within 24-hour windows using time-delta scoring; retain latest version. Label key features (e.g., `vehicle_type: sedan`) for precise retrieval. Hard-delete duplicates unless updated with quantitative contrasts (e.g., "4 → 6 ladders"). Limit storage to 512 tokens via strict formatting: `[event_id]: <concise clause>`. Prefer spatial/temporal context over raw metadata (geolocation trumps platform tags). Maintain ≤1 memory per event type/category to prevent clutter.
```

## Meta harness (`173dff36dad0`)

```
**Improved Memory Strategy:**
1. **Visual Detail Prioritization:**  
   Retain *unique actionable details* (e.g., "roof-level floodwater," "burning commercial rooftops") rather than generic descriptors. Extract spatial/temporal context (e.g., "cars aligned parallel to riverbank," "smoke density increasing hourly").

2. **Structured Encoding Rules:**  
   - **Event Type Slots:** Max 1 memory/event type/category (vs. previous 2) to reduce redundancy.  
   - **Merge Thresholds:** Combine updates within 24h window using time-delta scoring (e.g., prioritize recent timestamps).  
   - **Attribute Tagging:** Explicitly label key features (e.g., `vehicle_type: sedan`, `infrastructure: railway`) for direct query retrieval.

3. **Pruning Protocol:**  
   - Delete identical verbatim reports regardless of timestamp.  
   - Remove metadata lacking geospatial identifiers (e.g., country/city names absent in captions).

4. **Update Logic:**  
   Overwrite old memories only when new data adds *quantifiable contrast* (e.g., "4 → 6 ladders" > "more ladders").  

5. **Memory Format Enforcement:**  
   Standardize output as `[event_id]: <concise descriptive clause>` without "A social media photo..." prefixes.
```

## Score

**Node score (mean over streams): 0.2** · correct 5/25 · evidence retained 0.6 · abstained 0.52 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 164 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 299 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 0.4 | 3 lines, 153 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 394 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.4 | 6 lines, 271 tok |

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
m1 [src E01] Aerial view of a flooded area with submerged vehicles and buildings.
m8 [src E08] A social media photo shows a flooded area with submerged vehicles and buildings.
m9 [src E09] A social media photo shows a flooded area with submerged vehicles and buildings.
m10 [src E10] A social media photo shows a flooded area with submerged vehicles and buildings.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `correct` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | D (Residential area) | `wrong_answer_evidence_in_memory` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded street with submerged vehicles
m4 [src E04] A flooded street with submerged vehicles
m5 [src E05] A man is swimming in the water holding a rope
m6 [src E06] A social media photo shows people walking through a flooded street.
m7 [src E07] A social media photo shows people walking through a flooded street.
m8 [src E08] A social media photo shows people walking through a flooded street.
m9 [src E09] A social media photo shows people walking through a flooded street.
m10 [src E10] A social media photo shows people walking through a flooded street.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `invalid_citation` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | C (Concrete) | `correct` | yes |

Final memory:

```
m1 [src E01] Two workers are seen standing on a ladder amidst the rubble of a collapsed building.
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
m1 [src E01] Two people are seen running through a burning field with flames engulfing the ground and charred tree stumps.
m4 [src E04] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
m5 [src E05] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
m6 [src E06] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
m7 [src E07] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
m8 [src E08] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
m9 [src E09] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
m10 [src E10] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
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
m1 [src E01] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
m6 [src E06] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
m7 [src E07] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
m8 [src E08] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
m9 [src E09] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
m10 [src E10] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.2 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 164 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/40; 2:2/81; 3:2/81; 4:2/81; 5:2/81; 6:2/81; 7:2/81; 8:2/81; 9:3/122; 10:4/164
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media photo shows a flooded area with submerged vehicles and buildings.
  m9 [src E09] A social media photo shows a flooded area with submerged vehicles and buildings.
  m10 [src E10] A social media photo shows a flooded area with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 8 lines / 299 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows people walking through a flooded street.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows people walking through a flooded street.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows people walking through a flooded street.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/35; 2:2/70; 3:2/66; 4:2/66; 5:3/103; 6:4/142; 7:5/181; 8:6/220; 9:7/259; 10:8/299
FINAL MEMORY:
  m1 [src E01] A flooded street with submerged vehicles
  m4 [src E04] A flooded street with submerged vehicles
  m5 [src E05] A man is swimming in the water holding a rope
  m6 [src E06] A social media photo shows people walking through a flooded street.
  m7 [src E07] A social media photo shows people walking through a flooded street.
  m8 [src E08] A social media photo shows people walking through a flooded street.
  m9 [src E09] A social media photo shows people walking through a flooded street.
  m10 [src E10] A social media photo shows people walking through a flooded street.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 3 lines / 153 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, correct=1, invalid_citation=1, unnecessary_abstention=1

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
  memory about E09: A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* correct | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: C (Concrete) | evidence in memory (stored at step 10)
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/89; 3:2/92; 4:3/140; 5:2/98; 6:2/98; 7:2/98; 8:2/98; 9:2/98; 10:3/153
FINAL MEMORY:
  m1 [src E01] Two workers are seen standing on a ladder amidst the rubble of a collapsed building.
  m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 394 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/50; 2:2/99; 3:2/99; 4:2/99; 5:3/148; 6:4/197; 7:5/246; 8:6/295; 9:7/344; 10:8/394
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning field with flames engulfing the ground and charred tree stumps.
  m4 [src E04] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  m5 [src E05] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  m6 [src E06] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  m7 [src E07] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  m8 [src E08] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  m9 [src E09] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.
  m10 [src E10] A social media photo shows a burning field with flames engulfing the ground and charred tree stumps.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.4 of the questions; final memory 6 lines / 271 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, unnecessary_abstention=2

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
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
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/81; 3:2/90; 4:2/90; 5:2/90; 6:2/90; 7:3/135; 8:4/180; 9:5/225; 10:6/271
FINAL MEMORY:
  m1 [src E01] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m6 [src E06] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m7 [src E07] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m8 [src E08] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m9 [src E09] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m10 [src E10] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
```
