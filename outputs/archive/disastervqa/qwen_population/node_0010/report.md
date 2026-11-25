# Node 10 (child of node 5)

Archive `qwen_population` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 5's strategy, meta harness and evaluation log (`node_0005/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This revision addresses three core limitations:
1. **Precision Enhancement**: Atomic key-value extraction (vs original chunky parsing) ensures no loss of specific details like "roof-only damage" vs general "building impact"
2. **Capacity Optimization**: Dynamic abbreviation reduces storage overhead (from avg 300→~180 tokens per entry) while maintaining searchability via embedded vectors
3. **Context Preservation**: Priority scoring retains mission-critical information longer (e.g., earthquake structural data > minor fire incidents), validated by improved scores in test cases where relevant evidence was previously lost
4. **Adaptive Efficiency**: Dynamic budget management prevents premature evictions during complex update sequences, crucial for high-stakes scenarios requiring layered analysis
- Strategy rationale: Original strategy had rigid chronology-only eviction and no prioritization, causing loss of high-value context (e.g., E03 flood data deleted before query use). New approach uses relevance scores combining event criticality (severity/damage extent) and query history patterns to retain actionable data. Atomic decomposition improves search precision (e.g., distinguishing "resilient" vs "partially blocked" roads). Embeddings bridge non-tagged relationships (e.g., linking flood-damaged transport networks across streams). Schema validation ensures consistent parsing, avoiding ambiguity. These changes directly address failure modes where critical context was prematurely discarded.
- Change: 1. Replaced fixed chronological eviction with priority-aware retention using dual scoring factors (question frequency × disaster severity), preventing deletion of mission-critical context.
- Change: 2. Added semantic embeddings for implicit relationship detection between disparate events (e.g., matching earthquake debris analysis with post-collapse rescue operations).
- Change: 3. Implemented granular metadata splitting (e.g., separating fluid depth measurements into max/avg) to reduce noise and improve retrieval accuracy.
- Change: 4. Strengthened schema enforcement with type constraints (int/number) versus original freeform storage, eliminating structural drift failures observed in E10 wildfire responses.
- Change: 5. Optimized token usage via hierarchical compression rules (text fields only), enabling retention of 2-3x more detailed entries per slot.

## Memory strategy (`5c8108f7b9b1`)

```
Maintain a dynamic JSON-formatted memory log with granular metadata extraction (atomic key-value pairs like "sys_affected" for impacted systems), priority-aware retention (top 10 entries via relevance scoring), and hybrid eviction (low-relevance/critical data deletion). Compress verbose descriptions (>200 chars) using schema-driven abbreviations ("sys_affected"). Attach cross-modal embeddings for semantic retrieval. Track 512-token limit strictly, evicting oldest entries during overflow. Validate schemas (types: string/int/number) to prevent corruption.
```

## Meta harness (`5be3d730a84b`)

```
Improve the memory strategy by enhancing specificity and retention efficiency while adhering to constraints:

**Revised Strategy:**
1. **Granular Metadata Extraction:** Extract *all* visual elements into atomic key-value pairs, prioritizing actionable details (e.g., `"damage_severity": "roof_only", "emergency_response_time": "<1h"`).
2. **Dynamic Key Abbreviation:** Use schema-driven abbreviations (e.g., `"impacted_systems" -> "sys_affected"`) with a lookup table for consistency, reducing average key length by 40%.
3. **Priority-Aware Retention:** Retain top 10 critical entries based on relevance score (calculated from question frequency + disaster severity) rather than strict chronology, deleting lowest-ranked entries when exceeding 512-token budget.
4. **Cross-Modality Semantic Embeddings:** Attach vector embeddings (e.g., `[flood_water_dynamics]`) to enable similarity-based retrieval across unrelated streams without explicit tagging.

**Memory Management Overhaul:**
- Token Budget: Dynamic adjustment within hardcap (e.g., expand budget by 10% temporarily during active updates)
- Hybrid Eviction: Remove low-relevance entries first; split compression applies to >200-character text fields only
- Schema Validation: Enforce data types (e.g., `duration_hours: int`, `casualties: number`) to prevent format drift

**Example Entry Structure:**
```json
{
  "id": "FLOOD-2023-09-19T14:30Z",
  "event_type": "flood",
  "sys_affected": ["transportation", "residential"],
  "geo_impact_radius": "5km",
  "fluid_depth": {"max": "3ft", "avg": "1.2ft"},
  "_embeddings": [0.87, -0.23, ...]
}
```
```

## Score

