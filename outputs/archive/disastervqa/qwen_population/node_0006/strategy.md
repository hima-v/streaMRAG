Maintain a token-efficient memory log storing structured JSON entries with:  
1. Optimized keys (e.g., `disaster_typ`, `impacted_infra`), compressed values (e.g., `{"colr":"brwn","dens":"shlw"}`), and source-specific timestamps.  
2. Semantic links via tags (e.g., `[flood_rescue]`), entity IDs (e.g., `@loc:bridge_xyz`), and severity indicators.  
3. Chronological eviction: Retain only latest 10 complete entries; replace oldest full entry if exceeding 512-token budget. No partial deletions.  
4. Contextual grouping using standardized terms (e.g., `vehicle_types=["train_carriage"]` instead of prose).
