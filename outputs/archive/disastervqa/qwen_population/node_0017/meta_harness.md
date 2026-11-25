**Revised Meta Harness:**

**Core Memory Constraints:**
1. **Strict Redundancy Elimination:**  
   Merge entries only if ≥70% lexical overlap *and* spatial/temporal alignment exists (e.g., same geolocation ±10m, same time window ±1h). Use Jaccard index on noun phrases (building names, disaster types) for critical matches.  

2. **Spatial Explicitness Mandate:**  
   Prefer verbatim coordinates ("X.Y Z St.") over vague terms ("near downtown") when available. Geotags must map to OpenStreetMap features (road IDs, landmarks) for indexing.  

3. **Hierarchical Temporal Chains:**  
   Link events via `(location, duration)` overlaps. For example, connect E05→E06 if both occur at "downtown intersection" between 15:00–16:00. Discard isolated timestamps lacking spatial anchors.  

4. **Confidence-Driven Updates:**  
   Replace prior memories only if new claim has ≥80% confidence AND contradicts existing data (e.g., conflicting disaster timelines). Log updates with confidence scores (e.g., `Updated E03@14:00 → Confidence: 0.85`).  

5. **Structured Attribute Preservation:**  
   Retain top-3 entity-value pairs per event (e.g., `"building_class: hospital"`, `"damage_level: partial"`). Enforce atomicity: split compound sentences into triples (subject-predicate-object).  

---

**Token Efficiency Optimization:**  
- Cap descriptive clauses at 12 words/event. Prune adjectives violating >50% repetition rate.  
- Cache repeated structures (e.g., "social media post dated [timestamp]") as reusable templates.  

---

**Dynamic Evaluation Protocol:**  
```python
def calculate_score(correct_count, abstained_count, contradiction_penalty):
    recall = correct_count / len(questions) if questions else 0
    precision = correct_count / (correct_count + abs(wrong_answers)) if (correct_count + abs(wrong_answers)) > 0 else 0
    
    # Precision-recall harmonic mean
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'f1': round(f1, 2),
        'penalty_adjustment': max(-contradiction_penalty * len(contradictions), 0),
        'efficiency_ratio': sum(answer_lengths)/sum(token_counts)
    }
```

---

**Critical Failures Mitigation:**  
- Add **geofence-based filtering**: Discard memories outside predefined regions (e.g., hurricane zones vs. earthquake faults).  
- Implement **conflict resolution hierarchy**: Spatial > temporal > confidence > recency.  
- Introduce **temporal decay**: Halve memory relevance every 6 hours absent reinforcement.  
```
