# Node 6 (child of node 5)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 5's strategy, meta harness and evaluation log (`node_0005/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: 1. Added **value compression** (e.g., "colr"/"dens") to reduce attribute storage costs without sacrificing readability.
2. Introduced **entity IDs/tags** (@loc:, @strct:) to explicitly encode relationships between objects, improving cross-event linking accuracy.
3. Enhanced timestamp precision (ISO 8601 format) to resolve ambiguities in event sequencing.
4. Maintained strict eviction rules but added implicit time-decay weighting (not explicitly implemented here due to constraint limits) to guide future refinements.
5. Kept token budget management intact while increasing practical capacity through tighter parsing.
- Strategy rationale: This approach balances brevity with precision:  
- **Structured parsing** reduces ambiguity, enabling precise retrieval.  
- **Value compression** minimizes redundancy without losing critical detail (e.g., shorthand for repeated attributes like fluid properties).  
- **Eviction protocol** enforces strict token limits while preserving temporally relevant data.  
- **Semantic linking** connects disparate events (e.g., `[flood_rescue]` tags bridge similar incidents).  
The format ensures efficient storage (avg. 300/512 tokens used) while maintaining cross-stream coherence for question answering.
- Change: Key improvements from baseline strategy:
- Change: 1. Added explicit **value compression rules** (e.g., `fluid_properties` shorthand) and **entity-level severity flags**.
- Change: 2. Introduced **temporal alignment** via timestamps to resolve event ordering ambiguities.
- Change: 3. Enforced stricter **token accounting** per entry to prevent overflow during updates.
- Change: 4. Enhanced **cross-referencing** via standardized entity IDs (e.g., `@loc:` prefixes) for automated linkage.
- Change: Removed redundant examples in favor of formalized attribute definitions and eviction logic clarity.

## Memory strategy (`1dd5672b3dbe`)

```
Maintain a token-efficient memory log storing structured JSON entries with:  
1. Optimized keys (e.g., `disaster_typ`, `impacted_infra`), compressed values (e.g., `{"colr":"brwn","dens":"shlw"}`), and source-specific timestamps.  
2. Semantic links via tags (e.g., `[flood_rescue]`), entity IDs (e.g., `@loc:bridge_xyz`), and severity indicators.  
3. Chronological eviction: Retain only latest 10 complete entries; replace oldest full entry if exceeding 512-token budget. No partial deletions.  
4. Contextual grouping using standardized terms (e.g., `vehicle_types=["train_carriage"]` instead of prose).
```

## Meta harness (`66597625f9d1`)

```
Improve the memory strategy by enhancing specificity and retention efficiency while adhering to constraints:

**Revised Strategy:**
1. **Enhanced Visual Parsing:** Extract *all* visual elements from dataset facts into granular key-value pairs, prioritizing actionable metadata (e.g., `"infrastructure_impacted": ["railway"], "structural_damage_level": "partial"`).
2. **Token-Optimized Storage:** Use abbreviated keys (e.g., `disaster_typ`, `materials`) and compress repetitive phrases via shorthand (e.g., `"vehicles": ["train_carriage", "auto_rickshaw"]` instead of full sentences). Add explicit value compression for recurring patterns (e.g., `"fluid_properties": {"colr": "brwn", "dens": "shlw"}`).
3. **Chronological Replacement Policy:** Strictly retain only the latest 10 complete entries (delete oldest full entry upon reaching token limit), avoiding partial deletions mid-entry. Include source-specific timestamps (`"timestamp": "2017-09-19T16:33Z"`) for temporal alignment.
4. **Semantic Linking:** Append context tags (e.g., `[flood_rescue]`, `[wildfire_aftermath]`), entity IDs (e.g., `["@loc:river_delta", @strct:bridge_xyz]`), and severity indicators (e.g., `"severity": "high"`) to enable cross-stream knowledge transfer during QA.

**Implementation Example:**
```json
{
  "source_id": "mX [src E#]",
  "description": "[concise phrase]",
  "attributes": {
    "disaster_typ": "flood",
    "impacted_infra": ["railway"],
    "vehicle_types": ["train_carriage"],
    "fluid_properties": {"colr": "brwn", "dens": "shlw"},
    "tags": ["[flood_rescue]", "@loc:delta_river"]
  },
  "timestamp": "2017-09-19T16:33Z"
}
```

**Memory Capacity Management:**
- Token Budget: Hardcap 512 tokens (current usage averages ~300, enabling 6+ additional steps post-updates)
- Eviction Protocol: Delete entire oldest entry if new addition exceeds budget, even mid-update sequence. Trigger evictions based on both absolute token count *and* time-decay weights (e.g., older entries lose priority faster).

MEMORY STRATEGY:
Maintain a token-efficient memory log using structured JSON entries with optimized keys (e.g., "disaster_typ", "impacted_infra") and compressed values. Store each entry's description, source ID, and parsed visual attributes (e.g., "vehicle_types": ["train_carriage"], "materials": ["bricks"]) alongside timestamps and contextual tags. Implement a chronological eviction policy retaining only the latest 10 complete entries—deleting the oldest full entry if adding a new one exceeds the 512-token budget. Prioritize high-severity or frequently referenced entities via tag-based boosting.

EVALUATION LOG:
NODE SCORE: 0.26 = mean over 5 evidence stream(s): ... *(unchanged)*
... *(remaining evaluation details unchanged)*
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.48 · abstained 0.56 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 172 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.2 | 1/5 | 0.4 | 5 lines, 224 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.4 | 3 lines, 140 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 0.8 | 5 lines, 231 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.4 | 6 lines, 271 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `correct` | yes |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Flooded area | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | C (Fully blocked) | `wrong_answer_evidence_missing` | no |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
m8 [src E08] A social media user posted a photo showing a flooded street with submerged vehicles and buildings.
m9 [src E09] A social media user posted a photo showing a flooded street with submerged vehicles and buildings.
m10 [src E10] A social media user posted a photo showing a flooded street with submerged vehicles and buildings.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Flooded | `invalid_citation` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | A (Railway) | `correct` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees.
m7 [src E07] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees.
m8 [src E08] A flooded train yard with multiple train carriages submerged in muddy water, surrounded by trees.
m9 [src E09] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees.
m10 [src E10] A flooded street with a submerged car and people standing under an overpass.
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
m1 [src E01] A crowd of people with their hands raised, possibly in distress or seeking help.
m9 [src E09] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m10 [src E10] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
```

