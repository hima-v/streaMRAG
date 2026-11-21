NODE SCORE: 0.12 = mean over 5 evidence stream(s): dvqa-hurricane-len10-010 0.0, dvqa-flood-len10-024 0.0, dvqa-earthquake-len10-054 0.4, dvqa-wildfire-len10-064 0.2, dvqa-fire-len10-066 0.0
STREAM dvqa-hurricane-len10-010: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 1.0; evidence still in memory for 0.8 of the questions; final memory 8 lines / 457 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=1, unnecessary_abstention=4

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E01 (posted 2017-09-19 16:33 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Flood) | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 1, deleted at step 6
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What type of disaster is depicted in the image? Flood; What is the condition of the roads in the image? Completely flooded
* unnecessary_abstention | E03 (posted 2017-09-19 17:03 UTC): What type of area is affected? Answer with one or two words.
  gold: Residential | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 3)
  memory about E03: Social media photo (Twitter) posted 2017-09-19 17:03 UTC corroborates the scene.
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles on the flooded road? Yes; Can emergency vehicles pass through this area? Yes; What type of area is affected? Residential
* unnecessary_abstention | E05 (posted 2017-09-19 18:05 UTC): What is the condition of the road? Select all that apply.
  gold: B (Partially blocked) | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 5)
  memory about E05: Social media photo (Twitter) posted 2017-09-19 18:05 UTC corroborates the scene.
  what the photo actually shows (dataset facts): Are there any visible emergency vehicles in the image? No; Is there any visible flooding on the road? No; What is the condition of the road? Partially blocked
* unnecessary_abstention | E06 (posted 2017-09-19 18:16 UTC): Is there a fallen tree blocking the road? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: Social media photo (Twitter) posted 2017-09-19 18:16 UTC corroborates the scene.
  what the photo actually shows (dataset facts): Is there a fallen tree blocking the road? No; Are there any power lines down in the image? Yes; What is the primary obstruction on the road? Broken power pole
* unnecessary_abstention | E08 (posted 2017-09-19 19:20 UTC): Are there any fallen trees visible in the image? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 8)
  memory about E08: Social media photo (Twitter) posted 2017-09-19 19:20 UTC corroborates the scene.
  what the photo actually shows (dataset facts): Are there any fallen trees visible in the image? Yes; Are there any collapsed buildings visible in the image? No
MEMORY PER STEP (lines / tokens / fallback): 1:1/64; 2:2/183; 3:2/225; 4:3/334; 5:4/443; 6:4/228/budget_evict_oldest; 7:5/285; 8:6/342; 9:7/399; 10:8/457
FINAL MEMORY:
  m3 [src E03] Social media photo (Twitter) posted 2017-09-19 17:03 UTC corroborates the scene.
  m4 [src E04] Social media photo (Twitter) posted 2017-09-19 18:03 UTC corroborates the scene.
  m5 [src E05] Social media photo (Twitter) posted 2017-09-19 18:05 UTC corroborates the scene.
  m6 [src E06] Social media photo (Twitter) posted 2017-09-19 18:16 UTC corroborates the scene.
  m7 [src E07] Social media photo (Twitter) posted 2017-09-19 18:40 UTC corroborates the scene.
  m8 [src E08] Social media photo (Twitter) posted 2017-09-19 19:20 UTC corroborates the scene.
  m9 [src E09] Social media photo (Twitter) posted 2017-09-19 19:51 UTC corroborates the scene.
  m10 [src E10] Social media photo (Twitter) posted 2017-09-19 20:20 UTC corroborates the scene.

STREAM dvqa-flood-len10-024: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.4 of the questions; final memory 2 lines / 237 tokens; budget fallbacks 1).
OUTCOMES: invalid_citation=2, unnecessary_abstention=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* invalid_citation | E03 (posted 2015-12-03 16:52 UTC): Are there any vehicles submerged in water? Answer with Yes or No.
  gold: Yes | given: Yes | evidence stored at step 3, deleted at step 6
  memory about E03: (none)
  what the photo actually shows (dataset facts): Is flooding visible in the image? Yes; Are there any vehicles submerged in water? Yes; What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof; What is the condition of the building in the background? Intact
* invalid_citation | E04 (posted 2015-12-03 17:20 UTC): What is the primary obstacle on the road? Answer with one or two words.
  gold: Floodwater | given: Flooded | evidence stored at step 4, deleted at step 6
  memory about E04: (none)
  what the photo actually shows (dataset facts): What is the condition of the road in the image? Flooded; What is the primary obstacle on the road? Floodwater
