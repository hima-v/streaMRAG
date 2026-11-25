Improve the memory strategy:

Memory Strategy:
For each new evidence item, extract **only** visually distinct elements directly observable in the image using precise descriptors (e.g., "floodwater reaching rooftops" instead of "severe flooding"). Store three categories:
1. *Structural context*: Building types (commercial/residential), construction materials (brick/concrete), architectural features
2. *Disaster specifics*: Water levels (submerging vehicles vs. inundated streets), fire intensity (flames engulfing roofs vs. smoldering vegetation), earthquake damage patterns (collapsed walls vs. cracked foundations)
3. *Temporal markers*: Explicit timestamps from posts, visible date indicators in scenes (e.g., calendar pages)

Prune redundancies: Delete duplicates unless later instances show contradictory details (e.g., retain first report of "vehicles submerged" but update if second post clarifies "cars fully submerged"). Enforce strict slot limits: maximum 1 memory per event type (flood/fire/etc.) and 2 spatial relationship memories total. Remove non-visual metadata (platform tags, usernames) unless timestamp resolution exceeds image quality. Prioritize quantitative observations when available ("three cars overturned" > "several damaged vehicles").

During updates, merge similar reports hierarchically: aggregate multiple references to "fallen structures" into summarized counts if spatially co-located. Maintain version history via memory revision counters (v1/v2) rather than full replacement to preserve provenance.

Evaluation Log:
NODE SCORE: 0.38 = mean over 5 streams (↑14% improvement). Memory efficiency maintained (<320 tokens/post-update).
