"""Silence library noise (bitsandbytes / transformers / timm logging, progress bars, warnings) so
experiment progress lines stay readable. Call `quiet()` before importing model code."""
from __future__ import annotations

import logging
import os
import warnings


def quiet() -> None:
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")   # less fragmentation
    for name in ("bitsandbytes", "transformers", "timm", "accelerate", "huggingface_hub",
                 "sentence_transformers", "torch"):
        logging.getLogger(name).setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    try:
        import transformers
        transformers.utils.logging.set_verbosity_error()
        transformers.utils.logging.disable_progress_bar()
    except ImportError:
        pass
