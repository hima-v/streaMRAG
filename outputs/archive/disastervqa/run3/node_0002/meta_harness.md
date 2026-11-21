"Optimize memory retention for diverse spatial-temporal contexts and critical details (e.g., timestamps, locations, unique identifiers like 'submerged vehicles') by merging temporally proximate duplicates (same location within X minutes/hours) into consolidated summaries. Prioritize unique events over redundant ones; retain only essential metadata (ID, timestamp, coordinates) alongside compressed narratives. Implement stricter semantic similarity thresholds (≥0.8 Jaccard index) to filter redundancies before deletion. Explicitly preserve comparative elements required for cross-time reasoning (e.g., 'changes between dates') by flagging divergent states in merged entries. Enforce token limits rigorously, evicting oldest entries first if budgets exceed capacity."

**Revised Evaluation Criteria:**
1. Token Efficiency: Merge overlapping entries to maintain ≤512 tokens/batch, prioritizing high-value data.
2. Retrieval Accuracy: Verify merged entries resolve queries without missing context (e.g., "How did conditions evolve?").
3. Contextual Preservation: Enable inference across timepoints via explicit comparisons in retained summaries.
