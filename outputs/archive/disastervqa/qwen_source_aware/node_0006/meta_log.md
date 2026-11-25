NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.2, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.4, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.8 of the questions; final memory 8 lines / 420 tokens; budget fallbacks 0).
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
  memory about E08: A social media photo posted on Twitter at 19:20 UTC on September 19, 2017, shows a flooded area with submerged vehicles and buildings.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/40; 2:2/81; 3:2/81; 4:2/81; 5:3/122; 6:4/163; 7:5/227; 8:6/291; 9:7/355; 10:8/420
FINAL MEMORY:
  m1 [src E01] Aerial view of a flooded area with submerged vehicles and buildings.
  m4 [src E04] A social media photo shows a flooded area with submerged vehicles and buildings.
  m5 [src E05] A social media photo shows a flooded area with submerged vehicles and buildings.
  m6 [src E06] A social media photo shows a flooded area with submerged vehicles and buildings.
  m7 [src E07] A social media photo posted on Twitter at 18:40 UTC on September 19, 2017, shows a flooded area with submerged vehicles and buildings.
  m8 [src E08] A social media photo posted on Twitter at 19:20 UTC on September 19, 2017, shows a flooded area with submerged vehicles and buildings.
  m9 [src E09] A social media photo posted on Twitter at 19:51 UTC on September 19, 2017, shows a flooded area with submerged vehicles and buildings.
  m10 [src E10] A social media photo posted on Twitter at 20:20 UTC on September 19, 2017, shows a flooded area with submerged vehicles and buildings.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.2 of the questions; final memory 2 lines / 133 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=2, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* abstained_evidence_missing | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_missing | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: C (Highway) | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC, showing a flooded area with submerged vehicles and collapsed buildings.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/66; 2:2/132; 3:2/132; 4:2/132; 5:2/132; 6:2/132; 7:2/132; 8:2/132; 9:2/132; 10:2/133
FINAL MEMORY:
  m1 [src E01] A social media photo was posted on Twitter on October 8, 2015, at 23:05 UTC, showing a flooded area with submerged vehicles and collapsed buildings.
  m10 [src E10] A social media photo was posted on Twitter on December 4, 2015, at 17:45 UTC, showing a flooded area with submerged vehicles and collapsed buildings.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.2 of the questions; final memory 2 lines / 171 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=2, unnecessary_abstention=1, wrong_answer_evidence_missing=2

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 5
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* wrong_answer_evidence_missing | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: A (Intact) | evidence stored at step 7, deleted at step 9
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
  memory about E10: A social media photo from Twitter shows a silver car parked on a street with a large crack in the asphalt. There are people standing around the car, including a police officer and a man in a red shirt. The scene appears to be in a city with a modern building in the background.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/42; 2:2/107; 3:2/170; 4:2/170; 5:2/170; 6:2/170; 7:2/113; 8:3/255; 9:2/170; 10:2/171
FINAL MEMORY:
  m1 [src E01] A social media photo from Twitter shows a silver car parked on a street with a large crack in the asphalt. There are people standing around the car, including a police officer and a man in a red shirt. The scene appears to be in a city with a modern building in the background.
  m10 [src E10] A social media photo from Twitter shows a silver car parked on a street with a large crack in the asphalt. There are people standing around the car, including a police officer and a man in a red shirt. The scene appears to be in a city with a modern building in the background.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 1.0 of the questions; final memory 8 lines / 441 tokens; budget fallbacks 0).
OUTCOMES: correct=2, unnecessary_abstention=1, unsupported=1, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* unnecessary_abstention | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* correct | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence in memory (stored at step 7)
* unsupported | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence in memory (stored at step 9)
  memory about E09: A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
  evaluator: unsupported - The image shows a wildfire, not fireworks.
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/69; 2:2/122; 3:2/122; 4:2/122; 5:3/175; 6:4/228; 7:5/281; 8:6/334; 9:7/387; 10:8/441
FINAL MEMORY:
  m1 [src E01] Two people are seen running through a burning landscape, with flames engulfing the ground and charred tree stumps. The scene is dark and smoky, with the fire casting an eerie red glow.
  m4 [src E04] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  m5 [src E05] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  m6 [src E06] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  m7 [src E07] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  m8 [src E08] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  m9 [src E09] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.
  m10 [src E10] A social media user posted a photo of the burning landscape on Twitter, showing a trail of fire and smoke rising into the sky.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.4 of the questions; final memory 6 lines / 510 tokens; budget fallbacks 0).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 1)
  memory about E01: A large fire broke out in a multi-story building at night, with multiple fire trucks and emergency responders on the scene. The building has several fire escapes and ladders are being used to access the upper floors. There are many firefighters and paramedics present, and an American flag is visible in the background. The scene is chaotic and intense, with smoke and lights illuminating the area.
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
  memory about E06: A social media photo was posted on July 21, 2017, at 00:43 UTC, showing a large fire in a multi-story building at night. The scene is chaotic and intense, with smoke and lights illuminating the area.
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/106; 2:2/187; 3:2/186; 4:2/187; 5:2/187; 6:2/187; 7:3/268; 8:4/349; 9:5/429; 10:6/510
FINAL MEMORY:
  m1 [src E01] A large fire broke out in a multi-story building at night, with multiple fire trucks and emergency responders on the scene. The building has several fire escapes and ladders are being used to access the upper floors. There are many firefighters and paramedics present, and an American flag is visible in the background. The scene is chaotic and intense, with smoke and lights illuminating the area.
  m6 [src E06] A social media photo was posted on July 21, 2017, at 00:43 UTC, showing a large fire in a multi-story building at night. The scene is chaotic and intense, with smoke and lights illuminating the area.
  m7 [src E07] A social media photo was posted on August 23, 2017, at 00:46 UTC, showing a large fire in a multi-story building at night. The scene is chaotic and intense, with smoke and lights illuminating the area.
  m8 [src E08] A social media photo was posted on August 28, 2017, at 10:43 UTC, showing a large fire in a multi-story building at night. The scene is chaotic and intense, with smoke and lights illuminating the area.
  m9 [src E09] A social media photo was posted on September 6, 2017, at 09:22 UTC, showing a large fire in a multi-story building at night. The scene is chaotic and intense, with smoke and lights illuminating the area.
  m10 [src E10] A social media photo was posted on September 8, 2017, at 03:41 UTC, showing a large fire in a multi-story building at night. The scene is chaotic and intense, with smoke and lights illuminating the area.
