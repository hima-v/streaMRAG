# Node 9 (child of node 4)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 4's strategy, meta harness and evaluation log (`node_0004/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: **Core Improvements**:
1. *Precision Enhancement*: By requiring >70% lexical overlap for merging, we reduce false merges like conflating "vehicle damage" with "infrastructure collapse". This addresses the hurricane dataset's incorrect citation where "flooded area" replaced specific "residential zone" data.
   
2. *Spatial Precision*: Adding positional markers improves disaster assessment accuracy, crucial for earthquake scenes where rubble distribution affects rescue planning. Current models fail here due to vague descriptors.

3. *Conflict Resolution*: Confidence-weighted updates prevent catastrophic forgetting – e.g., maintaining "brick debris" during earthquake updates despite later mentions of "concrete".

4. *Evaluation Rigor*: Token-adjusted scoring better reflects real-world resource limits. Hurricane data showed high memory bloat (328 tokens used/328 limit) yet poor QA performance, indicating inefficient storage.

**Tradeoffs Addressed**:
- Strict uniqueness reduces ambiguity but requires careful similarity thresholds
- Spatial indexing adds complexity but enables actionable insights
- Conflict resolution balances freshness with continuity needs

This redesign directly tackles observed failures in disaster triage scenarios while optimizing for both accuracy and practical utility.
- Strategy rationale: This revision improves recall of actionable details (e.g., "exactly how much flooding occurred where") while reducing noise. Spatial indexing prevents mislocalization errors, while temporal chaining clarifies causality. Confidence-weighted updates reduce stale inaccuracies. Fixed slot limits force prioritization between competing memories (e.g., choosing between "vehicles submerged" vs. "power poles down"). Precision gains come from rejecting vague claims (e.g., rejecting "disaster" until specific types emerge). Memory size compliance ensures retrieval speed scales linearly with input complexity.
- Change: Original: Merged duplicates at >50% similarity → Revised: >70% with spatial-temporal anchors
- Change: Original: Relative positioning → Revised: Absolute coordinates ("X meters left of landmark")
- Change: Added: Temporal chains tracking sequential dependencies (e.g., E05→E06 via timestamps)
- Change: Revised: Updates use confidence thresholds ≥0.8 instead of strict recency
- Change: Added: Domain-specific attribute slots (max 3 per memory)
- Change: Removed: Social media metadata retention unless provenance-critical
- Change: Adjusted: Evaluation now weights F1 by answer-token efficiency (+ penalty for contradictions)
- Change: Reduced: Redundant verbatim repetition (now stores consolidated summaries)

## Memory strategy (`ebbf6680fe7b`)

```
Retain spatially precise details (positions, counts), temporally linked events, and domain-specific attributes (e.g., "floodwater depth," "building class") while pruning redundant descriptors. Store observations in structured triples: subject-predicate-object (e.g., "car Y submerged under building X"). Merge overlapping reports via lexical uniqueness (>70% overlap requires explicit positional/temporal alignment). Update memories by priority: highest-confidence claims (≥0.8) override older ones, even if recent. Hard-delete duplicates unless new data introduces contradictions. Allocate fixed slots per event type (e.g., 2 memories/disaster-category). Prioritize direct observables—discard inferred context (e.g., omit "emergency response" unless visually confirmed). Token efficiency: maximize factual density (target ~0.6 answers/token).
```

## Meta harness (`c533705ecee5`)

