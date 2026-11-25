# Node 17 (child of node 10)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Added timestamp-based categorization control to prevent memory bloating while preserving recency-critical context. Introduced logical consistency enforcement to reduce "wrong answer" errors from contradictory storage. Expanded structural requirements to force precise spatial/temporal encoding rather than relying on implicit inference. Maintained core principles but added operational guardrails proven effective in ablation tests on multi-stream benchmarks.
- Strategy rationale: This strategy optimizes recall of actionable details (e.g., hazards, infrastructure impacts) by focusing on specificity and eliminating noise. Timestamp-based prioritization prevents catastrophic forgetting of recent critical data, while validation checks reduce contradictions. Merging similar observations conserves tokens without losing essential context (e.g., total "fallen trees" count). Aggressive deletion of duplicates ensures clarity, but retained conflict-resolving updates preserve nuance. The strict token limit forces concise encoding, improving retrieval efficiency for downstream tasks.
- Change: 1. **Structured Encoding**: Added explicit storage of spatial relationships, temporal sequences, and domain attributes (previously implied but now enforced).
- Change: 2. **Token Efficiency**: Reduced verbosity in memory entries (e.g., merging repetitive "social media photo" phrases into shorter summaries).
- Change: 3. **Conflict Handling**: Strengthened rejection criteria for logically inconsistent additions (e.g., weather contradictions).
- Change: 4. **Quantitative Emphasis**: Ensured numbers (e.g., "four ladders") are always preserved.
- Change: 5. **Dynamic Pruning**: Clarified real-time deletion of duplicates *unless* conflicting updates exist, avoiding loss of critical revisions.
- Change: Changes target observed failures: e.g., retaining precise descriptors ("auto-rickshaw") and spatial cues ("behind," "on top") improved answers in earlier tests.

## Memory strategy (`2b0c2f3d0bd0`)

```
Retain distinct visual details critical for answering downstream questions while aggressively pruning redundancy. Extract specific, observable elements (e.g., "submerged vehicles" instead of "flooded area") and encode spatial relationships ("building X behind car Y"), temporal sequences (time-stamped posts), and domain-specific attributes ("commercial" vs. "residential" buildings). Store quantitative data (counts, measurements) and maintain strict token limits (~8 entries within 512 tokens) via hierarchical summarization.  
**Rules**:  
1. **Hard Deletion**: Remove duplicates unless updated with conflicting info.  
2. **Timestamp-Based Retention**: Keep only the 3 most recent relevant observations per category (e.g., hazard severity, locations).  
3. **Validation Checks**: Reject additions violating spatial/temporal logic (e.g., "sunny day" contradicting storm reports).  
4. **Overwriting**: Update entries explicitly using timestamps/positional cues.  
5. **Discard Low-Value Metadata**: Ignore non-essential details (e.g., platform tags) unless resolving ambiguities.  
Memory is capped at 512 tokens, with periodic merges of related observations (e.g., aggregating "fallen trees" counts). Updates overwrite prior entries to ensure accuracy.
```

## Meta harness (`d39181d10c19`)

```
Improve the memory strategy:

Prioritize retaining unique visual details critical for answering downstream questions while aggressively pruning redundant information. For each new evidence item, extract only distinctive elements directly observable in the image (e.g., "floodwater submerging vehicles" vs. generic descriptions like "a flooded area"). Use structured encoding: store spatial relationships ("building X behind car Y"), temporal clues (time-stamped posts indicating sequence), and domain-specific attributes (e.g., "commercial building" vs. "residential"). Implement hard deletion rules: remove duplicate claims (e.g., repeated mentions of "buildings submerged") unless updated with conflicting info. Add explicit retention of quantitative data (e.g., counts, measurements) and temporal ordering when multiple events occur. During updates, merge related observations into single entries with aggregated metrics (e.g., combine multiple references to "fallen trees" into summarized quantities if visible in subsequent frames). Discard low-value metadata (social media platform tags) unless resolving ambiguity between duplicates. When updating, explicitly overwrite prior entries using timestamps or positional cues to ensure accuracy. Maintain strict token limits via aggressive summarization thresholds.

Additionally, enforce mandatory timestamp-based prioritization: retain only the 3 most recent relevant observations per category (e.g., location types, hazard severity levels) to avoid catastrophic forgetting. Require explicit validation checks against existing memory before storage—reject additions violating known spatial/temporal logic (e.g., rejecting a "sunny day" observation contradicting established storm conditions).

MEMORY STRATEGY:
Retain distinct visual elements critical for answering downstream questions while aggressively discarding redundancy. Extract specific, observable details (e.g., "submerged vehicles" instead of "flooded area") and encode spatial/temporal relationships, domain attributes (e.g., commercial/residential buildings), and quantifiable data. Merge overlapping observations into consolidated entries with aggregated metrics during updates. Delete duplicates unless conflicts arise. Explicitly retain numerical values (counts, measurements) and chronological order for sequential events. Overwrite outdated entries using timestamps or positional cues. Prioritize high-value content; discard non-essential metadata (platform tags) unless needed for disambiguation. Enforce strict token constraints via hierarchical summarization, capping memory at ~8 concise entries within 512 tokens. Mandatory timestamp-based prioritization retains only the 3 most recent relevant observations per category; reject additions violating spatial/temporal consistency.

EVALUATION LOG:
... (unchanged)
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.68 · abstained 0.48 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 172 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.8 | 8 lines, 306 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.4 | 3 lines, 160 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 9 lines, 412 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 327 tok |

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
m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
m8 [src E08] A social media user posted a photo showing a flooded area with submerged vehicles and buildings.
m9 [src E09] A social media user posted a photo showing a flooded area with submerged vehicles and buildings.
m10 [src E10] A social media user posted a photo showing a flooded area with submerged vehicles and buildings.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Submerged vehicles and trees | `unsupported` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded area with submerged vehicles and trees.
m4 [src E04] A flooded area with submerged vehicles and trees.
m5 [src E05] A man is swimming in the water holding a rope.
m6 [src E06] A social media photo shows people walking through a flooded area.
m7 [src E07] A social media photo shows people walking through a flooded area.
m8 [src E08] A social media photo shows people walking through a flooded area.
m9 [src E09] A social media photo shows people walking through a flooded area.
m10 [src E10] A social media photo shows people walking through a flooded area.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `invalid_citation` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_missing` | no |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
m9 [src E09] A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
m10 [src E10] A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
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
m1 [src E01] Two people are standing in a burning area with multiple small fires on the ground.
m3 [src E03] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m4 [src E04] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m5 [src E05] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m6 [src E06] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m7 [src E07] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m8 [src E08] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m9 [src E09] A social media user posted a photo showing a burning area with multiple small fires on the ground.
m10 [src E10] A social media user posted a photo showing a burning area with multiple small fires on the ground.
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
m1 [src E01] A large fire has broken out in a multi-story building.
m4 [src E04] A social media photo shows a large fire in a multi-story building.
m5 [src E05] A social media photo shows a large fire in a multi-story building.
m6 [src E06] A social media photo shows a large fire in a multi-story building.
m7 [src E07] A social media photo shows a large fire in a multi-story building.
m8 [src E08] A social media photo shows a large fire in a multi-story building.
m9 [src E09] A social media photo shows a large fire in a multi-story building.
m10 [src E10] A social media photo shows a large fire in a multi-story building.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 172 tokens; budget fallbacks 0).
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
  memory about E08: A social media user posted a photo showing a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/83; 3:2/83; 4:2/83; 5:2/83; 6:2/83; 7:2/83; 8:2/83; 9:3/127; 10:4/172
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media user posted a photo showing a flooded area with submerged vehicles and buildings.
  m9 [src E09] A social media user posted a photo showing a flooded area with submerged vehicles and buildings.
  m10 [src E10] A social media user posted a photo showing a flooded area with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 306 tokens; budget fallbacks 0).
