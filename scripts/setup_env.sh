#!/usr/bin/env bash
# Create the main env. torch 2.7.1+cu126 is chosen so mamba-ssm / causal-conv1d
# install from prebuilt wheels (no local nvcc build needed).
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PYTHON:-python3}
[ -d .venv ] || $PY -m venv .venv
PIP=".venv/bin/pip"
$PIP install -q --upgrade pip wheel setuptools packaging ninja
.venv/bin/python -c "import torch" 2>/dev/null || \
  $PIP install -q torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu126
$PIP install -q -e ".[dev]"
# Nemotron-H (Mamba hybrid) kernels; --no-build-isolation so setup.py sees torch and fetches the matching wheel
$PIP install -q --no-build-isolation causal-conv1d==1.5.2 mamba-ssm==2.2.5
.venv/bin/python - <<'PY'
import torch, transformers, mamba_ssm, causal_conv1d
print("torch", torch.__version__, "cuda", torch.cuda.is_available())
print("transformers", transformers.__version__, "mamba_ssm", mamba_ssm.__version__)
PY
