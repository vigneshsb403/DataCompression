# Fix: KeyError when loading models

## Problem
If you get this error:
```
KeyError: 'qarv_base'
```

## Solution
You need to import the model modules **before** calling `get_model()`. The models are registered when their modules are imported.

### Quick Fix
Add this line **before** loading any model:

```python
# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model

# Now you can use get_model()
model = get_model('qarv_base', pretrained=True)
```

### Complete Example
```python
import torch

# Step 1: Import model modules (this registers them)
from lvae.models import qarv, qresvae, rd

# Step 2: Import get_model function
from lvae import get_model

# Step 3: Now you can load models
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = get_model('qarv_base', pretrained=True)
model = model.to(device)
model.eval()
model.compress_mode(True)
```

## Why This Happens
The project uses a decorator-based registration system. Models are registered when their `zoo.py` modules are imported. If you only import `get_model` without importing the model modules, the registry will be empty.

## Available Models
After importing, you can use:
- `qarv_base` - Variable rate compression (recommended)
- `qres34m` - Fixed rate compression
- `qres34m_lossless` - Lossless compression
- `qres17m` - Smaller model

Example:
```python
from lvae.models import qarv, qresvae, rd
from lvae import get_model

# Variable rate model
model1 = get_model('qarv_base', pretrained=True)

# Fixed rate model (need to specify lambda)
model2 = get_model('qres34m', lmb=256, pretrained=True)

# Lossless model
model3 = get_model('qres34m_lossless', pretrained=True)
```

