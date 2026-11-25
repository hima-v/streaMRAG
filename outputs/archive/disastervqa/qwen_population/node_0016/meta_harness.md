Improve the memory strategy by enhancing specificity and retention efficiency while adhering to constraints:

**Revised Strategy:**
1. **Enhanced Visual Parsing:** Extract *all* visual elements from dataset facts into granular key-value pairs, prioritizing actionable metadata (e.g., `"infrastructure_impacted": ["railway"], "structural_damage_level": "partial"`). Add explicit spatial relationships (e.g., `"proximity_to_water": true`, `"obstruction_location": "road_center"`) when inferrable from descriptions.
2. **Token-Optimized Storage:** Use abbreviated keys (e.g., `disaster_typ`, `materials`), compress repetitive phrases via shorthand (e.g., `"vehicles": ["train_carriage", "auto_rickshaw"]`), and encode recurring entities with unique IDs (e.g., `"building_id": "BLDG-72"` for cross-referencing).
3. **Chronological Replacement Policy:** Retain the latest 10 complete entries strictly. If adding an entry would exceed the 512-token budget, delete the oldest *full* entry first, even mid-update sequence. Never truncate individual entries.
4. **Semantic Linking:** Append context tags (e.g., `[flood_rescue]`, `[wildfire_aftermath]`) and entity references (e.g., `ref:BLDG-72`) to enable cross-event reasoning. Include causal links like `[caused_by_previous_disaster]` where applicable.
5. **Structured Metadata Validation:** Ensure attribute consistency (e.g., `vehicle_types` must align with `damage_type`: no submarines in land floods).

**Memory Capacity Management:**
- Token Budget: Enforce hardcap of 512 tokens. Current average usage (~300 tokens) allows buffer for dynamic updates without evictions unless critical.
- Eviction Protocol: Prioritize deletion of redundant entries (e.g., duplicate descriptions) before chronological ones. Maintain a secondary cache of high-priority tags for rapid retrieval.

**Implementation Example (Updated):**
```json
{
  "source_id": "mX [src E#]",
  "description": "[concise phrase]",
  "attributes": {
    "disaster_typ": "flood",
    "impacted_infra": ["railway"],
    "vehicle_types": ["train_carriage"],
    "spatial_relations": {"near_body_of_water": true},
    "linked_entities": ["BLDG-72"]
  },
  "tags": ["[flood_rescue]", "[structural_damage]"]
}
```

**Memory Strategy Enhancements:**
- Replace generic descriptors with quantified metrics (e.g., `"submerged_percentage": "80%"` vs. `"mostly submerged"`).
- Integrate entity tracking (e.g., `"people_count": 2` → `"persons_visible": 2`) for precise recall.
- Use nested objects for complex relations (e.g., `"impacts": {railway: "partial", bridges: "complete"}`).

**Evaluation Log Metrics:**
Track per-stream performance decay over time to identify leakage points. Penalize incorrect citations more heavily than abstentions to discourage guesswork.
