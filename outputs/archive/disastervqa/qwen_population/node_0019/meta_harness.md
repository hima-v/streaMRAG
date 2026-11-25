{
  "memory_strategy": {
    "priority_tiers": [
      {"metrics": ["structural_damage", "infrastructure_criticality"], "thresholds": [{"type": "percentage", "value": 50}, {"type": "severity_score": 0.8}]},
      {"metrics": ["evacuation_status"], "thresholds": []},
      {"metrics": ["contextual_descriptors"], "thresholds": [{"type": "token_budget_percent", "value": 30}]}
    ],
    "hierarchical_compression": {
      "nested_tag_pattern": "{{[primary_disaster}}}={{[secondary_disaster}}}={{[specific_impact}}}",
      "dynamic_thresholds": {
        "severe_events": {"compression_ratio": 25, "fallback_mode": "exact_values"},
        "moderate_events": {"compression_ratio": 15}
      }
    },
    "adaptive_eviction": {
      "retention_priority": "highest_first",
      "buffer_utilization": {
        "trigger_points": [
          {"threshold": 0.85, "action": "aggressive_compression"},
          {"threshold": 0.92, "action": "partial_entry_preservation"}
        ]
      },
      "temporal_decay": {
        "function": "sqrt_time_weighted",
        "half_life_days": 30,
        "min_retention": 7
      }
    },
    "validation_framework": {
      "hash_reservation": {"capacity": 0.05, "algorithm": "sha256"},
      "incomplete_entry_flag": "[INCOMPLETE]"
    },
    "token_accounting": {
      "baseline_storage_cost": 12,
      "current_limit": 512,
      "real_time_tracking": true
    }
  }
}
