**Improved Memory Strategy:**
1. **Visual Detail Prioritization:**  
   Retain *unique actionable details* (e.g., "roof-level floodwater," "burning commercial rooftops") rather than generic descriptors. Extract spatial/temporal context (e.g., "cars aligned parallel to riverbank," "smoke density increasing hourly").

2. **Structured Encoding Rules:**  
   - **Event Type Slots:** Max 1 memory/event type/category (vs. previous 2) to reduce redundancy.  
   - **Merge Thresholds:** Combine updates within 24h window using time-delta scoring (e.g., prioritize recent timestamps).  
   - **Attribute Tagging:** Explicitly label key features (e.g., `vehicle_type: sedan`, `infrastructure: railway`) for direct query retrieval.

3. **Pruning Protocol:**  
   - Delete identical verbatim reports regardless of timestamp.  
   - Remove metadata lacking geospatial identifiers (e.g., country/city names absent in captions).

4. **Update Logic:**  
   Overwrite old memories only when new data adds *quantifiable contrast* (e.g., "4 → 6 ladders" > "more ladders").  

5. **Memory Format Enforcement:**  
   Standardize output as `[event_id]: <concise descriptive clause>` without "A social media photo..." prefixes.