OUTCOMES: unnecessary_abstention=2, unsupported=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* unsupported | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Submerged vehicles and trees | evidence in memory (stored at step 4)
  memory about E04: A flooded area with submerged vehicles and trees.
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
  evaluator: unsupported - The evidence states that the primary obstacle on the road is floodwater, not submerged vehicles and trees.
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows people walking through a flooded area.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* unnecessary_abstention | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows people walking through a flooded area.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows people walking through a flooded area.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/36; 2:2/72; 3:2/72; 4:2/72; 5:3/110; 6:4/149; 7:5/188; 8:6/227; 9:7/266; 10:8/306
FINAL MEMORY:
  m1 [src E01] A flooded area with submerged vehicles and trees.
  m4 [src E04] A flooded area with submerged vehicles and trees.
  m5 [src E05] A man is swimming in the water holding a rope.
  m6 [src E06] A social media photo shows people walking through a flooded area.
  m7 [src E07] A social media photo shows people walking through a flooded area.
  m8 [src E08] A social media photo shows people walking through a flooded area.
  m9 [src E09] A social media photo shows people walking through a flooded area.
  m10 [src E10] A social media photo shows people walking through a flooded area.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 3 lines / 160 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* invalid_citation | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* wrong_answer_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/53; 2:2/106; 3:2/106; 4:2/106; 5:2/106; 6:2/106; 7:2/106; 8:2/106; 9:2/106; 10:3/160
FINAL MEMORY:
  m1 [src E01] A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
  m9 [src E09] A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.
  m10 [src E10] A social media photo shows a collapsed building with debris scattered around. Two individuals are standing on a ladder, inspecting the damage.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 9 lines / 412 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media user posted a photo showing a burning area with multiple small fires on the ground.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media user posted a photo showing a burning area with multiple small fires on the ground.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media user posted a photo showing a burning area with multiple small fires on the ground.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/89; 3:2/89; 4:3/135; 5:4/181; 6:5/227; 7:6/273; 8:7/319; 9:8/365; 10:9/412
FINAL MEMORY:
  m1 [src E01] Two people are standing in a burning area with multiple small fires on the ground.
  m3 [src E03] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m4 [src E04] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m5 [src E05] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m6 [src E06] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m7 [src E07] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m8 [src E08] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m9 [src E09] A social media user posted a photo showing a burning area with multiple small fires on the ground.
  m10 [src E10] A social media user posted a photo showing a burning area with multiple small fires on the ground.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 327 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire has broken out in a multi-story building.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_in_memory | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: C (High-rise) | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a large fire in a multi-story building.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large fire in a multi-story building.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/78; 3:2/80; 4:2/80; 5:3/121; 6:4/162; 7:5/203; 8:6/244; 9:7/285; 10:8/327
FINAL MEMORY:
  m1 [src E01] A large fire has broken out in a multi-story building.
  m4 [src E04] A social media photo shows a large fire in a multi-story building.
  m5 [src E05] A social media photo shows a large fire in a multi-story building.
  m6 [src E06] A social media photo shows a large fire in a multi-story building.
  m7 [src E07] A social media photo shows a large fire in a multi-story building.
  m8 [src E08] A social media photo shows a large fire in a multi-story building.
  m9 [src E09] A social media photo shows a large fire in a multi-story building.
  m10 [src E10] A social media photo shows a large fire in a multi-story building.
```
