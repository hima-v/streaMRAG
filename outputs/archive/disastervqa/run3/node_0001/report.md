# Node 1 (child of node 0)

Archive `run3` · dataset `disastervqa` · base stream `len10` · 5 evidence stream(s) of 10 items · budget 512 tokens · profile `minimal` · switches {'memory_strategy': 'dynamic', 'meta_harness': 'dynamic'}

Questions are asked only after the last item of each stream; the memory agent never sees them.

## How this node was created

The meta agent took parent node 0's strategy, meta harness and evaluation log (`node_0000/meta_log.md`), wrote the new meta harness below, then followed it to write the new memory strategy.

- Harness rationale: This revised harness addresses three core weaknesses observed in prior evaluations:  
1. **Temporal/Spatial Context Loss**: By mandating timestamp-location metadata preservation, it mitigates errors where identical-looking events (e.g., sequential flood photos) overwrote unique contextual clues needed for answering "condition change" questions.  
2. **Redundant Detail Storage**: Merging repetitive visual descriptions (e.g., four flood images showing "cars submerged") reduces token bloat without losing critical data points like exact dates or coordinates.  
3. **Cross-Image Inference Support**: Consolidated entries retain enough variance to support comparisons (e.g., tracking brick vs. concrete debris across earthquake scenes), fixing failures in streams requiring multi-step reasoning.  

The evaluation criteria enforce practical constraints: token budgets mirror real-world limitations, while retrieval tests ensure merged data remains actionable. This approach balances depth and efficiency better than naive FIFO eviction policies seen in earlier implementations.
- Strategy rationale: The original strategy aimed to retain diverse contexts but struggled with merging sufficient information for cross-event inference tasks. By explicitly defining fusion criteria (geographic/temporal proximity + semantic overlap) and mandating inclusion of specific feature markers ("collapsed buildings"), the revised approach better supports comparative queries (e.g., "Day 1 vs. Day 3 changes"). Summarization reduces token waste without losing retrieval-critical elements, addressing prior failures where identical entries diluted relevance scoring. Metadata anchoring (coordinates + timestamps) enables precise recall despite compression, mitigating issues seen in hurricane/flood tests where deleted entries caused citation errors.
- Change: Added explicit metrics for fusion decisions (proximity thresholds, semantic similarity scores). Introduced mandatory inclusion of predefined keywords (e.g., "submerged", "collapsed") in summaries to ensure retrieval accuracy. Strengthened temporal sequencing logic to preserve chronological evolution cues for change-detection queries. Reduced reliance on full-text storage by capping narrative length to 2 sentences per merged entry. Implemented stricter eviction policies targeting oldest/least-relevant data first when nearing token limits.

## Memory strategy (`f7c034a7dfbf`)

```
Prioritize retaining spatially-temporally distinct events and critical contextual details (e.g., timestamps, locations, unique incident markers like "submerged vehicles") by storing summaries instead of verbatim descriptions. Use semantic similarity thresholds to identify redundant updates—merge temporally proximate duplicates (e.g., sequential images of the same flood zone) into single entries highlighting evolving conditions. Store only essential metadata (ID, timestamp, coordinates) alongside compressed narratives emphasizing actionable details. For example, combine repeated flood imagery showing incremental water levels into a timeline entry noting rising severity. This ensures diversity preservation while adhering to the 512-token limit via aggressive summarization and redundancy elimination during memory updates.
```

## Meta harness (`6b19eb8d1ed9`)

```
**Meta Harness:**  
"Optimize the memory management system by prioritizing retention of diverse spatial-temporal context and critical details (e.g., timestamps, locations, event-specific features like 'submerged vehicles' or 'collapsed buildings'). When adding new items, compare their uniqueness against existing entries using semantic similarity checks rather than strict duplication. If similar content exists within the same geographic or temporal proximity (e.g., multiple images of the same flood zone taken hours apart), merge key details into a consolidated summary. Retain only essential metadata (date/time, location, unique identifiers) alongside summaries to minimize token usage while preserving retrieval accuracy."  

**Evaluation Criteria:**  
1. **Token Efficiency:** Ensure merged/metadata-only storage keeps total memory under 512 tokens per batch.  
2. **Retrieval Accuracy:** Validate that merged entries enable correct answers when queried post-deletion cycles.  
3. **Contextual Preservation:** Maintain ability to answer questions requiring cross-image inferences (e.g., "What changed between Day 1 and Day 3 floods?").
```

