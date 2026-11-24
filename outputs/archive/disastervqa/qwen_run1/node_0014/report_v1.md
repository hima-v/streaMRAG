# Node 14 (child of node 10)

Archive `qwen_run1` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This enhanced strategy addresses systematic failures observed in previous implementations through four core improvements:  
1. **Semantic Consistency Checks**: Prevent contradictory conclusions (e.g., marking roads as both "blocked" and "unobstructed") by validating logical coherence across memories. This would have corrected errors where incorrect citations persisted due to lack of contradiction resolution.  
2. **Perceptual Hashing & Version Control**: Enable efficient deduplication of visually identical/similar reports (like repetitive "burning building" entries) while tracking incremental changes in dynamic scenes (e.g., rising flood levels). Previous strategies failed to aggregate similar observations meaningfully.  
3. **Source Credibility Weighting**: Prioritize verified institutional accounts over ambiguous user-generated content, reducing reliance on potentially unreliable metadata (e.g., platform tags). This could improve accuracy in domains like earthquake damage assessment where official reports matter more.  
4. **Confidence Thresholding**: Automatically demote older/more uncertain memories below a confidence score (default 0.6), forcing periodic re-evaluation. This might reduce unnecessary abstentions by surfacing previously dismissed but relevant details when context changes.  

These additions specifically target weaknesses exposed in hurricane/flood/wildfire cases – e.g., preventing simultaneous storage of conflicting evacuation routes or enabling better aggregation of fire-related damage metrics across frames.
- Strategy rationale: This strategy optimizes memory efficiency while preserving actionable insights. By focusing on distinctive visual features and structured metadata (spatial/temporal relationships, quantitative data), it ensures relevance for downstream tasks. Aggressive pruning prevents noise accumulation, while conflict resolution and source prioritization enhance reliability. Temporal handling via versioning balances historical context preservation with space constraints. Token budget adherence forces concise encoding, critical for real-time performance.
- Change: Original: Generic phrases allowed (e.g., "flooded area"); no explicit conflict resolution or confidence scoring.
- Change: Revised: Mandates specific observables, adds conflict flags/semantic checks, introduces versioning for dynamic entities, implements source credibility weighting, and enforces stricter token discipline. Added perceptual hashing for efficient deduplication and expanded temporal granularity requirements.

## Memory strategy (`c32b90dad3c7`)

```
Prioritize retaining unique visual details critical for answering downstream questions while aggressively pruning redundant information. For each new evidence item, extract only distinctive elements directly observable in the image (e.g., "submerged vehicles" instead of generic "flooded area"). Encode spatial relationships ("building X behind car Y"), temporal clues (timestamps indicating sequence), and domain-specific attributes (e.g., "commercial building" vs. "residential"). Implement hard deletion rules: remove duplicate claims (e.g., repeated "buildings submerged") unless updated with conflicting info. Add explicit retention of quantitative data (counts, measurements) and temporal ordering for sequential events. During updates, merge related observations into single entries with aggregated metrics (e.g., summarize "fallen trees" into quantities if visible in subsequent frames). Discard low-value metadata (social media platform tags) unless resolving ambiguity. When updating, explicitly overwrite prior entries using timestamps or positional cues. Maintain strict token limits via aggressive summarization (<50–100 tokens per entry), reserving >200 tokens for multi-modal cross-references. Enforce semantic consistency checks: flag contradictions (e.g., "no debris" overriding "debris present") and prioritize verified sources. Assign probabilistic confidence scores based on observation frequency/recency, decaying older memories. Store raw perceptual hashes (SHA-1) for rapid deduplication without full-image storage. Version persistent entities (e.g., moving objects) rather than deleting records entirely.
```

## Meta harness (`bad68a9e2516`)

