Domain: each evidence stream is 20 social-media photos of disasters (mostly floods), delivered one at a time in posting order, spread over days to years. The memory agent sees every photo only once and keeps a small token budget of notes.

Questions: after any number of photos, questions may be asked about specific photos, identified by posting time and item id. They are yes/no questions, multiple-choice questions and short open answers about what is visible: people and what they are doing, vehicles and their condition, water level, damage to buildings, roads, bridges or fences, emergency responders, boats, objects people use, animals, weather. Any photo may be asked about, early or late in the stream. Questions about photos that have not arrived yet must be answered NOT_ENOUGH_EVIDENCE, which the answering agent can only do if the memory makes clear which items it covers.

How to write a good memory strategy:
- Record concrete, checkable visual details per photo (counts, states, yes/no facts) rather than general impressions.
- Keep every note tied to its item id; the answering agent finds photos by item id and time.
- Spread the budget over all photos so early photos are not lost when the memory fills up; compress wording before deleting a photo's only note.
- Give an explicit, testable rule for what to do when over budget.

How to read the evaluation log:
- "evidence never stored": the strategy did not make the agent record that kind of detail, or skipped the photo.
- "evidence deleted": the eviction rule removed needed notes; protect or compress instead.
- "evidence in memory but answer wrong": the note was vague, wrong, or missing the specific detail; ask for more specific observations.
- "premature answer": the agent answered about a photo not yet received; notes must make item coverage clear.
Propose specific changes that address the most frequent failure types, and keep what worked.