## Score

**Node score (mean over streams): 0.16** · correct 4/25 · evidence retained 0.48 · abstained 0.48 · budget fallbacks 10

| stream | items | score | correct | evidence retained | final memory |
|---|---|---|---|---|---|
| `dvqa-hurricane-len10-010` | E01-E10 | 0.2 | 1/5 | 0.4 | 4 lines, 385 tok |
| `dvqa-flood-len10-024` | E01-E10 | 0.2 | 1/5 | 0.4 | 2 lines, 235 tok |
| `dvqa-earthquake-len10-054` | E01-E10 | 0.2 | 1/5 | 0.8 | 6 lines, 439 tok |
| `dvqa-wildfire-len10-064` | E01-E10 | 0.2 | 1/5 | 0.8 | 6 lines, 451 tok |
| `dvqa-fire-len10-066` | E01-E10 | 0.0 | 0/5 | 0.0 | 1 lines, 87 tok |

## Stream `dvqa-hurricane-len10-010` ([evaluation.md](runs/dvqa-hurricane-len10-010/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | What type of disaster is depicted in the image? Select all that apply. | B (Flood) | B (Flood) | `invalid_citation` | no |
| E03 | What type of area is affected? Answer with one or two words. | Residential | Residential area | `correct` | yes |
| E05 | What is the condition of the road? Select all that apply. | B (Partially blocked) | C (Fully blocked) | `wrong_answer_evidence_missing` | no |
| E06 | Is there a fallen tree blocking the road? Answer with Yes or No. | No | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E08 | Are there any fallen trees visible in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m3 [src E03] Social media photo (Twitter) posted 2017-09-19 17:03 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 17:03 UTC.
m8 [src E08] Social media photo (Twitter) posted 2017-09-19 19:20 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 19:20 UTC.
m9 [src E09] Social media photo (Twitter) posted 2017-09-19 19:51 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 19:51 UTC.
m10 [src E10] Social media photo (Twitter) posted 2017-09-19 20:20 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 20:20 UTC.
```

## Stream `dvqa-flood-len10-024` ([evaluation.md](runs/dvqa-flood-len10-024/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E03 | Are there any vehicles submerged in water? Answer with Yes or No. | Yes | Yes | `invalid_citation` | no |
| E04 | What is the primary obstacle on the road? Answer with one or two words. | Floodwater | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. | No | No | `correct` | yes |
| E08 | What infrastructure is affected by the flooding? Select all that apply. | A (Railway) | C (Highway) | `wrong_answer_evidence_missing` | no |
| E10 | What type of vehicle is partially submerged in the water? Select all that apply. | C (Auto-rickshaw) | A (Car) | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m6 [src E06] Social media photo (Twitter) showing a flooded area with submerged vehicles, including a white RV tilted on its side and a partially submerged white trailer. Debris and uprooted trees are visible in the water. Dense trees line the background, and the water appears murky brown. Location: near a road with a guardrail in the foreground. Timestamp: 2015-12-04 03:38 UTC.
m10 [src E10] Social media photo (Twitter) showing a flooded area with submerged vehicles, including a white RV tilted on its side and a partially submerged white trailer. Debris and uprooted trees are visible in the water. Dense trees line the background, and the water appears murky brown. Location: near a road with a guardrail in the foreground. Timestamp: 2015-12-04 17:45 UTC.
```

## Stream `dvqa-earthquake-len10-054` ([evaluation.md](runs/dvqa-earthquake-len10-054/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E04 | What is the primary material of the debris? Answer with one or two words. | Bricks | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E07 | What is the condition of the building in the image? Select all that apply. | C (Collapsed) | C (Collapsed) | `correct` | yes |
| E08 | Is there heavy machinery present in the image? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |
| E09 | Is the debris mostly concrete? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E10 | What is the primary material visible in the debris? Select all that apply. | C (Concrete) | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |

Final memory:

```
m5 [src E05] Image of a woman riding a yellow bicycle with a cargo attachment through a debris-strewn area near a collapsed building. Location: [REDACTED]. Timestamp: 2017-09-21 07:14 UTC.
m6 [src E06] Image of a woman riding a yellow bicycle with a cargo attachment through a debris-strewn area near a collapsed building. Location: [REDACTED]. Timestamp: 2017-09-21 07:16 UTC.
m7 [src E07] Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 08:35 UTC.
m8 [src E08] Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 08:44 UTC.
m9 [src E09] Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 10:33 UTC.
m10 [src E10] Image of a dog walking through debris with scattered clothing and a yellow rope. Location: [REDACTED]. Timestamp: 2017-09-21 10:48 UTC.
```

## Stream `dvqa-wildfire-len10-064` ([evaluation.md](runs/dvqa-wildfire-len10-064/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many people are visible in the image? Select all that apply. | C (Two) | A (None) | `wrong_answer_evidence_missing` | no |
| E06 | What is the primary material burning? Answer with one or two words. | Trees | NOT_ENOUGH_EVIDENCE | `unnecessary_abstention` | yes |
| E07 | What type of disaster is depicted in the image? Select all that apply. | B (Fire) | B (Fire) | `correct` | yes |
| E09 | Are these people watching fireworks? Answer with Yes or No. | No | No | `unsupported` | yes |
| E10 | Are there any emergency responders present? Answer with Yes or No. | Yes | No | `wrong_answer_evidence_in_memory` | yes |

Final memory:

```
m5 [src E05] A social media photo posted on Twitter on October 17, 2017, at 16:04 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
m6 [src E06] A social media photo posted on Twitter on October 18, 2017, at 07:23 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
m7 [src E07] A social media photo posted on Twitter on October 18, 2017, at 20:21 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
m8 [src E08] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
m9 [src E09] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
m10 [src E10] A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
```

## Stream `dvqa-fire-len10-066` ([evaluation.md](runs/dvqa-fire-len10-066/evaluation.md))

| item | question | gold | answer | outcome | evidence in memory |
|---|---|---|---|---|---|
| E01 | How many emergency ladders are deployed? Answer with one or two words. | Four | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E03 | Are there damaged vehicles in the image? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E04 | What type of building is affected by the fire? Select all that apply. | B (Commercial) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E05 | What is the condition of the buildings in the image? Select all that apply. | B (Intact with smoke) | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |
| E06 | Are there residential buildings near the fire? Answer with Yes or No. | Yes | NOT_ENOUGH_EVIDENCE | `abstained_evidence_missing` | no |

Final memory:

```
m10 [src E10] A social media photo posted on 2017-09-08 03:41 UTC shows a fire scene with a burning vehicle and debris scattered around. The timestamp is 2017-09-08 03:41 UTC.
```

## Evaluation log (fed to the meta agent if this node is chosen as a parent)

