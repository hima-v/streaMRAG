**Meta Harness:**  
"Optimize the memory management system by prioritizing retention of diverse spatial-temporal context and critical details (e.g., timestamps, locations, event-specific features like 'submerged vehicles' or 'collapsed buildings'). When adding new items, compare their uniqueness against existing entries using semantic similarity checks rather than strict duplication. If similar content exists within the same geographic or temporal proximity (e.g., multiple images of the same flood zone taken hours apart), merge key details into a consolidated summary. Retain only essential metadata (date/time, location, unique identifiers) alongside summaries to minimize token usage while preserving retrieval accuracy."  

**Evaluation Criteria:**  
1. **Token Efficiency:** Ensure merged/metadata-only storage keeps total memory under 512 tokens per batch.  
2. **Retrieval Accuracy:** Validate that merged entries enable correct answers when queried post-deletion cycles.  
3. **Contextual Preservation:** Maintain ability to answer questions requiring cross-image inferences (e.g., "What changed between Day 1 and Day 3 floods?").
