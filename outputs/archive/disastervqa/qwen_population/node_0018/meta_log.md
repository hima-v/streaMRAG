NODE SCORE: 0.16 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.2
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.4 of the questions; final memory 4 lines / 182 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, invalid_citation=2, unnecessary_abstention=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence in memory (stored at step 1)
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Flooded area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* invalid_citation | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: B (Partially blocked) | evidence stored at step 5, deleted at step 6
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* abstained_evidence_missing | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 8
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: A social media photo shows a group of people clearing debris from a road near a body of water.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/40; 2:2/81; 3:2/80; 4:2/87; 5:3/134; 6:2/87; 7:3/134; 8:2/87; 9:3/134; 10:4/182
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media photo shows a group of people clearing debris from a road near a body of water.
  m9 [src E09] A social media photo shows a group of people clearing debris from a road near a body of water.
  m10 [src E10] A social media photo shows a group of people clearing debris from a road near a body of water.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 301 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, correct=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* correct | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Floodwater | evidence in memory (stored at step 4)
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: People walking through floodwater
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: People are being rescued from floodwater by military personnel in a boat.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: People are being rescued from floodwater by military personnel in a boat.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/33; 2:2/66; 3:2/66; 4:2/65; 5:3/104; 6:4/136; 7:5/177; 8:6/218; 9:7/259; 10:8/301
FINAL MEMORY:
  m1 [src E01] Floodwater submerging vehicles
  m4 [src E04] People walking through floodwater
  m5 [src E05] A man is swimming in floodwater holding onto a rope.
  m6 [src E06] People walking through floodwater
  m7 [src E07] People are being rescued from floodwater by military personnel in a boat.
  m8 [src E08] People are being rescued from floodwater by military personnel in a boat.
  m9 [src E09] People are being rescued from floodwater by military personnel in a boat.
  m10 [src E10] People are being rescued from floodwater by military personnel in a boat.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.2 of the questions; final memory 2 lines / 161 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 6
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
* abstained_evidence_missing | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 9, deleted at step 10
  memory about E09: (none)
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* unnecessary_abstention | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a group of people gathered around a collapsed building. The debris is scattered across the ground, and there are rescue workers in high-visibility vests and helmets. The scene is illuminated by sunlight, and there are trees in the background.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/56; 2:2/107; 3:2/108; 4:2/108; 5:3/188; 6:2/160; 7:2/160; 8:2/160; 9:2/160; 10:2/161
FINAL MEMORY:
  m1 [src E01] A social media photo shows a group of people gathered around a collapsed building. The debris is scattered across the ground, and there are rescue workers in high-visibility vests and helmets. The scene is illuminated by sunlight, and there are trees in the background.
  m10 [src E10] A social media photo shows a group of people gathered around a collapsed building. The debris is scattered across the ground, and there are rescue workers in high-visibility vests and helmets. The scene is illuminated by sunlight, and there are trees in the background.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 5 lines / 211 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=1, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_in_memory | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: A (None) | evidence in memory (stored at step 1)
  memory about E01: A social media photo shows a wildfire burning in a forested area.
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* invalid_citation | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: Forest | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media photo shows a wildfire burning in a forested area.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* unnecessary_abstention | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 10)
  memory about E10: A social media photo shows a wildfire burning in a forested area.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/54; 2:2/84; 3:2/84; 4:2/84; 5:2/84; 6:2/84; 7:2/84; 8:3/126; 9:4/168; 10:5/211
FINAL MEMORY:
  m1 [src E01] A social media photo shows a wildfire burning in a forested area.
  m7 [src E07] A social media photo shows a wildfire burning in a forested area.
  m8 [src E08] A social media photo shows a wildfire burning in a forested area.
  m9 [src E09] A social media photo shows a wildfire burning in a forested area.
  m10 [src E10] A social media photo shows a wildfire burning in a forested area.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 1.0 of the questions; final memory 9 lines / 455 tokens; budget fallbacks 0).
OUTCOMES: correct=1, unnecessary_abstention=3, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* wrong_answer_evidence_in_memory | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 3)
  memory about E03: A car is on fire in a parking lot with debris scattered around. Smoke is rising from the car, and there are no visible emergency responders or fire trucks in the scene.
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* unnecessary_abstention | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: A fire is burning in a building with flames visible on the roof. Fire trucks and firefighters are present at the scene.
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* correct | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence in memory (stored at step 5)
* unnecessary_abstention | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/70; 2:2/113; 3:2/90; 4:3/142; 5:4/194; 6:5/242; 7:6/310; 8:7/358; 9:8/406; 10:9/455
FINAL MEMORY:
  m1 [src E01] A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  m3 [src E03] A car is on fire in a parking lot with debris scattered around. Smoke is rising from the car, and there are no visible emergency responders or fire trucks in the scene.
  m4 [src E04] A fire is burning in a building with flames visible on the roof. Fire trucks and firefighters are present at the scene.
  m5 [src E05] A fire is burning in a building with flames visible on the roof. Fire trucks and firefighters are present at the scene.
  m6 [src E06] A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  m7 [src E07] A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  m8 [src E08] A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  m9 [src E09] A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
  m10 [src E10] A fire is burning in a building with flames visible on the roof. Smoke is rising from the building.
