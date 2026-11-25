# Node 15 (child of node 13)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 13's strategy, meta harness and evaluation log (`node_0013/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This revised framework addresses original shortcomings through four core improvements:

1. **Precision Over Volume**: By mandating specific object descriptions with spatial attributes, we ensure memories directly answer downstream queries like "What's blocking Highway 1?" versus storing generic "flooded streets". The hierarchical categorization allows complex events to be encoded in single entries (e.g., distinguishing between primary earthquake damage and subsequent fires).

2. **Temporal Intelligence**: The exponential decay merging protocol prevents catastrophic forgetting while maintaining recency sensitivity. For instance, an initial report of "3 firefighters injured" would merge with later "4 firefighters rescued" but reject similar-timed duplicates like separate tweets reporting "2 casualties".

3. **Retrieval-First Design**: Embedding mandatory attribute tags creates implicit indexes for efficient querying. A user asking "Which structures remain intact?" could directly search for `[state: undamaged]` tagged entries rather than parsing full text.

4. **Validation Safeguards**: Requiring each memory to address potential question types ensures relevance preservation during aggressive pruning. This explains improved performance in streams requiring quantiative reasoning (wildfire: 0.4 score) versus abstract interpretation tasks (fire: 0.0 score).

The 400-word limit constrained deeper technical elaboration, particularly around the exponential decay formula's parameter selection. Future iterations should explore adaptive τ values based on disaster duration patterns observed in training data.
- Strategy rationale: This strategy balances precision and efficiency by focusing on discriminative elements critical for QA tasks. Exponential decay prevents stale merges without sacrificing recency, while mandatory labeling ensures actionable recall (e.g., "helicopter evacuation" adds specificity beyond "rescue ops"). Token optimization avoids redundancy (e.g., preferring "submerged cars" over verbose explanations). Testing reveals failures stem from oversimplification—merging too early erases unique clues (e.g., deleting E03’s submerged vehicle reference), but structured tagging mitigates ambiguity in later steps.
- Change: Replaced static 24h merging with dynamic decay scoring to adapt to varying event rates. Added validation checkpoints ensuring memories answer at least one QA-type query before storage. Simplified token rules to enforce conciseness while mandating three granular labels per entry. Introduced conflict-based pruning thresholds (≤0.7 similarity or ≥1 novel detail required for updates). Reduced reliance on platform-specific tags (e.g., Twitter/X) in favor of universal location geotags.

## Memory strategy (`ac3039b5b20d`)

```
The memory agent prioritizes high-value visual details: specific, spatially anchored objects (e.g., "charred bus facing north"), motion cues (e.g., "debris trajectory eastward"), and environmental interactions (e.g., "smoke piercing wires"). It uses hierarchical categorization (primary/secondary disasters, phases like "rescue_operations") and enforces granular tagging ([object: UPS truck]; [location: I-5 Bridge]) for precise retrieval. Updates merge dynamically via exponential decay ($ \tau = 3\text{h} $) requiring ≥1 novel detail, while pruning occurs for low-context (<2 anchors) or conflicting data (e.g., casualty count changes). Each entry must answer spatial, quantitative, or sequential queries pre-validation. Storage limits to 512 tokens via `[ID]: <concise_clause>` format, favoring sparse contexts over metadata.
```

## Meta harness (`6ed062e536b7`)

```
**Improved Memory Strategy:**

1. **Enhanced Visual Detail Prioritization:**  
   Retain *specific, spatially anchored objects* (e.g., "upright semi-truck wedged in bridge collapse," "charred bus with broken windshield facing northbound lane") instead of generic terms. Capture motion cues (e.g., "debris trajectory suggesting eastward momentum") and environmental interactions (e.g., "smoke plumes piercing electrical wires").

2. **Hierarchical Event Categorization:**  
   Use multi-slot encoding for complex events:  
   - Primary category (`disaster_type: earthquake`)  
   - Secondary attribute (`secondary_disaster: secondary_fires`)  
   - Temporal phase (`phase: rescue_operations`)

3. **Dynamic Merging Protocol:**  
   Replace fixed 24h window with exponential decay scoring:  
   $ \text{Similarity Score} = e^{-(t_{new}-t_{old})/\tau} $ where $ \tau = 3\text{h} $.  
   Merge if score ≥ 0.7 AND update introduces ≥1 novel detail (e.g., adding "helicopter evacuation" to existing "search team deployment").

4. **Contextual Attribute Tagging:**  
   Mandate minimum three granular labels per entry:  
   ```[object: UPS truck], [location: I-5 Bridge Crossing], [state: overturned]```  
   Include relative positioning markers ("adjacent_to: hospital", "distance_from_center: 15m").

5. **Adaptive Pruning Criteria:**  
   - Eliminate entries with <2 contextual anchors (e.g., missing location/time).  
   - Retain duplicate reports only if temporal gap > 72h OR contain conflicting sub-details (e.g., "3 casualties reported here" vs "no injuries observed").

6. **Memory Validation Checkpoints:**  
   Before writing, verify each entry answers at least one potential question type:  
   - Spatial ("What's west of X?")  
   - Quantitative ("How many Y in Z?")  
   - Sequential ("After W happened next?")

**Format Enforcement:** Strict `[ID]: <clause>` structure with embedded tags:  
`m123: [time: 2023-03-15T14:22Z] [type: aviation_disaster] Helicopter rotor blades spinning rapidly above collapsed construction site.`

**Token Budget Optimization:**  
Prefer concise clauses with embedded qualifiers:  
✅ "Submerged cars with smashed windows along Route 99" (12 tokens)  
❌ "Vehicles underwater due to severe flood damage from storm surge" (18 tokens + vague causality)
```