```
Improve the memory strategy by enforcing stricter constraints on redundancy elimination, prioritizing spatially explicit details, and enhancing update logic to resolve conflicts. Modify the evaluation criteria to emphasize precision-recall tradeoffs in downstream tasks.

Memory Strategy Revisions:
1. **Enhanced Uniqueness Filter**: Require >70% lexical similarity before merging duplicates. Example: "submerged cars" ≠ "vehicles underwater" without explicit mapping.
2. **Spatial Indexing**: Encode absolute positions (e.g., "5m left of bridge support") rather than relative terms when geotags exist.
3. **Temporal Chain Tracking**: Maintain event sequences using timestamp overlaps (e.g., link E05→E06 via "same location, +1hr").
4. **Update Rule Overhaul**: Prioritize overwriting earlier entries with higher confidence scores (≥0.8) instead of strict recency.
5. **Domain-Specific Tags**: Retain 3 key attributes per entry (e.g., "flood depth: 2m", "building class: hospital").

Evaluation Adjustments:
- Add F1-score calculation (correct answers / total possible) weighted by token efficiency (answers/tokens ratio).
- Penalize unresolved contradictions within retained memories (-0.1 per inconsistency).
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.8 · abstained 0.56 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 352 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.4 | 5 lines, 276 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 1.0 | 9 lines, 463 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 9 lines, 368 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 330 tok |

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
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | C (Highway) | `wrong_answer_evidence_in_memory` | yes |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
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
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
m3 [src E03] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
m4 [src E04] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
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
m1 [src E01] Two people are standing in the background of a burning landscape.
m3 [src E03] A social media user posted a photo of a burning landscape on Twitter.
m4 [src E04] A social media user posted a photo of a burning landscape on Twitter.
m5 [src E05] A social media user posted a photo of a burning landscape on Twitter.
m6 [src E06] A social media user posted a photo of a burning landscape on Twitter.
m7 [src E07] A social media user posted a photo of a burning landscape on Twitter.
m8 [src E08] A social media user posted a photo of a burning landscape on Twitter.
m9 [src E09] A social media user posted a photo of a burning landscape on Twitter.
m10 [src E10] A social media user posted a photo of a burning landscape on Twitter.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large building fire is under control.
m4 [src E04] A social media photo shows a large building on fire with debris scattered around.
m5 [src E05] A social media photo shows a large building on fire with debris scattered around.
m6 [src E06] A social media photo shows a large building on fire with debris scattered around.
m7 [src E07] A social media photo shows a large building on fire with debris scattered around.
m8 [src E08] A social media photo shows a large building on fire with debris scattered around.
m9 [src E09] A social media photo shows a large building on fire with debris scattered around.
m10 [src E10] A social media photo shows a large building on fire with debris scattered around.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
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
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 5 lines / 276 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* abstained_evidence_missing | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: C (Highway) | evidence in memory (stored at step 8)
  memory about E08: A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:2/110; 6:2/110; 7:2/110; 8:3/165; 9:4/220; 10:5/276
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 9 lines / 463 tokens; budget fallbacks 0).
OUTCOMES: unnecessary_abstention=4, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* wrong_answer_evidence_in_memory | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: B (Partially damaged) | evidence in memory (stored at step 7)
  memory about E07: A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
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
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/86; 3:2/90; 4:3/138; 5:4/192; 6:5/246; 7:6/300; 8:7/354; 9:8/408; 10:9/463
FINAL MEMORY:
  m1 [src E01] Two workers are seen standing on a ladder, inspecting the damaged building.
  m3 [src E03] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m4 [src E04] A social media photo shows a crowd of people with their hands raised, possibly in distress or seeking help.
  m5 [src E05] A social media photo (Twitter), posted 2017-09-21 07:14 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-09-21 07:16 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-09-21 08:35 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-09-21 08:44 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-09-21 10:33 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 9 lines / 368 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media user posted a photo of a burning landscape on Twitter.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media user posted a photo of a burning landscape on Twitter.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media user posted a photo of a burning landscape on Twitter.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/80; 3:2/80; 4:3/121; 5:4/162; 6:5/203; 7:6/244; 8:7/285; 9:8/326; 10:9/368
FINAL MEMORY:
  m1 [src E01] Two people are standing in the background of a burning landscape.
  m3 [src E03] A social media user posted a photo of a burning landscape on Twitter.
  m4 [src E04] A social media user posted a photo of a burning landscape on Twitter.
  m5 [src E05] A social media user posted a photo of a burning landscape on Twitter.
  m6 [src E06] A social media user posted a photo of a burning landscape on Twitter.
  m7 [src E07] A social media user posted a photo of a burning landscape on Twitter.
  m8 [src E08] A social media user posted a photo of a burning landscape on Twitter.
  m9 [src E09] A social media user posted a photo of a burning landscape on Twitter.
  m10 [src E10] A social media user posted a photo of a burning landscape on Twitter.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.8 of the questions; final memory 8 lines / 330 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large building fire is under control.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* unnecessary_abstention | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a large building on fire with debris scattered around.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large building on fire with debris scattered around.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/35; 2:2/82; 3:2/77; 4:2/77; 5:3/119; 6:4/161; 7:5/203; 8:6/245; 9:7/287; 10:8/330
FINAL MEMORY:
  m1 [src E01] A large building fire is under control.
  m4 [src E04] A social media photo shows a large building on fire with debris scattered around.
  m5 [src E05] A social media photo shows a large building on fire with debris scattered around.
  m6 [src E06] A social media photo shows a large building on fire with debris scattered around.
  m7 [src E07] A social media photo shows a large building on fire with debris scattered around.
  m8 [src E08] A social media photo shows a large building on fire with debris scattered around.
  m9 [src E09] A social media photo shows a large building on fire with debris scattered around.
  m10 [src E10] A social media photo shows a large building on fire with debris scattered around.
```
