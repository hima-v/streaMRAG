Retain distinct visual details critical for answering downstream questions while aggressively pruning redundancy. Extract specific, observable elements (e.g., "submerged vehicles" instead of "flooded area") and encode spatial relationships ("building X behind car Y"), temporal sequences (time-stamped posts), and domain-specific attributes ("commercial" vs. "residential" buildings). Store quantitative data (counts, measurements) and maintain strict token limits (~8 entries within 512 tokens) via hierarchical summarization.  
**Rules**:  
1. **Hard Deletion**: Remove duplicates unless updated with conflicting info.  
2. **Timestamp-Based Retention**: Keep only the 3 most recent relevant observations per category (e.g., hazard severity, locations).  
3. **Validation Checks**: Reject additions violating spatial/temporal logic (e.g., "sunny day" contradicting storm reports).  
4. **Overwriting**: Update entries explicitly using timestamps/positional cues.  
5. **Discard Low-Value Metadata**: Ignore non-essential details (e.g., platform tags) unless resolving ambiguities.  
Memory is capped at 512 tokens, with periodic merges of related observations (e.g., aggregating "fallen trees" counts). Updates overwrite prior entries to ensure accuracy.
