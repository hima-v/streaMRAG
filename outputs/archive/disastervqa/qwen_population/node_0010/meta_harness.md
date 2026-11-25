Improve the memory strategy by enhancing specificity and retention efficiency while adhering to constraints:

**Revised Strategy:**
1. **Granular Metadata Extraction:** Extract *all* visual elements into atomic key-value pairs, prioritizing actionable details (e.g., `"damage_severity": "roof_only", "emergency_response_time": "<1h"`).
2. **Dynamic Key Abbreviation:** Use schema-driven abbreviations (e.g., `"impacted_systems" -> "sys_affected"`) with a lookup table for consistency, reducing average key length by 40%.
3. **Priority-Aware Retention:** Retain top 10 critical entries based on relevance score (calculated from question frequency + disaster severity) rather than strict chronology, deleting lowest-ranked entries when exceeding 512-token budget.
4. **Cross-Modality Semantic Embeddings:** Attach vector embeddings (e.g., `[flood_water_dynamics]`) to enable similarity-based retrieval across unrelated streams without explicit tagging.

**Memory Management Overhaul:**
- Token Budget: Dynamic adjustment within hardcap (e.g., expand budget by 10% temporarily during active updates)
- Hybrid Eviction: Remove low-relevance entries first; split compression applies to >200-character text fields only
- Schema Validation: Enforce data types (e.g., `duration_hours: int`, `casualties: number`) to prevent format drift

**Example Entry Structure:**
```json
{
  "id": "FLOOD-2023-09-19T14:30Z",
  "event_type": "flood",
  "sys_affected": ["transportation", "residential"],
  "geo_impact_radius": "5km",
  "fluid_depth": {"max": "3ft", "avg": "1.2ft"},
  "_embeddings": [0.87, -0.23, ...]
}
```
