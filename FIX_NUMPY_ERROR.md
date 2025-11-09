# Fix: NumPy Compatibility Error

## Problem
If you get this error:
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. 
Expected 96 from C header, got 88 from PyObject
```

## Solution

This happens when NumPy 2.x is installed but PyTorch was compiled against NumPy 1.x.

### Quick Fix (Run in a cell)

**Step 1: Install compatible NumPy version**
```python
!pip install --force-reinstall numpy==1.26.4
```

**Step 2: Restart the runtime (REQUIRED!)**
- Colab: `Runtime` → `Restart runtime`
- Kaggle: `Session` → `Restart Session`

**Step 3: Run your cells again**

### Complete Fix (Recommended)

Run this before importing any models:

```python
import subprocess
import sys

# Fix numpy compatibility
print("Fixing numpy compatibility...")
subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '--force-reinstall', 'numpy'], check=False)

# Now import models
from lvae.models import qarv, qresvae, rd
from lvae import get_model
```

### Alternative: Try Different Compatible Versions

If numpy 1.26.4 doesn't work, try these versions:

```python
# Option 1: numpy 1.26.4 (recommended)
!pip install --force-reinstall numpy==1.26.4

# Option 2: numpy 1.24.3
!pip install --force-reinstall numpy==1.24.3

# Option 3: numpy 1.23.5
!pip install --force-reinstall numpy==1.23.5
```

**Always restart runtime after changing numpy version!**

## Why This Happens

- PyTorch and other packages are compiled against a specific numpy version
- When numpy is upgraded/downgraded, binary compatibility breaks
- Colab/Kaggle sometimes have pre-installed packages with mismatched versions

## Prevention

Always reinstall numpy **before** installing other dependencies:

```python
# Step 1: Fix numpy first
!pip install --upgrade --force-reinstall numpy

# Step 2: Then install other packages
!pip install tqdm timm compressai

# Step 3: Then install project
!pip install -e .
```

## Verify Fix

After fixing, verify numpy works:

```python
import numpy as np
import torch
print(f"NumPy: {np.__version__}")
print(f"PyTorch: {torch.__version__}")

# This should work without errors
from lvae.models import qarv, qresvae, rd
```

