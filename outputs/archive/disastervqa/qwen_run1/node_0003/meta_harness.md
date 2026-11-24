Improve the memory strategy.

MEMORY STRATEGY:
Update the memory with the new item, ensuring each entry includes both the original text description and key visual details extracted from the corresponding photograph's dataset facts. Prioritize retaining specific attributes relevant to potential downstream QA tasks.

When updating memory:
1. Store entries in chronological order (oldest first)
2. Include three components per entry:
   a. Source identifier (e.g., "mX [src E#]")
   b. Original text description
   c. Structured key-value pairs of critical visual elements (e.g., {"disaster_type": "flood", "affected_area": "residential"})

If storage capacity is exceeded, delete the oldest complete entry rather than partial content.

EVALUATION LOG:
...[unchanged]...
