# Node 15 (child of node 10)

Archive `qwen_source_aware` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Memory agent `qwen2-vl-7b` · meta agent `nemotron-12b-vl` · answering agent `qwen2-vl-7b` · evaluator `qwen2-vl-7b`

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 10's strategy, meta harness and evaluation log (`node_0010/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This revision addresses systemic failures observed in evaluations:  
1. **Spatial specificity**: Generic phrases like "burning landscape" (dvqa-fire-len10-066) failed to capture key details (ladders, vehicle types), leading to abstentions. Adding "leaning trees," "bridge-submerged vehicles" forces retention of location-critical data.  
2. **Temporal grouping**: Mixed-phase events caused confusion (e.g., earthquake debris evolving from bricks → concrete). Temporal clustering preserves cause-effect chains via ±1hr windows.  
3. **Cross-stream consistency**: Duplicate landmarks/vehicles appearing across floods/wildfires weren’t tracked, causing contradictory answers. Entity tracking prevents this.  
4. **Quantification gaps**: Missing %age/frequency data hurt wildfire questions requiring comparison (e.g., "primary burning material" needs volume estimates).  
5. **Token efficiency**: Strict slot caps force prioritization – e.g., merging similar wildfire scenes reduces noise without losing actionable patterns.  
By anchoring updates to explicit conflict detection and preserving geolocation warnings (critical for hazard mapping), this strategy should reduce `wrong_answer_evidence_in_memory` errors (seen in hurricane/earthquake streams) while improving temporal coherence in multi-phase disasters.
- Strategy rationale: Current failures stem from conflating descriptive summaries with actionable intelligence. Generic phrases like "flooded area" omit critical discriminators (e.g., "residential zone," "partially blocked road"). Temporal clustering enables sequence reconstruction (e.g., post-disaster cleanup timelines), while entity persistence detection identifies suspicious patterns (repeated license plates suggesting looting). Quantitative thresholds allow users to filter responses by severity (e.g., >50% structure collapse). Token constraints must prioritize novel, multi-modal clues (e.g., "downed wires + floodwater" implies electrocution risk) over repetitive descriptors. Conflict resolution requires full entry replacement to prevent semantic drift—a key failure mode in earthquake/collapse scenarios where debris materials shift between wood/concrete.
- Change: 1. **Entity Tracking**: Added explicit protocol for matching license plates/landmarks across streams using perceptual hashing
- Change: 2. **Temporal Phasing**: Formalized window-based grouping to distinguish pre/post-event states (e.g., rescue operations vs. initial impact)
- Change: 3. **Quantification Rules**: Mandate explicit %/count storage for destructible assets/injuries
- Change: 4. **Conflict Handling**: Replace entire entries during contradictions to avoid compounded errors
- Change: 5. **Redundancy Pruning**: Strengthened regex filters targeting adjective-heavy noun phrases ("many broken..." → "2+ broken...")
- Change: 6. **Token Allocation**: Implemented tiered scoring system weighting spatial precision (+2pts), causality (-1pt for missing timestamps)
- Change: 7. **Metadata Tagging**: Expanded warning preservation to include platform-specific risk codes (e.g., Twitter's @disasteralert tags)

## Memory strategy (`f634c7c3df4f`)

```
Prioritize retention of actionable spatial-temporal-contextual details (e.g., "3+ submerged vehicles," "collapsed brick walls," "active fire zones") by merging duplicate descriptions while preserving unique identifiers (license plates, timestamps). Cluster observations into pre-disaster/active/afermath phases using ±1-hour windows to maintain causal inference capabilities. Track persistent entities (landmarks, license plates) across evidence items using fuzzy matching to detect anomalies. Quantify measurable metrics (% debris coverage, casualty counts) explicitly for analytical reuse. When compressing: hard-delete vague descriptors ("several cars") unless numeric counts exist, retain geolocation hashes/warnings, and overwrite older entries with newer ones if spatially/temporally congruent. Cap memory at 8 highest-density entries (calculated as novelty × relevance ÷ redundancy score), truncating low-value details iteratively. Avoid aggregating contradictory observations without conflict flags.
```

## Meta harness (`804bee06c95b`)

```
Improve the memory strategy:  
Enhance retention of spatially rich details (e.g., "vehicles submerged under bridges," "trees leaning toward roads") and contextual objects (e.g., "emergency lights," "road barriers") often omitted in generic captions. Introduce *temporal grouping*: cluster observations by event phases (pre-disaster, active phase, aftermath) using timestamp windows (±1 hour margins) to preserve causal context. Add *cross-image correlation tracking*: flag recurring entities (e.g., same license plate numbers, identical landmarks) across streams for continuity analysis. Retain *quantitative thresholds* (e.g., "% coverage of floodwater," "number of casualties per frame") to enable comparative reasoning. During compression, prioritize keeping *question-relevant patterns* (e.g., directional damage flows, repeating hazards like "downed wires") over isolated descriptors. Apply *hard deletion* for redundant adjectives (e.g., delete "several cars" → keep "3+ cars"), but retain exact counts where specified numerically. Expand *metadata preservation*: save geolocation hashes (if available) and platform-specific risk warnings alongside timestamps. On update triggers (conflicting reports/contradictory visuals), replace entire entries rather than partial edits. Enforce strict token budgets by capping memory slots at 6–8 entries (prioritizing high-information-density frames first) and applying iterative lossy summarization for overflow cases.  
MEMORY STRATEGY:  
Retain spatial specifics (objects + locations), temporal clusters (±1hr windows), cross-stream correlations, quantified metrics, and question-linked patterns. Group images temporally to infer sequences; track persistent entities (license plates, landmarks); use exact counts; merge only visually indistinguishable instances. Preserve geolocation/platform warnings. Hard-delete redundancies except for conflicting data. Token management: cap at 8 entries via greedy scoring (novelty × relevance ÷ redundancy). Summarize lower-priority entries iteratively until <512 tokens remain.
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.76 · abstained 0.56 · budget fallbacks 0

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 341 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.0 | 0/5 | 0.6 | 6 lines, 331 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.0 | 0/5 | 0.6 | 4 lines, 333 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.4 | 2/5 | 1.0 | 8 lines, 422 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.2 | 1/5 | 0.8 | 8 lines, 380 tok |

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
m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
m4 [src E04] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
m5 [src E05] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
m6 [src E06] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
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
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m1 [src E01] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `invalid_citation` | no |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A social media photo from 2017-09-21 04:40 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
m8 [src E08] A social media photo from 2017-09-21 08:44 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
m9 [src E09] A social media photo from 2017-09-21 10:33 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
m10 [src E10] A social media photo from 2017-09-21 10:48 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
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
m1 [src E01] Two individuals are seen walking through a burning landscape with multiple small fires and charred tree stumps.
m4 [src E04] A social media photo shows two individuals walking through a burning landscape with multiple small fires and charred tree stumps.
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
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | B (Intact with smoke) | `correct` | yes |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m1 [src E01] A large building fire is under control at night with multiple fire trucks and emergency responders on the scene.
m4 [src E04] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
m5 [src E05] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
m6 [src E06] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
m7 [src E07] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
m8 [src E08] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
m9 [src E09] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
m10 [src E10] A social media photo posted on Twitter shows a large building fire with multiple fire trucks and emergency responders on the scene.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 341 tokens; budget fallbacks 0).
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
  memory about E05: A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/82; 3:2/82; 4:2/82; 5:3/125; 6:4/168; 7:5/211; 8:6/254; 9:7/297; 10:8/341
FINAL MEMORY:
  m1 [src E01] Aerial view of flooded area with submerged vehicles and buildings.
  m4 [src E04] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m5 [src E05] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m6 [src E06] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m7 [src E07] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m9 [src E09] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.
  m10 [src E10] A social media photo from Twitter shows a flooded area with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.6 of the questions; final memory 6 lines / 331 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, unnecessary_abstention=1, wrong_answer_evidence_in_memory=2

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
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:2/110; 6:2/110; 7:3/165; 8:4/220; 9:5/275; 10:6/331
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.6 of the questions; final memory 4 lines / 333 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* invalid_citation | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo from 2017-09-21 08:44 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo from 2017-09-21 10:33 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo from 2017-09-21 10:48 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/83; 2:2/166; 3:2/166; 4:2/166; 5:2/166; 6:2/166; 7:2/166; 8:2/166; 9:3/249; 10:4/333
FINAL MEMORY:
  m1 [src E01] A social media photo from 2017-09-21 04:40 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
  m8 [src E08] A social media photo from 2017-09-21 08:44 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
  m9 [src E09] A social media photo from 2017-09-21 10:33 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.
  m10 [src E10] A social media photo from 2017-09-21 10:48 UTC shows a scene of a collapsed building with debris scattered around. There are two individuals on the scene, one wearing a white hat and the other in a green vest.

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
  m1 [src E01] Two individuals are seen walking through a burning landscape with multiple small fires and charred tree stumps.
  m4 [src E04] A social media photo shows two individuals walking through a burning landscape with multiple small fires and charred tree stumps.
  m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m9 [src E09] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.8 of the questions; final memory 8 lines / 380 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large building fire is under control at night with multiple fire trucks and emergency responders on the scene.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* unnecessary_abstention | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/47; 2:2/94; 3:2/94; 4:2/94; 5:3/141; 6:4/188; 7:5/235; 8:6/282; 9:7/329; 10:8/380
FINAL MEMORY:
  m1 [src E01] A large building fire is under control at night with multiple fire trucks and emergency responders on the scene.
  m4 [src E04] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  m5 [src E05] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  m6 [src E06] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  m7 [src E07] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  m8 [src E08] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  m9 [src E09] A social media photo shows a large building fire with multiple fire trucks and emergency responders on the scene.
  m10 [src E10] A social media photo posted on Twitter shows a large building fire with multiple fire trucks and emergency responders on the scene.
```