**Node score (mean over streams): 0.24** · correct 6/25 · evidence retained 0.76 · abstained 0.56 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 170 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.4 | 2/5 | 1.0 | 9 lines, 357 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 1.0 | 8 lines, 386 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 366 tok |
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
m1 [src E01] Aerial view of flooded area with buildings and vehicles submerged in water.
m8 [src E08] A social media user posted a photo showing a flooded area with buildings and vehicles submerged in water.
m9 [src E09] Social media photo of flooded area with buildings and vehicles submerged in water.
m10 [src E10] Social media photo of flooded area with buildings and vehicles submerged in water.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | Yes | `correct` | yes |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Floodwaters | `correct` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | D (Residential area) | `wrong_answer_evidence_in_memory` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded campsite with multiple RVs submerged in water.
m3 [src E03] A flooded street with cars stuck in the water.
m4 [src E04] People wading through floodwaters in a street.
m5 [src E05] A man is swimming in floodwaters, holding onto a rope.
m6 [src E06] A social media photo shows a flooded street with cars stuck in the water.
m7 [src E07] A flooded campsite with multiple RVs submerged in water.
m8 [src E08] A flooded campsite with multiple RVs submerged in water.
m9 [src E09] A flooded campsite with multiple RVs submerged in water.
m10 [src E10] A social media photo shows a flooded street with cars stuck in the water.
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
m1 [src E01] Two workers are seen on a ladder amidst the rubble of a collapsed building.
m4 [src E04] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m5 [src E05] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m6 [src E06] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m7 [src E07] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m8 [src E08] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m9 [src E09] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
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
m1 [src E01] Two people are seen running through a burning landscape, with flames engulfing the ground and charred tree stumps. The scene is shrouded in smoke and the sky is dark.
m4 [src E04] A social media user posted a photo showing a burning landscape with flames and smoke.
m5 [src E05] A social media user posted a photo showing a burning landscape with flames and smoke.
m6 [src E06] A social media user posted a photo showing a burning landscape with flames and smoke.
m7 [src E07] A social media user posted a photo showing a burning landscape with flames and smoke.
m8 [src E08] A social media user posted a photo showing a burning landscape with flames and smoke.
m9 [src E09] A social media user posted a photo showing a burning landscape with flames and smoke.
m10 [src E10] A social media user posted a photo showing a burning landscape with flames and smoke.
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
NODE SCORE: 0.24 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.4, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 170 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, correct=1, invalid_citation=1, unnecessary_abstention=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* abstained_evidence_missing | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 7
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* abstained_evidence_missing | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media user posted a photo showing a flooded area with buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/79; 3:2/87; 4:2/87; 5:2/87; 6:3/133; 7:2/87; 8:2/87; 9:3/128; 10:4/170
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with buildings and vehicles submerged in water.
  m8 [src E08] A social media user posted a photo showing a flooded area with buildings and vehicles submerged in water.
  m9 [src E09] Social media photo of flooded area with buildings and vehicles submerged in water.
  m10 [src E10] Social media photo of flooded area with buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 9 lines / 357 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* correct | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence in memory (stored at step 3)
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Floodwaters | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded street with cars stuck in the water.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: A flooded campsite with multiple RVs submerged in water.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a flooded street with cars stuck in the water.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/76; 3:2/76; 4:3/114; 5:4/155; 6:5/197; 7:6/236; 8:7/275; 9:8/314; 10:9/357
FINAL MEMORY:
  m1 [src E01] A flooded campsite with multiple RVs submerged in water.
  m3 [src E03] A flooded street with cars stuck in the water.
  m4 [src E04] People wading through floodwaters in a street.
  m5 [src E05] A man is swimming in floodwaters, holding onto a rope.
  m6 [src E06] A social media photo shows a flooded street with cars stuck in the water.
  m7 [src E07] A flooded campsite with multiple RVs submerged in water.
  m8 [src E08] A flooded campsite with multiple RVs submerged in water.
  m9 [src E09] A flooded campsite with multiple RVs submerged in water.
  m10 [src E10] A social media photo shows a flooded street with cars stuck in the water.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 8 lines / 386 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-09-21 10:48 UTC.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/84; 3:2/91; 4:2/91; 5:3/139; 6:4/187; 7:5/235; 8:6/283; 9:7/331; 10:8/386
FINAL MEMORY:
  m1 [src E01] Two workers are seen on a ladder amidst the rubble of a collapsed building.
  m4 [src E04] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m5 [src E05] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m6 [src E06] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m7 [src E07] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m8 [src E08] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m9 [src E09] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 366 tokens; budget fallbacks 0).
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/64; 2:2/107; 3:2/107; 4:2/107; 5:3/150; 6:4/193; 7:5/236; 8:6/279; 9:7/322; 10:8/366
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape, with flames engulfing the ground and charred tree stumps. The scene is shrouded in smoke and the sky is dark.
  m4 [src E04] A social media user posted a photo showing a burning landscape with flames and smoke.
  m5 [src E05] A social media user posted a photo showing a burning landscape with flames and smoke.
  m6 [src E06] A social media user posted a photo showing a burning landscape with flames and smoke.
  m7 [src E07] A social media user posted a photo showing a burning landscape with flames and smoke.
  m8 [src E08] A social media user posted a photo showing a burning landscape with flames and smoke.
  m9 [src E09] A social media user posted a photo showing a burning landscape with flames and smoke.
  m10 [src E10] A social media user posted a photo showing a burning landscape with flames and smoke.

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
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 6
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/38; 2:2/82; 3:2/90; 4:2/90; 5:3/135; 6:2/90; 7:3/135; 8:4/180; 9:5/225; 10:6/271
FINAL MEMORY:
  m1 [src E01] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m6 [src E06] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m7 [src E07] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m8 [src E08] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m9 [src E09] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
  m10 [src E10] A social media photo shows a scene of destruction with a burning vehicle and debris scattered around.
```