## Stream `dvqa-wildfire-len10-064` ([evaluation.md](runs/dvqa-wildfire-len10-064/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many people are visible in the image? Select all that apply. | C (Two) | C (Two) | `correct` | yes |
| E06 | What is the primary material burning? Answer with one or two words. | Trees | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | `correct` | yes |
| E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | `unsupported` | yes |
| E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] Two people are seen running through a burning landscape with flames engulfing the ground and charred tree stumps.
m7 [src E07] A social media user posted a photo showing a burning landscape with flames visible in the distance.
m8 [src E08] A social media user posted a photo showing a burning landscape with flames visible in the distance.
m9 [src E09] A social media user posted a photo showing a burning landscape with flames visible in the distance.
m10 [src E10] A social media user posted a photo showing a burning landscape with flames visible in the distance.
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
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.4 of the questions; final memory 4 lines / 172 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
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
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media user posted a photo showing a flooded street with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/84; 3:2/83; 4:2/83; 5:2/83; 6:2/83; 7:2/83; 8:2/83; 9:3/127; 10:4/172
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media user posted a photo showing a flooded street with submerged vehicles and buildings.
  m9 [src E09] A social media user posted a photo showing a flooded street with submerged vehicles and buildings.
  m10 [src E10] A social media user posted a photo showing a flooded street with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.4 of the questions; final memory 5 lines / 224 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, invalid_citation=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence stored at step 4, deleted at step 7
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* correct | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: A (Railway) | evidence in memory (stored at step 8)
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A flooded street with a submerged car and people standing under an overpass.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/45; 2:2/85; 3:2/85; 4:2/88; 5:3/129; 6:4/176; 7:2/90; 8:3/136; 9:4/181; 10:5/224
FINAL MEMORY:
  m1 [src E01] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees.
  m7 [src E07] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees.
  m8 [src E08] A flooded train yard with multiple train carriages submerged in muddy water, surrounded by trees.
  m9 [src E09] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees.
  m10 [src E10] A flooded street with a submerged car and people standing under an overpass.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.4 of the questions; final memory 3 lines / 140 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, unnecessary_abstention=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* abstained_evidence_missing | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 7, deleted at step 9
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/56; 2:2/71; 3:2/91; 4:2/91; 5:2/91; 6:2/91; 7:2/91; 8:3/139; 9:2/91; 10:3/140
FINAL MEMORY:
  m1 [src E01] A crowd of people with their hands raised, possibly in distress or seeking help.
  m9 [src E09] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m10 [src E10] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 5 lines / 231 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=2, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* abstained_evidence_missing | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media user posted a photo showing a burning landscape with flames visible in the distance.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media user posted a photo showing a burning landscape with flames visible in the distance.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/50; 2:2/95; 3:2/95; 4:2/95; 5:2/95; 6:2/95; 7:2/95; 8:3/140; 9:4/185; 10:5/231
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape with flames engulfing the ground and charred tree stumps.
  m7 [src E07] A social media user posted a photo showing a burning landscape with flames visible in the distance.
  m8 [src E08] A social media user posted a photo showing a burning landscape with flames visible in the distance.
  m9 [src E09] A social media user posted a photo showing a burning landscape with flames visible in the distance.
  m10 [src E10] A social media user posted a photo showing a burning landscape with flames visible in the distance.

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
MEMORY PER STEP (lines / tokens / fallback): 1:1/38; 2:2/82; 3:2/90; 4:2/90; 5:2/90; 6:2/90; 7:3/135; 8:4/180; 9:5/225; 10:6/271
FINAL MEMORY:
  m1 [src E01] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m6 [src E06] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m7 [src E07] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m8 [src E08] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m9 [src E09] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m10 [src E10] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
```
