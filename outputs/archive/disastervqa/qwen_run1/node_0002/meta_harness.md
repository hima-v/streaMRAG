Improve the memory strategy to enhance accuracy while managing token usage effectively. Key modifications include:

1. **Prioritize Distinctive Information**: Store only unique details per event (e.g., "flooded area" repeated redundantly in multiple entries can be consolidated into a single summary).

2. **Structured Memory Encoding**: Use bullet-point summaries with clear labels (e.g., `EVT_E01: Flooded area; Submerged vehicles; Buildings intact`) to reduce verbosity and improve retrieval efficiency.

3. **Automated Evidence Validation**: Before answering, cross-check retrieved memories against dataset facts to detect contradictions (e.g., if memory claims "no vehicles," but data confirms "yes," flag the inconsistency).

4. **Token-Aware Retention Policy**: Evict redundant or low-value memories when nearing the 512-token limit (e.g., prioritize keeping distinctive events like disasters over repetitive descriptions).

5. **Question-Specific Context Injection**: When answering, append relevant question metadata (e.g., "Focus on structural damage") to guide memory search toward pertinent information.

This approach reduces redundancy, ensures critical details persist, and minimizes errors caused by outdated/invalid citations.
