NODE SCORE: 0.08 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.0, dvqa-flood-len10-024 0.2, dvqa-earthquake-len10-054 0.0, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.0 of the questions; final memory 3 lines / 286 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=2, invalid_citation=2, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* invalid_citation | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: B (Flood) | evidence stored at step 1, deleted at step 7
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What type of disaster is depicted in the image? Flood; What is the condition of the roads in the image? Completely flooded
* invalid_citation | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: Residential area | evidence stored at step 3, deleted at step 4
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* abstained_evidence_missing | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 5, deleted at step 9
  memory about E05: (none)
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* abstained_evidence_missing | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 9
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* wrong_answer_evidence_missing | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/69; 2:2/138; 3:2/138; 4:2/254; 5:3/349; 6:4/444; 7:4/380/budget_evict_oldest; 8:5/475; 9:2/190; 10:3/286
FINAL MEMORY:
  m4 [src E04] Aerial view of a flooded residential area with submerged vehicles and buildings, including a white-roofed structure with a parking lot filled with cars, surrounded by greenery and trees, indicating a natural disaster event. Social media photo (Twitter), posted 2017-09-19 18:03 UTC.
  m9 [src E09] Aerial view of a flooded residential area with submerged vehicles and buildings, including a white-roofed structure with a parking lot filled with cars, surrounded by greenery and trees, indicating a natural disaster event. Social media photo (Twitter), posted 2017-09-19 19:51 UTC.
  m10 [src E10] Aerial view of a flooded residential area with submerged vehicles and buildings, including a white-roofed structure with a parking lot filled with cars, surrounded by greenery and trees, indicating a natural disaster event. Social media photo (Twitter), posted 2017-09-19 20:20 UTC.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.8 of the questions; final memory 4 lines / 461 tokens; budget fallbacks 1).
OUTCOMES: correct=1, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=2

PER QUESTION (asked after the last photo):
* correct | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence in memory (stored at step 3)
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Floodwaters | evidence stored at step 4, deleted at step 8
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: A group of individuals is navigating through floodwaters, with some standing in the water and others on a partially submerged structure. The water level reaches mid-thigh for most individuals, and the environment includes damaged structures and submerged vehicles. The scene is set in a forested area with dense trees and a metal guardrail visible in the foreground.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_in_memory | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: D (Residential area) | evidence in memory (stored at step 8)
  memory about E08: A man is seen in the floodwaters holding a long stick, possibly for support or navigation. The water appears murky and is moving, indicating a strong current. The man is wearing a white shirt, and the surrounding area is heavily affected by the flood, with submerged vehicles and debris visible. Dense trees border the scene, and a metal guardrail is visible in the foreground. | A group of individuals is navigating through floodwaters, with some standing in the water and others on a partially submerged structure. The water level reaches mid-thigh for most individuals, and the environment includes damaged structures and submerged vehicles. The scene is set in a forested area with dense trees and a metal guardrail visible in the foreground.
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: A group of individuals is navigating through floodwaters, with some standing in the water and others on a partially submerged structure. The water level reaches mid-thigh for most individuals, and the environment includes damaged structures and submerged vehicles. The scene is set in a forested area with dense trees and a metal guardrail visible in the foreground. | A social media photo (Twitter) posted on 2015-12-04 17:45 UTC shows a group of individuals navigating through floodwaters. The water level reaches mid-thigh for most individuals, and the environment includes damaged structures and submerged vehicles. The scene is set in a forested area with dense trees and a metal guardrail visible in the foreground.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/82; 2:2/167; 3:2/170; 4:3/258; 5:4/381; 6:5/476; 7:5/453/budget_evict_oldest; 8:3/331; 9:4/426; 10:4/461
FINAL MEMORY:
  m3 [src E03] Social media photo (Twitter) showing flood aftermath with submerged vehicles and damaged RVs in a forested area. Water level submerges multiple trailers, including a white RV tilted on its side with debris entangled. Dense trees border the scene, and a metal guardrail is visible in the foreground.
  m5 [src E05, E08] A man is seen in the floodwaters holding a long stick, possibly for support or navigation. The water appears murky and is moving, indicating a strong current. The man is wearing a white shirt, and the surrounding area is heavily affected by the flood, with submerged vehicles and debris visible. Dense trees border the scene, and a metal guardrail is visible in the foreground.
  m6 [src E06, E08, E10] A group of individuals is navigating through floodwaters, with some standing in the water and others on a partially submerged structure. The water level reaches mid-thigh for most individuals, and the environment includes damaged structures and submerged vehicles. The scene is set in a forested area with dense trees and a metal guardrail visible in the foreground.
  m9 [src E10] A social media photo (Twitter) posted on 2015-12-04 17:45 UTC shows a group of individuals navigating through floodwaters. The water level reaches mid-thigh for most individuals, and the environment includes damaged structures and submerged vehicles. The scene is set in a forested area with dense trees and a metal guardrail visible in the foreground.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.4 of the questions; final memory 3 lines / 495 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=1, invalid_citation=1, unnecessary_abstention=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 6
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* invalid_citation | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence stored at step 7, deleted at step 9
  memory about E07: (none)
  what the photo actually shows (dataset facts): Are there any vehicles trapped under debris? Yes; How many vehicles are visible in the image? One; What is the condition of the building in the image? Collapsed
