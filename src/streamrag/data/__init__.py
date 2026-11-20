from streamrag.data.disastervqa import DisasterVQA
from streamrag.data.m3bench import M3BenchRobot
from streamrag.data.mindcube import MindCubeTiny
from streamrag.data.videomme import VideoMME

DATASETS = {d.name: d for d in (DisasterVQA, VideoMME, M3BenchRobot, MindCubeTiny)}


def get_dataset(name: str, **overrides):
    if name not in DATASETS:
        raise KeyError(f"Unknown dataset '{name}'. Known: {sorted(DATASETS)}")
    return DATASETS[name](**overrides)


__all__ = ["DATASETS", "get_dataset", "DisasterVQA", "VideoMME", "M3BenchRobot", "MindCubeTiny"]