```
NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.4 of the questions; final memory 4 lines / 385 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=1, correct=1, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* invalid_citation | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence stored at step 1, deleted at step 7
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What type of disaster is depicted in the image? Flood; What is the condition of the roads in the image? Completely flooded
* correct | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Residential area | evidence in memory (stored at step 3)
* wrong_answer_evidence_missing | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: C (Fully blocked) | evidence stored at step 5, deleted at step 8
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* abstained_evidence_missing | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 8
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: Social media photo (Twitter) posted 2017-09-19 19:20 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 19:20 UTC.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/81; 2:2/162; 3:2/177; 4:3/273; 5:4/369; 6:5/465; 7:5/480/budget_evict_oldest; 8:2/192; 9:3/288; 10:4/385
FINAL MEMORY:
  m3 [src E03] Social media photo (Twitter) posted 2017-09-19 17:03 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 17:03 UTC.
  m8 [src E08] Social media photo (Twitter) posted 2017-09-19 19:20 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 19:20 UTC.
  m9 [src E09] Social media photo (Twitter) posted 2017-09-19 19:51 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 19:51 UTC.
  m10 [src E10] Social media photo (Twitter) posted 2017-09-19 20:20 UTC showing a flooded residential area with submerged vehicles and buildings. Water covers roads and yards, with no visible emergency response. Timestamp: 2017-09-19 20:20 UTC.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.4 of the questions; final memory 2 lines / 235 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, invalid_citation=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 6
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* abstained_evidence_missing | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 6
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* correct | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 6)
* wrong_answer_evidence_missing | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: C (Highway) | evidence stored at step 8, deleted at step 10
  memory about E08: (none)
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: Social media photo (Twitter) showing a flooded area with submerged vehicles, including a white RV tilted on its side and a partially submerged white trailer. Debris and uprooted trees are visible in the water. Dense trees line the background, and the water appears murky brown. Location: near a road with a guardrail in the foreground. Timestamp: 2015-12-04 17:45 UTC.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/110; 2:2/206; 3:2/220; 4:3/337; 5:4/454; 6:2/227; 7:2/234; 8:3/351; 9:4/468; 10:2/235
FINAL MEMORY:
  m6 [src E06] Social media photo (Twitter) showing a flooded area with submerged vehicles, including a white RV tilted on its side and a partially submerged white trailer. Debris and uprooted trees are visible in the water. Dense trees line the background, and the water appears murky brown. Location: near a road with a guardrail in the foreground. Timestamp: 2015-12-04 03:38 UTC.
  m10 [src E10] Social media photo (Twitter) showing a flooded area with submerged vehicles, including a white RV tilted on its side and a partially submerged white trailer. Debris and uprooted trees are visible in the water. Dense trees line the background, and the water appears murky brown. Location: near a road with a guardrail in the foreground. Timestamp: 2015-12-04 17:45 UTC.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 6 lines / 439 tokens; budget fallbacks 3).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 10
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* wrong_answer_evidence_in_memory | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 8)
  memory about E08: Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 08:44 UTC.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 10:33 UTC.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: Image of a dog walking through debris with scattered clothing and a yellow rope. Location: [REDACTED]. Timestamp: 2017-09-21 10:48 UTC.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/88; 2:2/199; 3:2/166; 4:3/246; 5:4/326; 6:5/406; 7:6/475; 8:6/461/budget_evict_oldest; 9:6/447/budget_evict_oldest; 10:6/439/budget_evict_oldest
FINAL MEMORY:
  m5 [src E05] Image of a woman riding a yellow bicycle with a cargo attachment through a debris-strewn area near a collapsed building. Location: [REDACTED]. Timestamp: 2017-09-21 07:14 UTC.
  m6 [src E06] Image of a woman riding a yellow bicycle with a cargo attachment through a debris-strewn area near a collapsed building. Location: [REDACTED]. Timestamp: 2017-09-21 07:16 UTC.
  m7 [src E07] Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 08:35 UTC.
  m8 [src E08] Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 08:44 UTC.
  m9 [src E09] Image of a collapsed building with a car partially buried in debris. Location: [REDACTED]. Timestamp: 2017-09-21 10:33 UTC.
  m10 [src E10] Image of a dog walking through debris with scattered clothing and a yellow rope. Location: [REDACTED]. Timestamp: 2017-09-21 10:48 UTC.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 6 lines / 451 tokens; budget fallbacks 3).
OUTCOMES: correct=1, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: A (None) | evidence stored at step 1, deleted at step 8
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo posted on Twitter on October 18, 2017, at 07:23 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/120; 2:2/194; 3:2/195; 4:3/270; 5:4/345; 6:5/420; 7:6/495; 8:6/450/budget_evict_oldest; 9:6/450/budget_evict_oldest; 10:6/451/budget_evict_oldest
FINAL MEMORY:
  m5 [src E05] A social media photo posted on Twitter on October 17, 2017, at 16:04 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  m6 [src E06] A social media photo posted on Twitter on October 18, 2017, at 07:23 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  m7 [src E07] A social media photo posted on Twitter on October 18, 2017, at 20:21 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  m8 [src E08] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  m9 [src E09] A social media photo posted on Twitter on October 19, 2017, at 07:36 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.
  m10 [src E10] A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC, depicting a wildfire scene with flames and smoke in a natural outdoor setting. The location is unspecified.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.0 of the questions; final memory 1 lines / 87 tokens; budget fallbacks 3).
OUTCOMES: abstained_evidence_missing=5

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 1, deleted at step 7
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 8
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* abstained_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 9
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* abstained_evidence_missing | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 10
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* abstained_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 10
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/121; 2:2/233; 3:2/207; 4:3/293; 5:4/379; 6:5/465; 7:5/430/budget_evict_oldest; 8:5/430/budget_evict_oldest; 9:5/430/budget_evict_oldest; 10:1/87
FINAL MEMORY:
  m10 [src E10] A social media photo posted on 2017-09-08 03:41 UTC shows a fire scene with a burning vehicle and debris scattered around. The timestamp is 2017-09-08 03:41 UTC.
```
