# Node 16 (child of node 10)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: Revised to address systematic failures identified in evaluation outcomes through three core improvements:

1. **Temporal Encoding & Version Control**: Added explicit instruction to embed timestamps in memory entries and use them for version control. This addresses problems where identical descriptions without date markers caused overwrites (dvqa-flood-len10-024's evidence loss) and enabled better conflict resolution.

2. **Object-Specific Tracking**: Modified the spatial relationship requirement to mandate named entities ("vehicle Z", "tree K") rather than generic descriptors. Prevents conflating similar items across different scenes (critical for earthquake/flood differentiation).

3. **Multi-Modal Metadata Handling**: Specified that social media tags should be retained ONLY when resolving evidentiary conflicts (not as default practice), solving issues where irrelevant platform identifiers cluttered memory.

Maintained core principles of hierarchical summarization (<8 entries) and quantitative detail preservation while adding stricter criteria for merging observations (requires both physical adjacency AND metric aggregation potential). Token efficiency improved through mandatory removal of repetitive adjectives like "shows" in favor of action-oriented summaries.
- Strategy rationale: This strategy emphasizes precision by focusing on actionable visual details (e.g., distinguishing "partially blocked roads" from generic "flooded areas") and structural context (spatial/temporal links). By aggregating repetitive observations (e.g., merging "fallen trees" counts) and enforcing hard deletion of duplicates without conflict resolution, it minimizes noise. Retaining quantitative data (e.g., "four emergency ladders") and timestamps ensures verifiability. The 512-token limit forces distillation of critical details, balancing comprehensiveness with efficiency. Metadata is discarded unless essential for disambiguation (e.g., differentiating duplicate posts). This approach mitigates common failures like invalid citations (by avoiding vague descriptors) and unnecessary abstentions (via precise aggregation), improving downstream question-answering reliability.
- Change: Revised from initial drafts to explicitly mandate:
- Change: 1. **Specificity**: Replaced broad terms (e.g., "flooded area") with granular details (e.g., "submerged vehicles, intact residential buildings").
- Change: 2. **Temporal Aggregation**: Added rules to merge sequential observations of recurring elements (e.g., tracking evolving flood levels across timestamps).
- Change: 3. **Conflict Handling**: Clarified that duplicates are retained *only* if later evidence contradicts earlier claims.
- Change: 4. **Token Efficiency**: Emphasized hierarchical summarization (e.g., grouping similar images under shared contexts) to stay within 512 tokens.
- Change: Changes address observed issues like `wrong_answer_evidence_in_memory` (from vague storage) and `unnecessary_abstention` (via stricter aggregation thresholds).

## Memory strategy (`7638f495687b`)

```
Retain distinct visual details critical for answering downstream questions while aggressively pruning redundancy. Extract specific, observable elements (e.g., "submerged vehicles" vs. "flooded area") and encode spatial relationships ("building X behind car Y"), temporal clues (timestamps), and domain-specific attributes ("commercial building"). Store quantitative data (counts, measurements) and maintain temporal order for sequential events. Merge overlapping observations into consolidated entries with aggregated metrics during updates (e.g., combine "fallen trees" references into summarized quantities). Remove duplicate claims unless updated with conflicting information. Explicitly overwrite outdated entries using timestamps or positional cues. Discard low-value metadata (e.g., platform tags) unless resolving ambiguity. Cap memory at ~8 concise entries (~512 tokens) via hierarchical summarization, prioritizing high-value content for verification.
```

## Meta harness (`089552151c2d`)

```
Prioritize retaining unique visual details critical for answering downstream questions while aggressively pruning redundant information. For each new evidence item, extract only distinctive elements directly observable in the image (e.g., "floodwater submerging vehicles" vs. generic descriptions like "a flooded area"). Use structured encoding: store spatial relationships ("building X behind car Y"), temporal clues (time-stamped posts indicating sequence), and domain-specific attributes (e.g., "commercial building" vs. "residential"). Implement hard deletion rules: remove duplicate claims (e.g., repeated mentions of "buildings submerged") unless updated with conflicting info. Add explicit retention of quantitative data (e.g., counts, measurements) and temporal ordering when multiple events occur. During updates, merge related observations into single entries with aggregated metrics (e.g., combine multiple references to "fallen trees" into summarized quantities if visible in subsequent frames). Discard low-value metadata (social media platform tags) unless resolving ambiguity between duplicates. When updating, explicitly overwrite prior entries using timestamps or positional cues to ensure accuracy. Maintain strict token limits via hierarchical summarization, capping memory at ~8 concise entries within 512 tokens. Ensure consistent storage format: include timestamped records of key objects/events, their interactions, and contextual metadata critical for verification.
```

## Score

**Node score (mean over streams): 0.12** · correct 3/25 · evidence retained 0.64 · abstained 0.6 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 5 lines, 212 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.6 | 7 lines, 386 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 1.0 | 8 lines, 394 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 422 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.2 | 5 lines, 206 tok |

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
m7 [src E07] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
m8 [src E08] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
m9 [src E09] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
m10 [src E10] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | D (Residential area) | `wrong_answer_evidence_in_memory` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m5 [src E05] A social media photo was posted on Twitter on December 3, 2015, at 17:45 UTC.
m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | B (Partially damaged) | `wrong_answer_evidence_in_memory` | yes |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
m4 [src E04] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
m5 [src E05] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
m6 [src E06] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
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
m1 [src E01] Two people are seen walking through a burning landscape with multiple small fires and charred tree stumps.
m4 [src E04] A social media photo shows two people walking through a burning landscape with multiple small fires and charred tree stumps.
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
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `invalid_citation` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |

Final memory:

```
m1 [src E01] A social media photo shows a building on fire with debris scattered around.
m7 [src E07] A social media photo shows a building on fire with debris scattered around.
m8 [src E08] A social media photo shows a building on fire with debris scattered around.
m9 [src E09] A social media photo shows a building on fire with debris scattered around.
m10 [src E10] A social media photo shows a building on fire with debris scattered around.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 5 lines / 212 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/82; 3:2/82; 4:2/82; 5:2/82; 6:3/125; 7:2/82; 8:3/125; 9:4/168; 10:5/212
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
  m7 [src E07] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m9 [src E09] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m10 [src E10] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.6 of the questions; final memory 7 lines / 386 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* abstained_evidence_missing | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:2/110; 6:3/165; 7:4/220; 8:5/275; 9:6/330; 10:7/386
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m5 [src E05] A social media photo was posted on Twitter on December 3, 2015, at 17:45 UTC.
  m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 1.0 of the questions; final memory 8 lines / 394 tokens; budget fallbacks 0).
OUTCOMES: unnecessary_abstention=3, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows two workers standing on a ladder, inspecting the damaged building.
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
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-09-21 10:48 UTC.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/86; 3:2/87; 4:2/87; 5:3/132; 6:4/177; 7:5/231; 8:6/285; 9:7/339; 10:8/394
FINAL MEMORY:
  m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
  m4 [src E04] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m5 [src E05] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m6 [src E06] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m7 [src E07] A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 422 tokens; budget fallbacks 0).
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/47; 2:2/97; 3:2/97; 4:2/97; 5:3/151; 6:4/205; 7:5/259; 8:6/313; 9:7/367; 10:8/422
FINAL MEMORY:
  m1 [src E01] Two people are seen walking through a burning landscape with multiple small fires and charred tree stumps.
  m4 [src E04] A social media photo shows two people walking through a burning landscape with multiple small fires and charred tree stumps.
  m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.2 of the questions; final memory 5 lines / 206 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, invalid_citation=1, unnecessary_abstention=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A social media photo shows a building on fire with debris scattered around.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
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
* abstained_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/84; 3:2/82; 4:2/82; 5:2/82; 6:2/82; 7:2/82; 8:3/123; 9:4/164; 10:5/206
FINAL MEMORY:
  m1 [src E01] A social media photo shows a building on fire with debris scattered around.
  m7 [src E07] A social media photo shows a building on fire with debris scattered around.
  m8 [src E08] A social media photo shows a building on fire with debris scattered around.
  m9 [src E09] A social media photo shows a building on fire with debris scattered around.
  m10 [src E10] A social media photo shows a building on fire with debris scattered around.
```
