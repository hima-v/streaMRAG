For each new evidence item, extract only visually distinct elements directly observable in the image using precise descriptors (e.g., "floodwater submerging vehicles" instead of "severe flooding"). Structure memories into four categories:  
1. *Visual Context*: Spatial relationships between objects/buildings, structural states (intact/collapsed/submerged), and environmental conditions (burning/waterlogged).  
2. *Disaster-Specific Attributes*: Quantified damage metrics (number of collapsed structures, depth of submersion), hazard intensities (flame heights, wind speeds), and causal mechanisms (debris scattering patterns).  
3. *Temporal Markers*: Post timestamps converted to relative timelines, explicit date indications in scenes (e.g., license plates showing 2020 models).  
4. *Causal Inferences*: Observable cause-effect links (e.g., broken pipes → flooded basement).  

Enforce strict retention policies:  
- Max 2 memories/event-type (flood/fire/earthquake) and 2 cross-disaster spatial relationships.  
- Delete duplicates unless contradicted; prioritize recent conflicting updates.  
- Retain platform/user metadata only if timestamps resolve ambiguity.  
- Aggregate co-located observations into quantified summaries (e.g., "3 cars overturned" vs. individual reports).  
Maintain versioned histories (m1/m2) to track revisions without data loss. Limit token use via hierarchical merging and selective detail preservation.
