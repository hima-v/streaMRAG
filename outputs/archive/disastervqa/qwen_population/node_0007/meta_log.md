NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 4 lines / 168 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo shows a flooded area with multiple buildings submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/82; 3:2/83; 4:2/83; 5:2/83; 6:2/83; 7:2/83; 8:2/83; 9:3/125; 10:4/168
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with multiple buildings submerged in water.
  m8 [src E08] A social media photo shows a flooded area with multiple buildings submerged in water.
  m9 [src E09] A social media photo shows a flooded area with multiple buildings submerged in water.
  m10 [src E10] A social media photo shows a flooded area with multiple buildings submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 371 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: Social media photo (Twitter), posted 2015-12-04 03:38 UTC.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: A man is seen swimming in the water, holding onto a rope.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A man is seen swimming in the water, holding onto a rope.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/59; 2:2/115; 3:2/112; 4:2/112; 5:3/153; 6:4/206; 7:5/247; 8:6/288; 9:7/329; 10:8/371
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with multiple RVs submerged in water. The water level is high, and the surrounding area is covered in trees and vegetation.
  m4 [src E04] Social media photo (Twitter), posted 2015-12-03 17:20 UTC.
  m5 [src E05] A man is seen swimming in the water, holding onto a rope.
  m6 [src E06] Social media photo (Twitter), posted 2015-12-04 03:38 UTC.
  m7 [src E07] A man is seen swimming in the water, holding onto a rope.
  m8 [src E08] A man is seen swimming in the water, holding onto a rope.
  m9 [src E09] A man is seen swimming in the water, holding onto a rope.
  m10 [src E10] A man is seen swimming in the water, holding onto a rope.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.6 of the questions; final memory 4 lines / 166 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo from Twitter shows a collapsed building with debris scattered around.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo from Twitter shows a collapsed building with debris scattered around.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo from Twitter shows a collapsed building with debris scattered around.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/39; 2:2/83; 3:2/78; 4:2/81; 5:2/81; 6:2/81; 7:2/81; 8:2/81; 9:3/123; 10:4/166
FINAL MEMORY:
  m1 [src E01] Aerial view of a collapsed building with debris scattered around.
  m8 [src E08] A social media photo from Twitter shows a collapsed building with debris scattered around.
  m9 [src E09] A social media photo from Twitter shows a collapsed building with debris scattered around.
  m10 [src E10] A social media photo from Twitter shows a collapsed building with debris scattered around.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 393 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC shows a burning landscape with multiple small fires and charred tree stumps.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/47; 2:2/93; 3:2/93; 4:2/93; 5:3/139; 6:4/185; 7:5/231; 8:6/277; 9:7/323; 10:8/393
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape with multiple small fires and charred tree stumps.
  m4 [src E04] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m5 [src E05] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m6 [src E06] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m7 [src E07] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m8 [src E08] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m9 [src E09] A social media photo shows a burning landscape with multiple small fires and charred tree stumps.
  m10 [src E10] A social media photo posted on Twitter on October 20, 2017, at 11:11 UTC shows a burning landscape with multiple small fires and charred tree stumps.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.2 of the questions; final memory 4 lines / 167 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire broke out in a multi-story building at night.
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
* abstained_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/40; 2:2/82; 3:2/82; 4:2/82; 5:2/82; 6:2/82; 7:2/82; 8:2/82; 9:3/124; 10:4/167
FINAL MEMORY:
  m1 [src E01] A large fire broke out in a multi-story building at night.
  m8 [src E08] A social media photo shows a large fire burning in a multi-story building.
  m9 [src E09] A social media photo shows a large fire burning in a multi-story building.
  m10 [src E10] A social media photo shows a large fire burning in a multi-story building.
