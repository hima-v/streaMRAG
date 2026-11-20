Phase 1: memory update (runs for every new observation)

Input. Video frames go through a vision-language model (Nemotron VL) that writes captions. Text sources such as radio transcripts, robot dialogue and situation reports come in as-is. From here on, everything is text.
① Claim extraction. An LLM splits each caption or sentence into atomic facts: who/what, which property, what value, when, from which source, how confident. “A man walks in, door shut” becomes two claims.
② Retrieval. Find the stored facts about the same thing (same entity and attribute, or semantically similar).
③ Temporal NLI (the core idea). An NLI model compares the new claim against the stored one: entail, contradict, or neutral. A temporal gate then splits contradictions into two cases:
State change: a lot of time passed, and the property can change (hallway empty at 10:00, occupied at 10:05).
Conflict: the reports came at almost the same time, or the new one is hedged (“possibly”). Both versions are kept and flagged.
④ Update. Each label triggers a different action:
Reinforce: add support to the existing fact.
Add: store the new fact.
State change: close the old fact’s time interval and open a new one, keeping the history.
Conflict: keep both reports and link them.
⑤ Memory. Each fact is stored as one short text line with a validity interval, e.g. [10:00–10:05) hallway = empty ×3.
⑥ Consolidation. Only when memory hits the token budget (256/512/1024), evict the least useful facts first: one-off details and weakly supported notes. Protect the current state of each tracked thing, the points where states changed, and unresolved conflicts.

Phase 2: question answering (runs when someone asks)

Parse the question for the entity and the time it asks about.
Pull the facts that were valid at that time and line them up chronologically as an evidence chain.
Nemotron answers while citing fact IDs. It says “conflicting evidence” if sources disagree, and abstains if nothing covers that time.
Phase 3: Hyperagent loop (offline, optional)

The rules above (the τ threshold, prompts, eviction weights) form an editable policy.
A meta agent reads failures on development data and proposes edits. Following the Hyperagents idea, it can also edit its own instructions.
Every variant is scored and archived. The best one is tested once on held-out data.