* wrong_answer_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* unnecessary_abstention | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 9)
  memory about E09: A social media photo posted on Twitter at 2017-09-21 10:33 UTC shows a collapsed building with exposed rebar and debris. Workers in safety gear, including a white helmet and green vest, are on ladders, and tangled power lines are visible. A submerged black Toyota Corolla with license plate '152-406' is partially elevated over a large crack, with a man in a maroon shirt and white sneakers observing it. A police officer in a black uniform with 'POLICIA FEDERAL' raises his hand, and another worker in a high-visibility vest examines the area.
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* wrong_answer_evidence_in_memory | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: B (Metal) | evidence in memory (stored at step 10)
  memory about E10: A social media photo posted on Twitter at 2017-09-21 10:48 UTC shows a collapsed building with exposed rebar and debris. Workers in safety gear, including a white helmet and green vest, are on ladders, and tangled power lines are visible. A submerged black Toyota Corolla with license plate '152-406' is partially elevated over a large crack, with a man in a maroon shirt and white sneakers observing it. A police officer in a black uniform with 'POLICIA FEDERAL' raises his hand, and another worker in a high-visibility vest examines the area.
  what the photo actually shows (dataset facts): What is the primary material visible in the debris? Concrete; How many dogs are visible? One
MEMORY PER STEP (lines / tokens / fallback): 1:1/110; 2:2/339; 3:2/376; 4:2/330/budget_evict_oldest; 5:3/495; 6:1/165; 7:2/330; 8:3/495; 9:2/330; 10:3/495
FINAL MEMORY:
  m3 [src E03] A social media photo posted on Twitter at 2017-09-21 06:18 UTC shows a collapsed building with exposed rebar and debris. Workers in safety gear, including a white helmet and green vest, are on ladders, and tangled power lines are visible. A submerged black Toyota Corolla with license plate '152-406' is partially elevated over a large crack, with a man in a maroon shirt and white sneakers observing it. A police officer in a black uniform with 'POLICIA FEDERAL' raises his hand, and another worker in a high-visibility vest examines the area.
  m8 [src E09] A social media photo posted on Twitter at 2017-09-21 10:33 UTC shows a collapsed building with exposed rebar and debris. Workers in safety gear, including a white helmet and green vest, are on ladders, and tangled power lines are visible. A submerged black Toyota Corolla with license plate '152-406' is partially elevated over a large crack, with a man in a maroon shirt and white sneakers observing it. A police officer in a black uniform with 'POLICIA FEDERAL' raises his hand, and another worker in a high-visibility vest examines the area.
  m9 [src E10] A social media photo posted on Twitter at 2017-09-21 10:48 UTC shows a collapsed building with exposed rebar and debris. Workers in safety gear, including a white helmet and green vest, are on ladders, and tangled power lines are visible. A submerged black Toyota Corolla with license plate '152-406' is partially elevated over a large crack, with a man in a maroon shirt and white sneakers observing it. A police officer in a black uniform with 'POLICIA FEDERAL' raises his hand, and another worker in a high-visibility vest examines the area.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.2 of the questions; final memory 5 lines / 460 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=1, correct=1, invalid_citation=3