## Score

**Node score (mean over streams): 0.2** · correct 5/25 · evidence retained 0.8 · abstained 0.52 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 352 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.8 | 8 lines, 409 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 0.8 | 7 lines, 367 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 9 lines, 461 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.6 | 7 lines, 487 tok |

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
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m4 [src E04] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
m5 [src E05] A man is swimming in a river holding a long rope.
m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m10 [src E10] A man is swimming in a river holding a long rope.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | B (Partially damaged) | `wrong_answer_evidence_in_memory` | yes |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | C (Concrete) | `correct` | yes |

Final memory:

```
m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
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
m1 [src E01] Two individuals are seen running through a burning landscape, surrounded by charred trees and smoldering debris.
m3 [src E03] A social media photo shows a burning landscape with flames licking up from the ground.
m4 [src E04] A social media photo shows a burning landscape with flames licking up from the ground.
m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
m9 [src E09] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | A (Residential) | `wrong_answer_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large fire has broken out in a multi-story building in the city. Firefighters are using ladders and aerial ladders to access the building. There are multiple fire trucks and emergency vehicles on the scene. The building appears to be a residential or commercial structure with several floors. Smoke is visible coming from the windows and the roof. There are several firefighters and paramedics on the scene, working to extinguish the fire and provide medical assistance. The street is closed off, and there are no visible signs of damage to the surrounding area.
m5 [src E05] A social media photo of the fire scene was posted on June 25, 2017, at 21:15 UTC.
m6 [src E06] A social media photo of the fire scene was posted on July 21, 2017, at 00:43 UTC.
m7 [src E07] A social media photo of the fire scene was posted on August 23, 2017, at 00:46 UTC.
m8 [src E08] A social media photo of the fire scene was posted on August 28, 2017, at 10:43 UTC.
m9 [src E09] A social media photo of the fire scene was posted on September 6, 2017, at 09:22 UTC.
m10 [src E10] A social media photo of the fire scene was posted on September 8, 2017, at 03:41 UTC.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.2 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
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
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.8 of the questions; final memory 8 lines / 409 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* unnecessary_abstention | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* unnecessary_abstention | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A man is swimming in a river holding a long rope.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:3/149; 6:4/204; 7:5/259; 8:6/314; 9:7/369; 10:8/409
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m4 [src E04] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  m5 [src E05] A man is swimming in a river holding a long rope.
  m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m10 [src E10] A man is swimming in a river holding a long rope.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 7 lines / 367 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* wrong_answer_evidence_in_memory | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: B (Partially damaged) | evidence in memory (stored at step 7)
  memory about E07: A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* wrong_answer_evidence_in_memory | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 8)
  memory about E08: A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* correct | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: C (Concrete) | evidence in memory (stored at step 10)
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/84; 3:2/90; 4:3/138; 5:2/96; 6:3/150; 7:4/204; 8:5/258; 9:6/312; 10:7/367
FINAL MEMORY:
  m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
  m5 [src E05] A social media photo (Twitter), posted 2017-09-21 07:14 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-09-21 07:16 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 9 lines / 461 tokens; budget fallbacks 0).
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
  memory about E09: A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/48; 2:2/92; 3:2/92; 4:3/136; 5:4/190; 6:5/244; 7:6/298; 8:7/352; 9:8/406; 10:9/461
FINAL MEMORY:
  m1 [src E01] Two individuals are seen running through a burning landscape, surrounded by charred trees and smoldering debris.
  m3 [src E03] A social media photo shows a burning landscape with flames licking up from the ground.
  m4 [src E04] A social media photo shows a burning landscape with flames licking up from the ground.
  m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.6 of the questions; final memory 7 lines / 487 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire has broken out in a multi-story building in the city. Firefighters are using ladders and aerial ladders to access the building. There are multiple fire trucks and emergency vehicles on the scene. The building appears to be a residential or commercial structure with several floors. Smoke is visible coming from the windows and the roof. There are several firefighters and paramedics on the scene, working to extinguish the fire and provide medical assistance. The street is closed off, and there are no visible signs of damage to the surrounding area.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: A (Residential) | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo of the fire scene was posted on July 21, 2017, at 00:43 UTC.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/140; 2:2/209; 3:2/177; 4:2/280; 5:2/198; 6:3/256; 7:4/314; 8:5/372; 9:6/429; 10:7/487
FINAL MEMORY:
  m1 [src E01] A large fire has broken out in a multi-story building in the city. Firefighters are using ladders and aerial ladders to access the building. There are multiple fire trucks and emergency vehicles on the scene. The building appears to be a residential or commercial structure with several floors. Smoke is visible coming from the windows and the roof. There are several firefighters and paramedics on the scene, working to extinguish the fire and provide medical assistance. The street is closed off, and there are no visible signs of damage to the surrounding area.
  m5 [src E05] A social media photo of the fire scene was posted on June 25, 2017, at 21:15 UTC.
  m6 [src E06] A social media photo of the fire scene was posted on July 21, 2017, at 00:43 UTC.
  m7 [src E07] A social media photo of the fire scene was posted on August 23, 2017, at 00:46 UTC.
  m8 [src E08] A social media photo of the fire scene was posted on August 28, 2017, at 10:43 UTC.
  m9 [src E09] A social media photo of the fire scene was posted on September 6, 2017, at 09:22 UTC.
  m10 [src E10] A social media photo of the fire scene was posted on September 8, 2017, at 03:41 UTC.
```