* unnecessary_abstention | E06 (posted 2015-12-04 03:38 UTC): Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No.
  gold: No | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 6)
  memory about E06: Social media photo posted on 2015-12-04 03:38 UTC showing a flooded area with submerged vehicles and debris, including a white RV tilted and partially submerged, a white trailer with a blue tarp covering debris, and a white RV with a gray roof tilted and partially submerged. Surrounding area has dense green trees and bushes. Photo taken from a bridge with a metal railing visible in the foreground.
  what the photo actually shows (dataset facts): Are there any visible risks such as downed power lines or open manholes? No; Is the main road in the image navigable by emergency vehicles? Yes; How many vehicles appear to be stranded or damaged in the floodwaters? None
* wrong_answer_evidence_missing | E08 (posted 2015-12-04 07:54 UTC): What infrastructure is affected by the flooding? Select all that apply.
  gold: A (Railway) | given: C (Highway) | evidence stored at step 8, deleted at step 10
  memory about E08: (none)
  what the photo actually shows (dataset facts): What infrastructure is affected by the flooding? Railway
* wrong_answer_evidence_in_memory | E10 (posted 2015-12-04 17:45 UTC): What type of vehicle is partially submerged in the water? Select all that apply.
  gold: C (Auto-rickshaw) | given: A (Car) | evidence in memory (stored at step 10)
  memory about E10: Social media photo posted on 2015-12-04 17:45 UTC showing a flooded area with submerged vehicles and debris, including a white RV tilted and partially submerged, a white trailer with a blue tarp covering debris, and a white RV with a gray roof tilted and partially submerged. Surrounding area has dense green trees and bushes. Photo taken from a bridge with a metal railing visible in the foreground.
  what the photo actually shows (dataset facts): Are there any vehicles partially submerged in water? Yes; What type of vehicle is partially submerged in the water? Auto-rickshaw; What is the condition of the road in the image? Flooded
MEMORY PER STEP (lines / tokens / fallback): 1:1/94; 2:2/257; 3:2/257; 4:3/375; 5:4/493; 6:2/258; 7:3/376; 8:4/494; 9:4/472/budget_evict_oldest; 10:2/237
FINAL MEMORY:
  m6 [src E06] Social media photo posted on 2015-12-04 03:38 UTC showing a flooded area with submerged vehicles and debris, including a white RV tilted and partially submerged, a white trailer with a blue tarp covering debris, and a white RV with a gray roof tilted and partially submerged. Surrounding area has dense green trees and bushes. Photo taken from a bridge with a metal railing visible in the foreground.
  m10 [src E10] Social media photo posted on 2015-12-04 17:45 UTC showing a flooded area with submerged vehicles and debris, including a white RV tilted and partially submerged, a white trailer with a blue tarp covering debris, and a white RV with a gray roof tilted and partially submerged. Surrounding area has dense green trees and bushes. Photo taken from a bridge with a metal railing visible in the foreground.

STREAM dvqa-earthquake-len10-054: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.4 (2/5 questions correct with valid evidence; abstained on 0.2; evidence still in memory for 0.6 of the questions; final memory 4 lines / 455 tokens; budget fallbacks 2).
OUTCOMES: correct=2, unnecessary_abstention=1, wrong_answer_evidence_missing=2

PER QUESTION (asked after the last photo):
* unnecessary_abstention | E04 (posted 2017-09-21 06:50 UTC): What is the primary material of the debris? Answer with one or two words.
  gold: Bricks | given: NOT_ENOUGH_EVIDENCE | evidence in memory (stored at step 4)
  memory about E04: Social media photo from Twitter posted on 2017-09-21 06:50 UTC showing a woman riding a yellow bicycle with a cargo attachment. She wears a white shirt, purple shorts with white stripes, and flip-flops. The bicycle has a green container attached to its front. The background features a collapsed building with exposed rebar, broken concrete, and wooden ladders. Power lines and a partially collapsed wall are visible. The environment is daylight with clear visibility.
  what the photo actually shows (dataset facts): Is the debris blocking the road? No; What is the condition of the building in the image? Completely Collapsed; What is the primary material of the debris? Bricks
* correct | E07 (posted 2017-09-21 08:35 UTC): What is the condition of the building in the image? Select all that apply.
  gold: C (Collapsed) | given: C (Collapsed) | evidence in memory (stored at step 7)
* wrong_answer_evidence_missing | E08 (posted 2017-09-21 08:44 UTC): Is there heavy machinery present in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 8, deleted at step 9
  memory about E08: (none)
  what the photo actually shows (dataset facts): Is there heavy machinery present in the image? Yes; Are there any people visible in the image? Yes; What is the primary material of the damaged building? Concrete
* wrong_answer_evidence_missing | E09 (posted 2017-09-21 10:33 UTC): Is the debris mostly concrete? Answer with Yes or No.
  gold: Yes | given: No | evidence stored at step 9, deleted at step 10
  memory about E09: (none)
  what the photo actually shows (dataset facts): Is the debris mostly concrete? Yes; What is the primary activity of the people in the image? Rescuing; How many ladders are visible? Two