```
Improve the memory strategy: Prioritize retaining unique visual details critical for answering downstream questions while aggressively pruning redundant information. For each new evidence item, extract only distinctive elements directly observable in the image (e.g., "floodwater submerging vehicles" vs. generic descriptions like "a flooded area"). Use structured encoding: store spatial relationships ("building X behind car Y"), temporal clues (time-stamped posts indicating sequence), and domain-specific attributes (e.g., "commercial building" vs. "residential"). Implement hard deletion rules: remove duplicate claims (e.g., repeated mentions of "buildings submerged") unless updated with conflicting info. **Add explicit retention of quantitative data** (e.g., counts, measurements) and **temporal ordering** when multiple events occur. During updates, merge related observations into single entries with aggregated metrics (e.g., combine multiple references to "fallen trees" into summarized quantities if visible in subsequent frames). Discard low-value metadata (social media platform tags) unless resolving ambiguity between duplicates. When updating, explicitly overwrite prior entries using timestamps or positional cues to ensure accuracy. Maintain strict token limits via aggressive summarization thresholds. Additionally, enforce semantic consistency checks: flag contradictions between retained memories (e.g., "no debris" later overriding "debris present") and prioritize higher-confidence sources (verified accounts over anonymous posts). Introduce probabilistic confidence scores for memories based on observation frequency and recency—older memories default to lower weights. Store raw perceptual hashes (e.g., SHA-1) alongside text summaries to enable rapid similarity detection for deduplication without storing full images. For time-sensitive updates (e.g., moving objects), append version numbers to key entities rather than deleting entire records. Limit summary lengths to 50–100 tokens per entry, reserving longer slots (>200 tokens) for multi-modal cross-references (e.g., linking a video frame hash to an audio transcript). MEMORY STRATEGY: Retain distinct visual elements critical for answering downstream questions while aggressively discarding redundancy. Extract specific, observable details (e.g., "submerged vehicles" instead of "flooded area") and encode spatial/temporal relationships, domain attributes (e.g., commercial/residential buildings), and quantifiable data. Merge overlapping observations into consolidated entries with aggregated metrics during updates. Delete duplicates unless conflicts arise. Explicitly retain numerical values (counts, measurements) and chronological order for sequential events. Overwrite outdated entries using timestamps or positional cues. Prioritize high-value content; discard non-essential metadata (platform tags) unless needed for disambiguation. Enforce strict token constraints via hierarchical summarization, capping memory at ~8 concise entries within 512 tokens. ADDITIONAL RULES: 1. Semantic Consistency: Verify logical coherence across memories (e.g., reject "no debris" after confirming "debris present"). 2.
```

## Score

