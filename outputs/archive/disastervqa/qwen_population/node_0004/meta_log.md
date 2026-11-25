NODE SCORE: 0.24 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.2, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 328 tokens; budget fallbacks 0).
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
  memory about E05: A social media photo shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/40; 2:2/81; 3:2/81; 4:2/81; 5:3/122; 6:4/163; 7:5/204; 8:6/245; 9:7/286; 10:8/328
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with submerged vehicles and buildings.
  m4 [src E04] A social media photo shows a flooded area with submerged vehicles and buildings.
  m5 [src E05] A social media photo shows a flooded area with submerged vehicles and buildings.
  m6 [src E06] A social media photo shows a flooded area with submerged vehicles and buildings.
  m7 [src E07] A social media photo shows a flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media photo shows a flooded area with submerged vehicles and buildings.
  m9 [src E09] A social media photo shows a flooded area with submerged vehicles and buildings.
  m10 [src E10] A social media photo shows a flooded area with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 325 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Floodwater | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a flooded street with vehicles partially submerged in water.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: C (Highway) | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a flooded street with vehicles partially submerged in water.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* unnecessary_abstention | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a flooded street with vehicles partially submerged in water.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/33; 2:2/72; 3:2/72; 4:2/72; 5:3/113; 6:4/156; 7:5/198; 8:6/240; 9:7/282; 10:8/325
FINAL MEMORY:
  m1 [src E01] A flooded street with vehicles partially submerged in water.
  m4 [src E04] A flooded street with vehicles partially submerged in water
  m5 [src E05] A man is swimming in the floodwater, holding onto a rope.
  m6 [src E06] A social media photo shows a flooded street with vehicles partially submerged in water.
  m7 [src E07] A social media photo shows a flooded street with vehicles partially submerged in water.
  m8 [src E08] A social media photo shows a flooded street with vehicles partially submerged in water.
  m9 [src E09] A social media photo shows a flooded street with vehicles partially submerged in water.
  m10 [src E10] A social media photo shows a flooded street with vehicles partially submerged in water.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.8; evidence still in memory for 1.0 of the questions; final memory 8 lines / 329 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a scene of destruction after a building collapse.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* unnecessary_abstention | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a scene of destruction after a building collapse.
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a scene of destruction after a building collapse.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a scene of destruction after a building collapse.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/41; 2:2/82; 3:2/82; 4:2/82; 5:3/123; 6:4/164; 7:5/205; 8:6/246; 9:7/287; 10:8/329
FINAL MEMORY:
  m1 [src E01] A social media photo shows a scene of destruction after a building collapse.
  m4 [src E04] A social media photo shows a scene of destruction after a building collapse.
  m5 [src E05] A social media photo shows a scene of destruction after a building collapse.
  m6 [src E06] A social media photo shows a scene of destruction after a building collapse.
  m7 [src E07] A social media photo shows a scene of destruction after a building collapse.
  m8 [src E08] A social media photo shows a scene of destruction after a building collapse.
  m9 [src E09] A social media photo shows a scene of destruction after a building collapse.
  m10 [src E10] A social media photo shows a scene of destruction after a building collapse.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 1.0 of the questions; final memory 8 lines / 419 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=2, unsupported=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo (Twitter) was posted on 2017-10-18 07:23 UTC.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo (Twitter) was posted on 2017-10-19 07:36 UTC.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* unnecessary_abstention | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo (Twitter) was posted on 2017-10-20 11:11 UTC.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/44; 2:2/91; 3:2/91; 4:2/91; 5:3/138; 6:4/194; 7:5/250; 8:6/306; 9:7/362; 10:8/419
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning area with flames and smoke in the background.
  m4 [src E04] A social media photo shows two people running through a burning area with flames and smoke in the background.
  m5 [src E05] A social media photo shows two people running through a burning area with flames and smoke in the background.
  m6 [src E06] A social media photo (Twitter) was posted on 2017-10-18 07:23 UTC.
  m7 [src E07] A social media photo (Twitter) was posted on 2017-10-18 20:21 UTC.
  m8 [src E08] A social media photo (Twitter) was posted on 2017-10-19 07:36 UTC.
  m9 [src E09] A social media photo (Twitter) was posted on 2017-10-19 07:36 UTC.
  m10 [src E10] A social media photo (Twitter) was posted on 2017-10-20 11:11 UTC.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.8 of the questions; final memory 8 lines / 336 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=2, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire is burning in a multi-story building.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_in_memory | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: C (High-rise) | evidence in memory (stored at step 4)
  memory about E04: A social media photo shows a large fire burning in a multi-story building.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media photo shows a large fire burning in a multi-story building.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/38; 2:2/76; 3:2/80; 4:2/80; 5:3/122; 6:4/164; 7:5/206; 8:6/248; 9:7/290; 10:8/336
FINAL MEMORY:
  m1 [src E01] A large fire is burning in a multi-story building.
  m4 [src E04] A social media photo shows a large fire burning in a multi-story building.
  m5 [src E05] A social media photo shows a large fire burning in a multi-story building.
  m6 [src E06] A social media photo shows a large fire burning in a multi-story building.
  m7 [src E07] A social media photo shows a large fire burning in a multi-story building.
  m8 [src E08] A social media photo shows a large fire burning in a multi-story building.
  m9 [src E09] A social media photo shows a large fire burning in a multi-story building.
  m10 [src E10] A social media photo posted on Twitter shows a large fire burning in a multi-story building.