PER QUESTION (asked after the last photo):
* invalid_citation | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence stored at step 1, deleted at step 10
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there any visible water source in the image? No; What type of disaster is depicted in the image? Wildfire; How many people are visible in the image? Two
* abstained_evidence_missing | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: NOT_ENOUGH_EVIDENCE | evidence never stored (no memory line ever cited this photo)
  memory about E06: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* invalid_citation | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence never stored (no memory line ever cited this photo)
  memory about E07: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Fire
* invalid_citation | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence never stored (no memory line ever cited this photo)
  memory about E09: (none)
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
* correct | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: Yes | evidence in memory (stored at step 10)
MEMORY PER STEP (lines / tokens / fallback): 1:1/90; 2:2/180; 3:2/180; 4:3/282; 5:4/389; 6:4/389; 7:4/389; 8:5/462; 9:5/462; 10:5/460/budget_evict_oldest
FINAL MEMORY:
  m3 [src E03] Social media photo from Twitter, timestamp 2017-10-12 03:22 UTC, depicting active wildfire with visible flames and smoke. Two individuals in casual attire standing at a distance, observing the fire. Environment includes charred vegetation and embers. Location details unspecified.
  m4 [src E04] Social media photo from Twitter, timestamp 2017-10-12 08:25 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards the fire. Environment includes charred vegetation and embers. Location details unspecified.
  m5 [src E05] Social media photo from Twitter, timestamp 2017-10-17 16:04 UTC, depicting a fire truck with all emergency lights activated, positioned near a wildfire. The truck's headlights and roof lights are on, illuminating the area. The background shows a mountain partially obscured by smoke, with trees and vegetation visible around the vehicle. Location details unspecified.
  m6 [src E08] Social media photo from Twitter, timestamp 2017-10-19 07:36 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.
  m7 [src E10] Social media photo from Twitter, timestamp 2017-10-20 11:11 UTC, depicting a firefighter in full gear, including helmet with headlamp, directing water towards a wildfire. Environment includes charred vegetation and embers. Location details unspecified.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.6; evidence still in memory for 0.0 of the questions; final memory 3 lines / 263 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=3, invalid_citation=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* wrong_answer_evidence_missing | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: 1 | evidence stored at step 1, deleted at step 6
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* abstained_evidence_missing | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 3, deleted at step 8
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* abstained_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 4, deleted at step 8
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* invalid_citation | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence stored at step 5, deleted at step 8
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* abstained_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 8
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/103; 2:2/248; 3:2/248; 4:3/340; 5:4/432; 6:4/368/budget_evict_oldest; 7:5/460; 8:1/92; 9:2/177; 10:3/263
FINAL MEMORY:
  m8 [src E08] Social media photo posted on 2017-08-28 10:43 UTC shows a fire truck with extended ladder near the burning building. A firefighter in full gear is visible on the truck's roof, observing the fire. The scene is illuminated by emergency lights against a dark sky.
  m9 [src E09] A social media photo posted on 2017-09-06 09:22 UTC shows a fire truck with an extended ladder near the burning building, with a firefighter in full gear on the truck's roof, under emergency lights against a dark sky.
  m10 [src E10] A social media photo posted on 2017-09-08 03:41 UTC shows a fire truck with an extended ladder near the burning building, with a firefighter in full gear on the truck's roof, under emergency lights against a dark sky.
