# Evaluation streams: archive `run3`

Experiment `short5` · dataset `disastervqa` · 5 streams of 10 photos · 25 questions · memory budget 512 tokens · stream selection `stratified` (seed 0).

Every node of this archive is scored on exactly these streams. In each stream the memory agent sees the photos one at a time (starting from empty memory) and never sees the questions; the questions are asked once, after the last photo, and the node score is the mean of the stream scores.

The *dataset facts* are DisasterVQA's verified annotations of each photo. They are shown here for readers and are used only by the evaluator, never given to the memory or answering agent.

| stream | disaster type | photos | posted | questions |
|---|---|---|---|---|
| [`dvqa-hurricane-len10-010`](#dvqa-hurricane-len10-010) | hurricane | 10 | 2017-09-19 → 2017-09-19 | 5 |
| [`dvqa-flood-len10-024`](#dvqa-flood-len10-024) | flood | 10 | 2015-10-08 → 2015-12-04 | 5 |
| [`dvqa-earthquake-len10-054`](#dvqa-earthquake-len10-054) | earthquake | 10 | 2017-09-21 → 2017-09-21 | 5 |
| [`dvqa-wildfire-len10-064`](#dvqa-wildfire-len10-064) | wildfire | 10 | 2017-10-12 → 2017-10-20 | 5 |
| [`dvqa-fire-len10-066`](#dvqa-fire-len10-066) | fire | 10 | 2017-02-25 → 2017-09-08 | 5 |

## dvqa-hurricane-len10-010

hurricane · 10 photos · 2017-09-19 16:33 UTC → 2017-09-19 20:20 UTC · 5 questions after the last photo

| step | item | posted | photo | dataset facts (evaluator only) |
|---|---|---|---|---|
| 1 | E01 **(asked)** | 2017-09-19 16:33 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910179981166305280_0.jpg" width="160"> | Is flooding visible in the image? Yes<br>Are there any vehicles submerged in water? Yes<br>What type of disaster is depicted in the image? Flood<br>What is the condition of the roads in the image? Completely flooded |
| 2 | E02 | 2017-09-19 16:51 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910184650307280896_0.jpg" width="160"> | Are there any power lines down in the image? Yes<br>Is there emergency vehicle present in the image? Yes<br>Is the road flooded in the image? Yes<br>What is blocking the road in the image? Downed power lines<br>What type of vehicle is present? Police car |
| 3 | E03 **(asked)** | 2017-09-19 17:03 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910187552266743808_0.jpg" width="160"> | Is flooding visible in the image? Yes<br>Are there any vehicles on the flooded road? Yes<br>Can emergency vehicles pass through this area? Yes<br>What type of area is affected? Residential |
| 4 | E04 | 2017-09-19 18:03 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910202655733112833_0.jpg" width="160"> | Is there presence of emergency personnel in the image? Yes<br>What are the people in the image primarily doing? Clearing debris<br>What is the condition of the road in the image? Partially blocked by debris |
| 5 | E05 **(asked)** | 2017-09-19 18:05 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910203290645823488_0.jpg" width="160"> | Are there any visible emergency vehicles in the image? No<br>Is there any visible flooding on the road? No<br>What is the condition of the road? Partially blocked |
| 6 | E06 **(asked)** | 2017-09-19 18:16 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910206000644444160_0.jpg" width="160"> | Is there a fallen tree blocking the road? No<br>Are there any power lines down in the image? Yes<br>What is the primary obstruction on the road? Broken power pole |
| 7 | E07 | 2017-09-19 18:40 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910211896451592193_0.jpg" width="160"> | Is there structural damage to buildings? Yes |
| 8 | E08 **(asked)** | 2017-09-19 19:20 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910222049569673216_0.jpg" width="160"> | Are there any fallen trees visible in the image? Yes<br>Are there any collapsed buildings visible in the image? No |
| 9 | E09 | 2017-09-19 19:51 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910229796805681153_0.jpg" width="160"> | Is there any visible damage to the building structure? No<br>Are there any emergency supplies visible on the cots? Yes<br>What type of facility is shown in the image? Shelter |
| 10 | E10 | 2017-09-19 20:20 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910237112108163072_1.jpg" width="160"> | Is there visible structural damage to buildings? Yes<br>What is the condition of the sky in the image? Cloudy, Smoky<br>How many people are visible in the image? More than 20 |

**Questions** (asked after the last photo):

| item | format | question | options | gold answer |
|---|---|---|---|---|
| E01 | mc | What type of disaster is depicted in the image? Select all that apply. | **A.** Earthquake · **B.** Flood · **C.** Wildfire · **D.** Tornado | B (Flood) |
| E03 | open | What type of area is affected? Answer with one or two words. |  | Residential |
| E05 | mc | What is the condition of the road? Select all that apply. | **A.** Clear · **B.** Partially blocked · **C.** Fully blocked · **D.** Collapsed | B (Partially blocked) |
| E06 | yesno | Is there a fallen tree blocking the road? Answer with Yes or No. |  | No |
| E08 | yesno | Are there any fallen trees visible in the image? Answer with Yes or No. |  | Yes |

## dvqa-flood-len10-024

flood · 10 photos · 2015-10-08 23:05 UTC → 2015-12-04 17:45 UTC · 5 questions after the last photo

| step | item | posted | photo | dataset facts (evaluator only) |
|---|---|---|---|---|
| 1 | E01 | 2015-10-08 23:05 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/652258499125202944_0.jpg" width="160"> | What type of disaster is depicted in the image? Flooding<br>What is the condition of the vehicles in the image? Submerged, Damaged<br>What type of structure is partially submerged in the floodwaters? Trailer |
| 2 | E02 | 2015-12-03 10:41 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/accrafloods_2015-12-03_10-41-52.jpg" width="160"> | Is flooding visible in the image? Yes<br>What type of disaster is depicted in the image? Flooding<br>What is the condition of the road in the image? Flooded |
| 3 | E03 **(asked)** | 2015-12-03 16:52 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672458294959607808_0.jpg" width="160"> | Is flooding visible in the image? Yes<br>Are there any vehicles submerged in water? Yes<br>What is the level of floodwater compared to the height of the submerged vehicle visible in the image? Up to the roof<br>What is the condition of the building in the background? Intact |
| 4 | E04 **(asked)** | 2015-12-03 17:20 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672465551357255680_0.jpg" width="160"> | What is the condition of the road in the image? Flooded<br>What is the primary obstacle on the road? Floodwater |
| 5 | E05 | 2015-12-03 17:45 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672471691629633536_1.jpg" width="160"> | What type of disaster is depicted in the image? Flood<br>What object is the person using for support? Rope |
| 6 | E06 **(asked)** | 2015-12-04 03:38 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672620846309965824_0.jpg" width="160"> | Are there any visible risks such as downed power lines or open manholes? No<br>Is the main road in the image navigable by emergency vehicles? Yes<br>How many vehicles appear to be stranded or damaged in the floodwaters? None |
| 7 | E07 | 2015-12-04 04:24 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672632607318781952_0.jpg" width="160"> | What is the primary activity visible in the image? Evacuation |
| 8 | E08 **(asked)** | 2015-12-04 07:54 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672685451426295813_1.jpg" width="160"> | What infrastructure is affected by the flooding? Railway |
| 9 | E09 | 2015-12-04 08:05 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672688113848832000_3.jpg" width="160"> | How many children are visible? Two |
| 10 | E10 **(asked)** | 2015-12-04 17:45 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/672834059966349312_1.jpg" width="160"> | Are there any vehicles partially submerged in water? Yes<br>What type of vehicle is partially submerged in the water? Auto-rickshaw<br>What is the condition of the road in the image? Flooded |

**Questions** (asked after the last photo):

| item | format | question | options | gold answer |
|---|---|---|---|---|
| E03 | yesno | Are there any vehicles submerged in water? Answer with Yes or No. |  | Yes |
| E04 | open | What is the primary obstacle on the road? Answer with one or two words. |  | Floodwater |
| E06 | yesno | Are there any visible risks such as downed power lines or open manholes? Answer with Yes or No. |  | No |
| E08 | mc | What infrastructure is affected by the flooding? Select all that apply. | **A.** Railway · **B.** Airport · **C.** Highway · **D.** Residential area | A (Railway) |
| E10 | mc | What type of vehicle is partially submerged in the water? Select all that apply. | **A.** Car · **B.** Bus · **C.** Auto-rickshaw · **D.** Truck | C (Auto-rickshaw) |

## dvqa-earthquake-len10-054

earthquake · 10 photos · 2017-09-21 04:40 UTC → 2017-09-21 10:48 UTC · 5 questions after the last photo

| step | item | posted | photo | dataset facts (evaluator only) |
|---|---|---|---|---|
| 1 | E01 | 2017-09-21 04:40 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910725304909389824_0.jpg" width="160"> | What is the condition of the building? Completely Collapsed<br>What is the main material of the debris? Concrete |
| 2 | E02 | 2017-09-21 06:02 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910745969163161600_0.jpg" width="160"> | Is there visible damage to the road surface? Yes<br>Is the vehicle trapped in a sinkhole? No<br>What is the likely cause of the damage depicted in the image? Earthquake<br>What is the condition of the vehicle in the image? Undamaged<br>What is the primary object causing obstruction on the road? Crack |
| 3 | E03 | 2017-09-21 06:18 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910749963423948805_0.jpg" width="160"> | Is heavy machinery needed to remove the debris? Yes<br>What is the likely cause of the damage depicted in the image? Earthquake<br>What is the condition of the building in the image? Completely collapsed |
| 4 | E04 **(asked)** | 2017-09-21 06:50 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910758076579491840_0.jpg" width="160"> | Is the debris blocking the road? No<br>What is the condition of the building in the image? Completely Collapsed<br>What is the primary material of the debris? Bricks |
| 5 | E05 | 2017-09-21 07:14 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910764046516764672_0.jpg" width="160"> | How many people are visibly injured? One |
| 6 | E06 | 2017-09-21 07:16 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910764633811816449_0.jpg" width="160"> | Is the area crowded? Yes<br>What is the primary activity of the people in the image? Rescuing |
| 7 | E07 **(asked)** | 2017-09-21 08:35 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910784474337574912_0.jpg" width="160"> | Are there any vehicles trapped under debris? Yes<br>How many vehicles are visible in the image? One<br>What is the condition of the building in the image? Collapsed |
| 8 | E08 **(asked)** | 2017-09-21 08:44 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910786811164635136_0.jpg" width="160"> | Is there heavy machinery present in the image? Yes<br>Are there any people visible in the image? Yes<br>What is the primary material of the damaged building? Concrete |
| 9 | E09 **(asked)** | 2017-09-21 10:33 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910814140192526336_0.jpg" width="160"> | Is the debris mostly concrete? Yes<br>What is the primary activity of the people in the image? Rescuing<br>How many ladders are visible? Two |
| 10 | E10 **(asked)** | 2017-09-21 10:48 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/910818046683631616_0.jpg" width="160"> | What is the primary material visible in the debris? Concrete<br>How many dogs are visible? One |

**Questions** (asked after the last photo):

| item | format | question | options | gold answer |
|---|---|---|---|---|
| E04 | open | What is the primary material of the debris? Answer with one or two words. |  | Bricks |
| E07 | mc | What is the condition of the building in the image? Select all that apply. | **A.** Intact · **B.** Partially damaged · **C.** Collapsed · **D.** Under construction | C (Collapsed) |
| E08 | yesno | Is there heavy machinery present in the image? Answer with Yes or No. |  | Yes |
| E09 | yesno | Is the debris mostly concrete? Answer with Yes or No. |  | Yes |
| E10 | mc | What is the primary material visible in the debris? Select all that apply. | **A.** Wood · **B.** Metal · **C.** Concrete · **D.** Glass | C (Concrete) |

## dvqa-wildfire-len10-064

wildfire · 10 photos · 2017-10-12 03:11 UTC → 2017-10-20 11:11 UTC · 5 questions after the last photo

| step | item | posted | photo | dataset facts (evaluator only) |
|---|---|---|---|---|
| 1 | E01 **(asked)** | 2017-10-12 03:11 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918313136654049281_0.jpg" width="160"> | Is there any visible water source in the image? No<br>What type of disaster is depicted in the image? Wildfire<br>How many people are visible in the image? Two |
| 2 | E02 | 2017-10-12 03:14 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918313986621362178_0.jpg" width="160"> | Are there any visible flames in the image? Yes<br>What type of disaster is depicted in the image? Wildfire<br>What is the visibility condition in the image? Smoky |
| 3 | E03 | 2017-10-12 03:22 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918315972976631808_0.jpg" width="160"> | What type of disaster is depicted in the image? Wildfire<br>How many people are visible? Four |
| 4 | E04 | 2017-10-12 08:25 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/918392155932065793_0.jpg" width="160"> | Is there any visible water being used to combat the fire? No<br>What type of disaster is depicted in the image? Wildfire |
| 5 | E05 | 2017-10-17 16:04 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920319688348901376_0.jpg" width="160"> | What type of disaster is depicted in the image? Wildfire |
| 6 | E06 **(asked)** | 2017-10-18 07:23 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920550861343948800_0.jpg" width="160"> | What type of disaster is depicted in the image? Wildfire<br>What is the primary material burning? Trees |
| 7 | E07 **(asked)** | 2017-10-18 20:21 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920746714637721600_0.jpg" width="160"> | What type of disaster is depicted in the image? Fire |
| 8 | E08 | 2017-10-19 07:36 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920916661519007745_1.jpg" width="160"> | Is there any visible water being used to combat the fire? Yes<br>What is the primary action being taken in the image? Firefighting<br>What is the condition of the trees in the image? Intact, Burning<br>What is the person holding? Hose |
| 9 | E09 **(asked)** | 2017-10-19 07:36 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/920916661519007745_3.jpg" width="160"> | Are these people watching fireworks? No<br>Are there emergency vehicles present in the image? Yes<br>What type of disaster is depicted in the image? Wildfire |
| 10 | E10 **(asked)** | 2017-10-20 11:11 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/921332920840843265_0.jpg" width="160"> | Is there a fire visible in the image? Yes<br>Are there any emergency responders present? Yes |

**Questions** (asked after the last photo):

| item | format | question | options | gold answer |
|---|---|---|---|---|
| E01 | mc | How many people are visible in the image? Select all that apply. | **A.** None · **B.** One · **C.** Two · **D.** Three | C (Two) |
| E06 | open | What is the primary material burning? Answer with one or two words. |  | Trees |
| E07 | mc | What type of disaster is depicted in the image? Select all that apply. | **A.** Flood · **B.** Fire · **C.** Earthquake · **D.** Tornado | B (Fire) |
| E09 | yesno | Are these people watching fireworks? Answer with Yes or No. |  | No |
| E10 | yesno | Are there any emergency responders present? Answer with Yes or No. |  | Yes |

## dvqa-fire-len10-066

fire · 10 photos · 2017-02-25 03:14 UTC → 2017-09-08 03:41 UTC · 5 questions after the last photo

| step | item | posted | photo | dataset facts (evaluator only) |
|---|---|---|---|---|
| 1 | E01 **(asked)** | 2017-02-25 03:14 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-02-25_03-14-47.jpg" width="160"> | Is there visible smoke coming from the building? Yes<br>Are ladders deployed to access the building? Yes<br>How many emergency ladders are deployed? Four |
| 2 | E02 | 2017-05-13 19:00 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-05-13_19-00-09.jpg" width="160"> | Which objects are visible in the image? Fire truck, Cars, Power lines<br>What is the role of the person visible in the image? Firefighter |
| 3 | E03 **(asked)** | 2017-06-01 13:57 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/suicidebombing_2017-06-01_13-57-59.jpg" width="160"> | Is the road blocked in the image? Yes<br>Are there damaged vehicles in the image? Yes<br>Is debris scattered across the ground? Yes<br>Which object is blocking the road? Burning vehicles, Debris<br>What is the condition of the vehicles in the image? Burning, Damaged |
| 4 | E04 **(asked)** | 2017-06-25 00:20 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-06-25_00-20-19.jpg" width="160"> | Is there any water being sprayed on the fire? Yes<br>What is the object burning in the image? Rooftop<br>What type of building is affected by the fire? Commercial<br>How many fire trucks are visible? Two |
| 5 | E05 **(asked)** | 2017-06-25 21:15 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-06-25_21-15-49.jpg" width="160"> | What is the condition of the buildings in the image? Intact with smoke |
| 6 | E06 **(asked)** | 2017-07-21 00:43 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-07-21_00-43-25.jpg" width="160"> | Is there a damaged vehicle visible in the image? Yes<br>Are there residential buildings near the fire? Yes<br>What is the primary source of danger in the image? Smoke, Fire<br>What type of building is on fire? Residential |
| 7 | E07 | 2017-08-23 00:46 UTC<br>social media photo (web) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/buildingfire_2017-08-23_00-46-05.jpg" width="160"> | Are there any emergency response tools visible in the image? Yes<br>What is the object used to block access to the burning area? Barricade tape |
| 8 | E08 | 2017-08-28 10:43 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/MEDIC/902119421631754244_0.jpg" width="160"> | Is there visible fire in the image? Yes<br>Are there damaged vehicles present? Yes<br>Is there structural damage visible in the background? Yes |
| 9 | E09 | 2017-09-06 09:22 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/905360530591944705_0.jpg" width="160"> | Is there a fire visible in the image? Yes<br>Are there any emergency vehicles present? No<br>What type of facility is affected by the disaster? Industrial<br>What is the main hazard present? Fire |
| 10 | E10 | 2017-09-08 03:41 UTC<br>social media photo (Twitter) | <img src="../../../../data/raw/disastervqa/DisasterVQA-Dataset-v3/DisasterVQA/CrisisMMD/905999617820688384_0.jpg" width="160"> | Is there a large fire visible in the image? Yes<br>Are there any emergency vehicles present? No<br>What is the primary action that needs to be done by emergency responders? Fire extinguishing |

**Questions** (asked after the last photo):

| item | format | question | options | gold answer |
|---|---|---|---|---|
| E01 | open | How many emergency ladders are deployed? Answer with one or two words. |  | Four |
| E03 | yesno | Are there damaged vehicles in the image? Answer with Yes or No. |  | Yes |
| E04 | mc | What type of building is affected by the fire? Select all that apply. | **A.** Residential · **B.** Commercial · **C.** High-rise · **D.** Town house | B (Commercial) |
| E05 | mc | What is the condition of the buildings in the image? Select all that apply. | **A.** Collapsed · **B.** Intact with smoke · **C.** Flooded · **D.** Damaged by wind | B (Intact with smoke) |
| E06 | yesno | Are there residential buildings near the fire? Answer with Yes or No. |  | Yes |
