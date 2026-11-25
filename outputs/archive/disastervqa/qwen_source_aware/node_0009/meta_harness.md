Improve the memory strategy by enforcing stricter constraints on redundancy elimination, prioritizing spatially explicit details, and enhancing update logic to resolve conflicts. Modify the evaluation criteria to emphasize precision-recall tradeoffs in downstream tasks.

Memory Strategy Revisions:
1. **Enhanced Uniqueness Filter**: Require >70% lexical similarity before merging duplicates. Example: "submerged cars" ≠ "vehicles underwater" without explicit mapping.
2. **Spatial Indexing**: Encode absolute positions (e.g., "5m left of bridge support") rather than relative terms when geotags exist.
3. **Temporal Chain Tracking**: Maintain event sequences using timestamp overlaps (e.g., link E05→E06 via "same location, +1hr").
4. **Update Rule Overhaul**: Prioritize overwriting earlier entries with higher confidence scores (≥0.8) instead of strict recency.
5. **Domain-Specific Tags**: Retain 3 key attributes per entry (e.g., "flood depth: 2m", "building class: hospital").

Evaluation Adjustments:
- Add F1-score calculation (correct answers / total possible) weighted by token efficiency (answers/tokens ratio).
- Penalize unresolved contradictions within retained memories (-0.1 per inconsistency).
