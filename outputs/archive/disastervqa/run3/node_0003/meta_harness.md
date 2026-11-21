"Optimize memory management by prioritizing retention of high-value spatial-temporal contexts (e.g., multi-day flood timelines, earthquake collapse sequences) and domain-critical indicators ('submerged vehicles', 'damage progression'). Implement three-tier deduplication: exact text matches (>90% lexical overlap), semantic paraphrases (>85% TF-IDF similarity), and spatio-temporal adjacency (<5km radius/hours gap). Merge candidates retain core metadata (timestamp, geohash) + synthetic composite narrative describing temporal evolution. Cap memory at 512 tokens via hierarchical pruning: first remove low-priority details, then full duplicate entries, finally oldest records. Maintain chain-of-evidence links between original sources for auditability."

**Enhancements:**
1. Added granular similarity thresholds for better redundancy detection
2. Explicit spatio-temporal merging criteria (geohash/radius/gap)
3. Introduced composite narrative generation for time-series synthesis
4. Specified eviction hierarchy (detail > entry > oldest)
5. Emphasized chain-of-evidence tracking for verification
