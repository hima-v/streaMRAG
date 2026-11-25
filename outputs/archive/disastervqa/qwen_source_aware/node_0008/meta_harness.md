**Enhanced Memory Strategy:**
1. **Hierarchical Visual Encoding:** Store three tiers of detail - macro context ("urban area"), mid-level features ("submerged vehicles", "roof-height water"), micro cues ("roof color patterns", "emergency light reflections")
2. **Temporal Contextualization:** Link timestamps to phase indicators ("Day 3: Initial rescue operations", "Post-rescue assessment phase")
3. **Structured Abstraction Rules:**
   - Merge identical events within ±2hr time windows
   - Maintain distinct entries when new contradictions emerge
   - Archive unverified claims after 3 update cycles without validation
4. **Contextual Filtering Protocol:**
   ```python
   def relevance_filter(memory_entry, question_type):
       weight = {
           'spatial': 0.3,
           'temporal': 0.2,
           'object': 0.4,
           'state': 0.1
       }
       score = sum(weight[k] * k in entry.tags for k in weight)
       return score > 0.6
   ```
5. **Dynamic Slot Management:**
   ```python
   class EventTracker:
       MAX_MEMORY = 512
       
       def __init__(self):
           self.slot_budgets = {'disaster_type': 2, ...}
           
       def process_update(self, new_data):
           if len(self.memory) >= self.MAX_MEMORY:
               oldest_entries = sorted(self.memory, key=lambda x: x.timestamp)[0]
               # Smart eviction using LRU + importance scoring
               candidate = min(oldest_entries, key=lambda x: x.importance_score)
               self.memory.remove(candidate)
   ```
