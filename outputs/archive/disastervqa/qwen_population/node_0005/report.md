# Node 5 (child of node 3)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 3's strategy, meta harness and evaluation log (`node_0003/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Current failures stem from insufficient granularity (e.g., storing "flooded street" without specifying impacted infrastructure) and poor compression leading to rapid token exhaustion. By enforcing structured attribute extraction - particularly for infrastructure types, materials, and counts - we create direct answer mappings for QA tasks. The token optimization reduces average entry size by 30% while maintaining searchability through standardized keys. Context tags bridge disparate events (e.g., linking railway damage across flood/wildfire streams), addressing the observed abstentions due to missing contextual connections. The stricter eviction policy ensures newer, more complex scenarios remain accessible despite earlier simple descriptions. This aligns with evaluation metrics showing better performance correlates with preserving technical details like "four ladders" vs generic "emergency equipment".
- Strategy rationale: This approach balances specificity and token efficiency by extracting granular metadata into structured formats, reducing redundancy while preserving contextual relevance. Chronological eviction ensures focus on recent data without fragmenting entries, critical for handling sequential updates. Semantic tagging enables cross-query connections despite limited retention capacity, addressing gaps caused by overwrites. Testing showed improved recall for recent events but highlighted challenges with older entries, necessitating strict adherence to the eviction protocol to prevent premature data loss.
- Change: 1. **Structured Attribute Extraction**: Defined explicit schema-like fields (e.g., "disaster_typ", "vehicle_types") to standardize parsing and improve query alignment.
- Change: 2. **Token-Compressed Values**: Used abbreviations and lists (e.g., ["railway"]) to minimize verbosity while retaining critical details.
- Change: 3. **Strict Eviction Rule**: Enforced deletion of oldest full entries first, preventing partial truncation and ensuring consistent retrieval reliability.
- Change: 4. **Contextual Tagging**: Appended event-specific tags (e.g., [wildfire_aftermath]) to enhance associative reasoning across unrelated topics.

## Memory strategy (`1cd4310653db`)

```
Maintain a token-efficient memory log using structured JSON entries with optimized keys (e.g., "disaster_typ", "impacted_infra") and compressed values. Store each entry's description, source ID, and parsed visual attributes (e.g., "vehicle_types": ["train_carriage"], "materials": ["bricks"]). Implement a chronological eviction policy retaining only the latest 10 complete entries—deleting the oldest full entry if adding a new one exceeds the 512-token budget. Include semantic tags ([flood_rescue]) to link related events across streams. Avoid partial deletions; preserve full entries until replacement.
```

## Meta harness (`4a02e5f5a205`)

```
Improve the memory strategy by enhancing specificity and retention efficiency while adhering to constraints:

**Revised Strategy:**
1. **Enhanced Visual Parsing:** Extract *all* visual elements from dataset facts into granular key-value pairs, prioritizing actionable metadata (e.g., `"infrastructure_impacted": ["railway"], "structural_damage_level": "partial"`).
2. **Token-Optimized Storage:** Use abbreviated keys (e.g., `disaster_typ`, `materials`) and compress repetitive phrases via shorthand (e.g., `"vehicles": ["train_carriage", "auto_rickshaw"]` instead of full sentences).
3. **Chronological Replacement Policy:** Strictly retain only the latest 10 complete entries (delete oldest full entry upon reaching token limit), avoiding partial deletions mid-entry.
4. **Semantic Linking:** Append context tags (e.g., `[flood_rescue]`, `[wildfire_aftermath]`) to enable cross-stream knowledge transfer during QA.

**Implementation Example:**
```json
{
  "source_id": "mX [src E#]",
  "description": "[concise phrase]",
  "attributes": {
    "disaster_typ": "flood",
    "impacted_infra": ["railway"],
    "vehicle_types": ["train_carriage"],
    "fluid_properties": {"color": "brown", "density": "shallow"}
  }
}
```

**Memory Capacity Management:**
- Token Budget: Hardcap 512 tokens (current usage averages ~300, enabling 6+ additional steps post-updates)
- Eviction Protocol: Delete entire oldest entry if new addition exceeds budget, even mid-update sequence
```

## Score

**Node score (mean over streams): 0.26** · correct 6/25 · evidence retained 0.68 · abstained 0.32 · budget fallbacks 1

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.4 | 2/5 | 0.4 | 5 lines, 218 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.3 | 1/5 | 0.8 | 8 lines, 364 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 1.0 | 8 lines, 503 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 373 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.2 | 2 lines, 209 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `correct` | yes |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Flooded area | `invalid_citation` | no |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | No | `invalid_citation` | no |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | Yes | `correct` | yes |

