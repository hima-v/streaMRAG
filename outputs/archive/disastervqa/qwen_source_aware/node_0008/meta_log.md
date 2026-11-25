NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 396 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=1, unnecessary_abstention=3

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* unnecessary_abstention | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 5)
  memory about E05: A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo posted on Twitter at 19:20 UTC shows a flooded area with multiple buildings and vehicles submerged in water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/84; 3:2/87; 4:2/87; 5:3/131; 6:4/175; 7:5/230; 8:6/285; 9:7/340; 10:8/396
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with multiple buildings and vehicles submerged in water.
  m4 [src E04] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m5 [src E05] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m6 [src E06] A social media photo shows a flooded area with multiple buildings and vehicles submerged in water.
  m7 [src E07] A social media photo posted on Twitter at 18:40 UTC shows a flooded area with multiple buildings and vehicles submerged in water.
  m8 [src E08] A social media photo posted on Twitter at 19:20 UTC shows a flooded area with multiple buildings and vehicles submerged in water.
  m9 [src E09] A social media photo posted on Twitter at 19:51 UTC shows a flooded area with multiple buildings and vehicles submerged in water.
  m10 [src E10] A social media photo posted on Twitter at 20:20 UTC shows a flooded area with multiple buildings and vehicles submerged in water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.8 of the questions; final memory 8 lines / 402 tokens; budget fallbacks 0).
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
  memory about E10: A man is swimming in a dirty brown river, holding onto a rope.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/55; 2:2/110; 3:2/110; 4:2/110; 5:3/152; 6:4/207; 7:5/262; 8:6/317; 9:7/359; 10:8/402
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on December 4, 2015, at 08:05 UTC.
  m4 [src E04] A social media photo was posted on Twitter on December 3, 2015, at 17:20 UTC.
  m5 [src E05] A man is swimming in a dirty brown river, holding onto a rope.
  m6 [src E06] A social media photo was posted on Twitter on December 4, 2015, at 03:38 UTC.
  m7 [src E07] A social media photo was posted on Twitter on December 4, 2015, at 04:24 UTC.
  m8 [src E08] A social media photo was posted on Twitter on December 4, 2015, at 07:54 UTC.
  m9 [src E09] A man is swimming in a dirty brown river, holding onto a rope.
  m10 [src E10] A man is swimming in a dirty brown river, holding onto a rope.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 0.2 of the questions; final memory 2 lines / 155 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=3, unnecessary_abstention=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* abstained_evidence_missing | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* wrong_answer_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* abstained_evidence_missing | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 9, deleted at step 10
  memory about E09: (none)
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo posted on Twitter shows a black car parked on a cracked road with debris around it. There are several people standing around the car, including a police officer and a man in a red shirt. The scene appears to be in daylight.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/99; 2:2/98; 3:2/154; 4:2/154; 5:2/154; 6:2/154; 7:2/154; 8:2/154; 9:2/154; 10:2/155
FINAL MEMORY:
  m1 [src E01] A social media photo posted on Twitter shows a black car parked on a cracked road with debris around it. There are several people standing around the car, including a police officer and a man in a red shirt. The scene appears to be in daylight.
  m10 [src E10] A social media photo posted on Twitter shows a black car parked on a cracked road with debris around it. There are several people standing around the car, including a police officer and a man in a red shirt. The scene appears to be in daylight.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 1.0 of the questions; final memory 9 lines / 433 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=2, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_in_memory | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: A (None) | evidence in memory (stored at step 1)
  cited memory line(s) that do not exist: m2
  memory about E01: m1 [src E01 @2017-10-12 03:11 UTC] ...
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: ...
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* unnecessary_abstention | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter), posted 2017-10-20 11:11 UTC.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/43; 2:2/83; 3:2/83; 4:3/123; 5:4/177; 6:5/231; 7:6/285; 8:7/339; 9:8/352; 10:9/433
FINAL MEMORY:
  m1 [src E01] m1 [src E01 @2017-10-12 03:11 UTC] ...
  m3 [src E03] A social media photo shows a burning landscape with flames and smoke.
  m4 [src E04] A social media photo shows a burning landscape with flames and smoke.
  m5 [src E05] A social media photo (Twitter), posted 2017-10-17 16:04 UTC.
  m6 [src E06] A social media photo (Twitter), posted 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter), posted 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter), posted 2017-10-19 07:36 UTC.
  m9 [src E09] ...
  m10 [src E10] A social media photo (Twitter), posted 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.6 of the questions; final memory 7 lines / 493 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=2, correct=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 1, deleted at step 9
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_in_memory | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: C (High-rise) | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/109; 2:2/148; 3:2/184; 4:2/184; 5:3/259; 6:4/334; 7:5/409; 8:6/484; 9:6/450/budget_evict_source_aware; 10:7/493
FINAL MEMORY:
  m4 [src E04] A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  m5 [src E05] A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  m6 [src E06] A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  m7 [src E07] A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  m8 [src E08] A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  m9 [src E09] A social media photo shows a large fire burning in a multi-story building. The fire is causing significant damage to the structure, and there are reports of people trapped inside. Emergency responders are working to rescue those who are still inside the building.
  m10 [src E10] A social media photo shows a large fire burning in a multi-story building.