**Node score (mean over streams): 0.12** · correct 3/25 · evidence retained 0.72 · abstained 0.44 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 5 lines, 220 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.8 | 8 lines, 323 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 1.0 | 8 lines, 385 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 405 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.4 | 6 lines, 247 tok |

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
m1 [src E01] Aerial view of a flooded area with submerged vehicles, buildings, and trees.
m7 [src E07] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
m8 [src E08] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
m9 [src E09] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
m10 [src E10] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | Yes | `invalid_citation` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | Submerged vehicles and fallen trees | `unsupported` | yes |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | C (Highway) | `wrong_answer_evidence_in_memory` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A flooded area with submerged vehicles and fallen trees.
m4 [src E04] A flooded area with submerged vehicles and fallen trees.
m5 [src E05] A man is swimming in the water holding a rope.
m6 [src E06] A social media photo shows a flooded area with submerged vehicles and fallen trees.
m7 [src E07] A social media photo shows a flooded area with submerged vehicles and fallen trees.
m8 [src E08] A social media photo shows a flooded area with submerged vehicles and fallen trees.
m9 [src E09] A social media photo shows a flooded area with submerged vehicles and fallen trees.
m10 [src E10] A social media photo shows a flooded area with submerged vehicles and fallen trees.
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
m7 [src E07] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
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
m1 [src E01] Two people are standing in the background, surrounded by burning debris and flames.
m4 [src E04] A social media photo shows two people standing in the background, surrounded by burning debris and flames.
m5 [src E05] A social media photo shows two people standing in the background, surrounded by burning debris and flames.
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
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | C (High-rise) | `wrong_answer_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `invalid_citation` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo shows a large fire in a multi-story building.
m6 [src E06] A social media photo shows a large fire in a multi-story building.
m7 [src E07] A social media photo shows a large fire in a multi-story building.
m8 [src E08] A social media photo shows a large fire in a multi-story building.
m9 [src E09] A social media photo shows a large fire in a multi-story building.
m10 [src E10] A social media photo shows a large fire in a multi-story building.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 5 lines / 220 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/87; 3:2/87; 4:2/87; 5:2/87; 6:2/87; 7:2/87; 8:3/131; 9:4/175; 10:5/220
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with submerged vehicles, buildings, and trees.
  m7 [src E07] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
  m8 [src E08] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
  m9 [src E09] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.
  m10 [src E10] A social media photo shows a flooded area with submerged vehicles, buildings, and trees.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 8 lines / 323 tokens; budget fallbacks 0).
OUTCOMES: invalid_citation=1, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* unsupported | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Submerged vehicles and fallen trees | evidence in memory (stored at step 4)
  memory about E04: A flooded area with submerged vehicles and fallen trees.
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
  evaluator: unsupported - The evidence mentions submerged vehicles and fallen trees, but the question asks about the primary obstacle on the road, which is not specified in the evidence.
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded area with submerged vehicles and fallen trees.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: C (Highway) | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a flooded area with submerged vehicles and fallen trees.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a flooded area with submerged vehicles and fallen trees.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/37; 2:2/74; 3:2/74; 4:2/74; 5:3/112; 6:4/154; 7:5/196; 8:6/238; 9:7/280; 10:8/323
FINAL MEMORY:
  m1 [src E01] A flooded area with submerged vehicles and fallen trees.
  m4 [src E04] A flooded area with submerged vehicles and fallen trees.
  m5 [src E05] A man is swimming in the water holding a rope.
  m6 [src E06] A social media photo shows a flooded area with submerged vehicles and fallen trees.
  m7 [src E07] A social media photo shows a flooded area with submerged vehicles and fallen trees.
  m8 [src E08] A social media photo shows a flooded area with submerged vehicles and fallen trees.
  m9 [src E09] A social media photo shows a flooded area with submerged vehicles and fallen trees.
  m10 [src E10] A social media photo shows a flooded area with submerged vehicles and fallen trees.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 1.0 of the questions; final memory 8 lines / 385 tokens; budget fallbacks 0).
OUTCOMES: unnecessary_abstention=3, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* wrong_answer_evidence_in_memory | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: B (Partially damaged) | evidence in memory (stored at step 7)
  memory about E07: A social media photo shows two workers standing on a ladder, inspecting the damaged building.
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/86; 3:2/87; 4:2/87; 5:3/132; 6:4/177; 7:5/222; 8:6/276; 9:7/330; 10:8/385
FINAL MEMORY:
  m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
  m4 [src E04] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m5 [src E05] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m6 [src E06] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m7 [src E07] A social media photo shows two workers standing on a ladder, inspecting the damaged building.
  m8 [src E08] A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 405 tokens; budget fallbacks 0).
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/88; 3:2/88; 4:2/88; 5:3/134; 6:4/188; 7:5/242; 8:6/296; 9:7/350; 10:8/405
FINAL MEMORY:
  m1 [src E01] Two people are standing in the background, surrounded by burning debris and flames.
  m4 [src E04] A social media photo shows two people standing in the background, surrounded by burning debris and flames.
  m5 [src E05] A social media photo shows two people standing in the background, surrounded by burning debris and flames.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 6 lines / 247 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A social media photo shows a large fire in a multi-story building.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
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
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large fire in a multi-story building.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/78; 3:2/82; 4:2/82; 5:2/82; 6:2/82; 7:3/123; 8:4/164; 9:5/205; 10:6/247
FINAL MEMORY:
  m1 [src E01] A social media photo shows a large fire in a multi-story building.
  m6 [src E06] A social media photo shows a large fire in a multi-story building.
  m7 [src E07] A social media photo shows a large fire in a multi-story building.
  m8 [src E08] A social media photo shows a large fire in a multi-story building.
  m9 [src E09] A social media photo shows a large fire in a multi-story building.
  m10 [src E10] A social media photo shows a large fire in a multi-story building.
```