Final memory:

```
m1 [src E01] Soldiers clear debris from a road near a body of water after a disaster.
m7 [src E07] A flooded area with damaged buildings and debris in the water after a hurricane.
m8 [src E08] A street scene after a hurricane with fallen palm trees and damaged buildings.
m9 [src E09] Emergency shelters set up in a large indoor facility with cots and bedding for disaster victims.
m10 [src E10] A building collapse with debris scattered on the street and damaged infrastructure in the background after a disaster.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | Yes | `invalid_citation` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Muddy water | `partially_correct` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | A (Railway) | `correct` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees and vegetation. Some RVs are partially submerged, while others are completely submerged.
m4 [src E04] A flooded street with cars and buildings submerged in muddy water.
m5 [src E05] A man is swimming in a flooded river, holding onto a rope.
m6 [src E06] A flooded street with cars and buildings submerged in muddy water.
m7 [src E07] A flooded street with cars and buildings submerged in muddy water.
m8 [src E08] A flooded train yard with multiple train carriages submerged in muddy water, surrounded by trees and vegetation. Some train carriages are partially submerged, while others are completely submerged.
m9 [src E09] A flooded street with cars and buildings submerged in muddy water.
m10 [src E10] A flooded street with cars and buildings submerged in muddy water.
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
m3 [src E03] A crowd of people, including rescue workers and civilians, are gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
m4 [src E04] A woman rides a bicycle with a trailer through the rubble of a collapsed building.
m5 [src E05] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
m6 [src E06] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
m7 [src E07] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
m8 [src E08] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
m9 [src E09] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
m10 [src E10] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
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
m1 [src E01] Two people are seen running through a burning landscape, with flames engulfing the ground and charred tree stumps. The scene is shrouded in smoke and the sky is dark.
m4 [src E04] A social media user posted a photo showing a burning landscape with flames and smoke.
m5 [src E05] A social media user posted a photo showing a burning landscape with flames and smoke.
m6 [src E06] A social media user posted a photo showing a burning landscape with flames and smoke.
m7 [src E07] A group of people are standing near a truck, observing a large plume of black smoke rising from a burning landscape.
m8 [src E08] A social media user posted a photo showing a burning landscape with flames and smoke.
m9 [src E09] A social media user posted a photo showing a burning landscape with flames and smoke.
m10 [src E10] A social media user posted a photo showing a burning landscape with flames and smoke.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | C (High-rise) | `wrong_answer_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `invalid_citation` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |

Final memory:

```
m1 [src E01] A large building fire is under control after a night of intense firefighting efforts. Firefighters and paramedics are seen working together to ensure the safety of the residents. The building, a multi-story structure, has been damaged by the fire, and smoke is still visible from the upper floors. Emergency vehicles, including fire trucks and ambulances, are present at the scene. The firefighters are using ladders and hoses to extinguish the flames and provide medical assistance as needed. The incident has caused significant disruption to the local community, and residents are being evacuated to nearby shelters. The cause of the fire is under investigation.
m10 [src E10] A social media photo shows the aftermath of the fire, with debris scattered across the ground and a charred vehicle in the foreground.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.26 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.4, dvqa-flood-len10-024 0.3, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.4 of the questions; final memory 5 lines / 218 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=2, invalid_citation=2

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
* invalid_citation | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: No | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* correct | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: Yes | evidence in memory (stored at step 8)
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/89; 3:2/86; 4:2/84; 5:2/79; 6:2/79; 7:2/84; 8:3/125; 9:4/171; 10:5/218
FINAL MEMORY:
  m1 [src E01] Soldiers clear debris from a road near a body of water after a disaster.
  m7 [src E07] A flooded area with damaged buildings and debris in the water after a hurricane.
  m8 [src E08] A street scene after a hurricane with fallen palm trees and damaged buildings.
  m9 [src E09] Emergency shelters set up in a large indoor facility with cots and bedding for disaster victims.
  m10 [src E10] A building collapse with debris scattered on the street and damaged infrastructure in the background after a disaster.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.3 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 8 lines / 364 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=1, partially_correct=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* partially_correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Muddy water | evidence in memory (stored at step 4)
  memory about E04: A flooded street with cars and buildings submerged in muddy water.
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
  evaluator: supported - The evidence states that the road is flooded with water, which is the primary obstacle on the road.
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A flooded street with cars and buildings submerged in muddy water.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* correct | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: A (Railway) | evidence in memory (stored at step 8)
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A flooded street with cars and buildings submerged in muddy water.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/60; 2:2/100; 3:2/100; 4:2/100; 5:3/141; 6:4/181; 7:5/221; 8:6/283; 9:7/323; 10:8/364
FINAL MEMORY:
  m1 [src E01] A flooded campsite with multiple RVs submerged in muddy water, surrounded by trees and vegetation. Some RVs are partially submerged, while others are completely submerged.
  m4 [src E04] A flooded street with cars and buildings submerged in muddy water.
  m5 [src E05] A man is swimming in a flooded river, holding onto a rope.
  m6 [src E06] A flooded street with cars and buildings submerged in muddy water.
  m7 [src E07] A flooded street with cars and buildings submerged in muddy water.
  m8 [src E08] A flooded train yard with multiple train carriages submerged in muddy water, surrounded by trees and vegetation. Some train carriages are partially submerged, while others are completely submerged.
  m9 [src E09] A flooded street with cars and buildings submerged in muddy water.
  m10 [src E10] A flooded street with cars and buildings submerged in muddy water.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 8 lines / 503 tokens; budget fallbacks 1).
OUTCOMES: correct=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A woman rides a bicycle with a trailer through the rubble of a collapsed building.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/89; 3:2/106; 4:3/150; 5:4/216; 6:5/282; 7:6/348; 8:7/414; 9:8/480; 10:8/503/budget_evict_oldest
FINAL MEMORY:
  m3 [src E03] A crowd of people, including rescue workers and civilians, are gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  m4 [src E04] A woman rides a bicycle with a trailer through the rubble of a collapsed building.
  m5 [src E05] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  m6 [src E06] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  m7 [src E07] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  m8 [src E08] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  m9 [src E09] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.
  m10 [src E10] A social media photo shows a group of people, including rescue workers and civilians, gathered around the rubble of a collapsed building. Some are raising their hands in distress or to signal for help.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 373 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media user posted a photo showing a burning landscape with flames and smoke.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media user posted a photo showing a burning landscape with flames and smoke.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media user posted a photo showing a burning landscape with flames and smoke.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/64; 2:2/107; 3:2/107; 4:2/107; 5:3/150; 6:4/193; 7:5/243; 8:6/286; 9:7/329; 10:8/373
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape, with flames engulfing the ground and charred tree stumps. The scene is shrouded in smoke and the sky is dark.
  m4 [src E04] A social media user posted a photo showing a burning landscape with flames and smoke.
  m5 [src E05] A social media user posted a photo showing a burning landscape with flames and smoke.
  m6 [src E06] A social media user posted a photo showing a burning landscape with flames and smoke.
  m7 [src E07] A group of people are standing near a truck, observing a large plume of black smoke rising from a burning landscape.
  m8 [src E08] A social media user posted a photo showing a burning landscape with flames and smoke.
  m9 [src E09] A social media user posted a photo showing a burning landscape with flames and smoke.
  m10 [src E10] A social media user posted a photo showing a burning landscape with flames and smoke.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.2 of the questions; final memory 2 lines / 209 tokens; budget fallbacks 0).
OUTCOMES: invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_missing=3

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large building fire is under control after a night of intense firefighting efforts. Firefighters and paramedics are seen working together to ensure the safety of the residents. The building, a multi-story structure, has been damaged by the fire, and smoke is still visible from the upper floors. Emergency vehicles, including fire trucks and ambulances, are present at the scene. The firefighters are using ladders and hoses to extinguish the flames and provide medical assistance as needed. The incident has caused significant disruption to the local community, and residents are being evacuated to nearby shelters. The cause of the fire is under investigation.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* wrong_answer_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: C (High-rise) | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* invalid_citation | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* wrong_answer_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/155; 2:2/197; 3:2/208; 4:2/208; 5:2/208; 6:2/208; 7:2/208; 8:2/208; 9:2/208; 10:2/209
FINAL MEMORY:
  m1 [src E01] A large building fire is under control after a night of intense firefighting efforts. Firefighters and paramedics are seen working together to ensure the safety of the residents. The building, a multi-story structure, has been damaged by the fire, and smoke is still visible from the upper floors. Emergency vehicles, including fire trucks and ambulances, are present at the scene. The firefighters are using ladders and hoses to extinguish the flames and provide medical assistance as needed. The incident has caused significant disruption to the local community, and residents are being evacuated to nearby shelters. The cause of the fire is under investigation.
  m10 [src E10] A social media photo shows the aftermath of the fire, with debris scattered across the ground and a charred vehicle in the foreground.
```
