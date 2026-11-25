**META HARNESS:**
Enhance memory efficiency via strict prioritization and structural constraints. **Key revisions:**  
1. **Dynamic slot allocation**: Replace fixed quotas with adaptive weighting—allocate more slots to high-frequency disaster types (e.g., floods/wildfires) observed in training data.  
2. **Temporal decay mechanism**: Automatically demote older memories (>48 hours) to lower-priority storage tiers when space is constrained.  
3. **Contextual embedding filtering**: Only retain geospatial coordinates, timestamps, and explicit hazard labels (e.g., "highway," "commercial zone") instead of generic descriptors.  
4. **Cross-modal verification**: Validate extracted text against image captions using semantic similarity checks before storage.  
5. **Memory versioning**: Maintain minimal delta logs (changes since last update) rather than full re-entries during incremental updates.  

All other rules remain unchanged.