* correct | E10 (posted 2017-09-21 10:48 UTC): What is the primary material visible in the debris? Select all that apply.
  gold: C (Concrete) | given: C (Concrete) | evidence in memory (stored at step 10)
MEMORY PER STEP (lines / tokens / fallback): 1:1/126; 2:2/296; 3:2/235; 4:3/365; 5:4/481; 6:4/464/budget_evict_oldest; 7:4/459/budget_evict_oldest; 8:4/454; 9:4/454; 10:4/455
FINAL MEMORY:
  m4 [src E04] Social media photo from Twitter posted on 2017-09-21 06:50 UTC showing a woman riding a yellow bicycle with a cargo attachment. She wears a white shirt, purple shorts with white stripes, and flip-flops. The bicycle has a green container attached to its front. The background features a collapsed building with exposed rebar, broken concrete, and wooden ladders. Power lines and a partially collapsed wall are visible. The environment is daylight with clear visibility.
  m5 [src E05] Social media photo from Twitter posted on 2017-09-21 07:14 UTC showing a group of individuals in safety gear (white hard hats, orange vests) assisting a person lying on a stretcher amidst rubble. Exposed rebar, broken concrete, and wooden ladders are visible. Power lines and a partially collapsed wall frame the scene. The environment is daylight with clear visibility.
  m7 [src E07] Social media photo from Twitter posted on 2017-09-21 08:35 UTC showing a collapsed building with exposed rebar, broken concrete, and wooden ladders. Power lines and a partially collapsed wall frame the scene. A silver car with open doors and debris inside is visible amidst rubble. The environment is daylight with clear visibility.
  m10 [src E10] Social media photo from Twitter posted on 2017-09-21 10:48 UTC showing a collapsed building with exposed rebar, broken concrete, and wooden ladders. Power lines and a partially collapsed wall frame the scene. A silver car with open doors and debris inside is visible amidst rubble. The environment is daylight with clear visibility.

STREAM dvqa-wildfire-len10-064: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.2 (1/5 questions correct with valid evidence; abstained on 0.0; evidence still in memory for 0.4 of the questions; final memory 2 lines / 245 tokens; budget fallbacks 0).
OUTCOMES: correct=1, invalid_citation=3, wrong_answer_evidence_in_memory=1

PER QUESTION (asked after the last photo):
* correct | E01 (posted 2017-10-12 03:11 UTC): How many people are visible in the image? Select all that apply.
  gold: C (Two) | given: C (Two) | evidence in memory (stored at step 1)
* invalid_citation | E06 (posted 2017-10-18 07:23 UTC): What is the primary material burning? Answer with one or two words.
  gold: Trees | given: brush and debris | evidence stored at step 6, deleted at step 8
  memory about E06: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Wildfire; What is the primary material burning? Trees
* invalid_citation | E07 (posted 2017-10-18 20:21 UTC): What type of disaster is depicted in the image? Select all that apply.
  gold: B (Fire) | given: B (Fire) | evidence stored at step 7, deleted at step 8
  memory about E07: (none)
  what the photo actually shows (dataset facts): What type of disaster is depicted in the image? Fire
* invalid_citation | E09 (posted 2017-10-19 07:36 UTC): Are these people watching fireworks? Answer with Yes or No.
  gold: No | given: No | evidence stored at step 9, deleted at step 10
  memory about E09: (none)
  what the photo actually shows (dataset facts): Are these people watching fireworks? No; Are there emergency vehicles present in the image? Yes; What type of disaster is depicted in the image? Wildfire
* wrong_answer_evidence_in_memory | E10 (posted 2017-10-20 11:11 UTC): Are there any emergency responders present? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 10)
  memory about E10: Social media photo from Twitter posted on 2017-10-20 11:11 UTC showing a wildfire scene with multiple fires on the ground, two individuals observing from a distance, and a hazy sky. The fire is consuming brush and debris, with visible flames and smoke. The individuals are standing on higher ground, facing the fire. The environment appears to be a natural, outdoor setting with trees and shrubs in the background.
  what the photo actually shows (dataset facts): Is there a fire visible in the image? Yes; Are there any emergency responders present? Yes
