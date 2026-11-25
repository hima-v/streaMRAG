**Improved Memory Strategy:**
1. **Visual Detail Extraction:** Capture granular, scene-specific features (e.g., "roof submerged up to third floor," "tree branches snapping under tension") rather than abstract categories. Store spatial hierarchies (e.g., "debris pile atop car," "power line crossing above road") and quantify where possible (e.g., "3 cars fully submerged").
2. **Temporal & Contextual Encoding:** Log timestamp differences to infer event sequencing (e.g., "smoke thickens post-18:00 UTC"). Correlate geotags/platform IDs when merging duplicates (e.g., same location but different angles/time stamps).
3. **Hard Deletion Rules:** Remove repetitive descriptors (e.g., deleting "burning structure" after noting "charred timber beams and melted metal fixtures"). Retain contradictions requiring reconciliation (e.g., conflicting casualty reports).
4. **Quantitative Aggregation:** Summarize recurring themes numerically (e.g., "4+ structures compromised" instead of listing individual incidents separately). Track progression (e.g., "damage escalates hourly: Phase I—structural cracks → Phase II—partial collapse").
5. **Token Optimization:** Use tiered prioritization: top-tier slots reserved for actionable data (coordinates, counts, hazards); lower tiers for contextual details. Apply compression algorithms (e.g., hexadecimal truncation of URLs).

**Structured Schema Example:**
```json
{
  "ID": "E01",
  "timestamp": "2017-09-19 16:33 UTC",
  "location": "[geohash]",
  "scene_elements": {
    "primary_hazard": "Flood",
    "quantitative_data": {"submerged_vehicles": 12},
    "spatial_details": [
      {"object": "car", "position": "behind gas station"},
      {"object": "building", "state": "partially collapsed"}
    ]
  },
  "metadata": ["Twitter", "verified account"]
}
```

**Update Protocol:**
- On receiving new evidence: Compare against existing entries using Jaccard index (>0.7 similarity triggers full comparison).
- If conflict detected: Flag both versions with version control headers (`[V1]`/`[V2]`) for human review later.
- Prune lowest-priority details first (e.g., emojis, hashtags) until below token limit.

**Memory Management Thresholds:**
| Token Budget | Action |
|--------------|--------|
| >75%         | Add new entry without deletion |
| ≤75%-50%     | Replace oldest entry <10% relevance score |
| <50%         | Aggressive chunk removal (-30%) |

**Final Constraints:** Max 10 entries, 512 tokens total. Entries must include at least one measurable attribute (coordinate, count, dimension).