MEMORY PER STEP (lines / tokens / fallback): 1:1/122; 2:2/244; 3:2/244; 4:3/366; 5:4/488; 6:2/244; 7:3/366; 8:2/244; 9:3/366; 10:2/245
FINAL MEMORY:
  m1 [src E01] Social media photo from Twitter posted on 2017-10-12 03:11 UTC showing a wildfire scene with multiple fires on the ground, two individuals observing from a distance, and a hazy sky. The fire is consuming brush and debris, with visible flames and smoke. The individuals are standing on higher ground, facing the fire. The environment appears to be a natural, outdoor setting with trees and shrubs in the background.
  m10 [src E10] Social media photo from Twitter posted on 2017-10-20 11:11 UTC showing a wildfire scene with multiple fires on the ground, two individuals observing from a distance, and a hazy sky. The fire is consuming brush and debris, with visible flames and smoke. The individuals are standing on higher ground, facing the fire. The environment appears to be a natural, outdoor setting with trees and shrubs in the background.

STREAM dvqa-fire-len10-066: 10 photos (E01-E10), memory budget 512 tokens. The memory agent never sees the questions; 5 questions were asked once, after the last photo.
SCORE: 0.0 (0/5 questions correct with valid evidence; abstained on 0.4; evidence still in memory for 0.2 of the questions; final memory 2 lines / 237 tokens; budget fallbacks 1).
OUTCOMES: abstained_evidence_missing=2, invalid_citation=1, wrong_answer_evidence_in_memory=1, wrong_answer_evidence_missing=1

PER QUESTION (asked after the last photo):
* abstained_evidence_missing | E01 (posted 2017-02-25 03:14 UTC): How many emergency ladders are deployed? Answer with one or two words.
  gold: Four | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 1, deleted at step 6
  memory about E01: (none)
  what the photo actually shows (dataset facts): Is there visible smoke coming from the building? Yes; Are ladders deployed to access the building? Yes; How many emergency ladders are deployed? Four
* wrong_answer_evidence_in_memory | E03 (posted 2017-06-01 13:57 UTC): Are there damaged vehicles in the image? Answer with Yes or No.
  gold: Yes | given: No | evidence in memory (stored at step 3)
  memory about E03: A social media photo posted on 2017-06-01 13:57 UTC shows a firefighter standing on a fire truck, observing a large fire engulfing a multi-story building. The scene is illuminated by emergency lights, with smoke and flames visible against a darkening sky. The building appears to be a brick apartment complex with multiple windows and fire escapes. An American flag is visible on the fire truck.
  what the photo actually shows (dataset facts): Is the road blocked in the image? Yes; Are there damaged vehicles in the image? Yes; Is debris scattered across the ground? Yes; Which object is blocking the road? Burning vehicles, Debris; What is the condition of the vehicles in the image? Burning, Damaged
* wrong_answer_evidence_missing | E04 (posted 2017-06-25 00:20 UTC): What type of building is affected by the fire? Select all that apply.
  gold: B (Commercial) | given: A (Residential) | evidence stored at step 4, deleted at step 7
  memory about E04: (none)
  what the photo actually shows (dataset facts): Is there any water being sprayed on the fire? Yes; What is the object burning in the image? Rooftop; What type of building is affected by the fire? Commercial; How many fire trucks are visible? Two
* invalid_citation | E05 (posted 2017-06-25 21:15 UTC): What is the condition of the buildings in the image? Select all that apply.
  gold: B (Intact with smoke) | given: B (Intact with smoke) | evidence stored at step 5, deleted at step 7
  memory about E05: (none)
  what the photo actually shows (dataset facts): What is the condition of the buildings in the image? Intact with smoke
* abstained_evidence_missing | E06 (posted 2017-07-21 00:43 UTC): Are there residential buildings near the fire? Answer with Yes or No.
  gold: Yes | given: NOT_ENOUGH_EVIDENCE | evidence stored at step 6, deleted at step 7
  memory about E06: (none)
  what the photo actually shows (dataset facts): Is there a damaged vehicle visible in the image? Yes; Are there residential buildings near the fire? Yes; What is the primary source of danger in the image? Smoke, Fire; What type of building is on fire? Residential
MEMORY PER STEP (lines / tokens / fallback): 1:1/98; 2:2/211; 3:2/211; 4:3/329; 5:4/447; 6:4/472/budget_evict_oldest; 7:2/236; 8:3/354; 9:2/236; 10:2/237
FINAL MEMORY:
  m3 [src E03] A social media photo posted on 2017-06-01 13:57 UTC shows a firefighter standing on a fire truck, observing a large fire engulfing a multi-story building. The scene is illuminated by emergency lights, with smoke and flames visible against a darkening sky. The building appears to be a brick apartment complex with multiple windows and fire escapes. An American flag is visible on the fire truck.
  m10 [src E10] A social media photo posted on 2017-09-08 03:41 UTC shows a firefighter standing on a fire truck, observing a large fire engulfing a multi-story building. The scene is illuminated by emergency lights, with smoke and flames visible against a darkening sky. The building appears to be a brick apartment complex with multiple windows and fire escapes. An American flag is visible on the fire truck.
