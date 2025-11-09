# Running Lossy-VAE on Google Colab or Kaggle

This guide will help you run the Lossy-VAE project on Google Colab or Kaggle.

## Prerequisites

- Google Colab account (free) OR Kaggle account (free)
- Basic knowledge of Python

## Option 1: Google Colab

### Step 1: Open Google Colab
1. Go to https://colab.research.google.com/
2. Create a new notebook

### Step 2: Enable GPU
1. Click `Runtime` → `Change runtime type`
2. Set `Hardware accelerator` to `GPU` (T4)
3. Click `Save`

### Step 3: Upload Project Files
You have two options:

**Option A: Upload via Colab UI**
1. Click the folder icon on the left sidebar
2. Click `Upload` and upload your `DataCompression` folder
3. Or use the upload button in the file browser

**Option B: Clone from Git (if available)**
```python
!git clone <your-repo-url>
```

### Step 4: Run Setup
In a new cell, run:
```python
%cd /content/DataCompression/lossy-vae
exec(open('setup_colab_kaggle.py').read())
```

Or manually:
```python
import sys
from pathlib import Path

# Install dependencies
!pip install -q tqdm timm compressai

# Install project
%cd /content/DataCompression/lossy-vae
!pip install -e .

# Set up paths
import os
os.chdir('/content/DataCompression/lossy-vae')
```

### Step 5: Use the Project
See the `demo_colab_kaggle.ipynb` notebook for examples.

---

## Option 2: Kaggle

### Step 1: Create a New Notebook
1. Go to https://www.kaggle.com/
2. Click `Code` → `New Notebook`
3. Select `GPU` as accelerator

### Step 2: Upload Project Files
1. Click `+ Add data` → `Upload`
2. Upload your `DataCompression` folder as a dataset
3. Or use Kaggle Datasets if you've uploaded it there

### Step 3: Run Setup
In the first cell:
```python
import sys
from pathlib import Path

# Install dependencies
!pip install -q tqdm timm compressai

# Copy project to working directory
import shutil
shutil.copytree('/kaggle/input/your-dataset-name/DataCompression', 
                '/kaggle/working/DataCompression', dirs_exist_ok=True)

# Install project
%cd /kaggle/working/DataCompression/lossy-vae
!pip install -e .

# Set up paths
import os
os.chdir('/kaggle/working/DataCompression/lossy-vae')
```

### Step 4: Use the Project
See the `demo_colab_kaggle.ipynb` notebook for examples.

---

## Quick Start Examples

### Example 1: Load a Pre-trained Model
```python
# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = get_model('qarv_base', pretrained=True)
model = model.to(device)
model.eval()
model.compress_mode(True)
print("Model loaded successfully!")
```

### Example 2: Compress an Image
```python
from PIL import Image
import torchvision.transforms.functional as tvf

# Load an image
img_path = '/path/to/your/image.png'
output_path = '/path/to/compressed.bits'

model.compress_file(img_path, output_path)
print(f"Image compressed to {output_path}")
```

### Example 3: Decompress an Image
```python
# Decompress
reconstructed = model.decompress_file(output_path)

# Convert to PIL Image and display
from torchvision.utils import save_image
save_image(reconstructed, 'reconstructed.png')
print("Image decompressed!")
```

### Example 4: Download Test Dataset
```python
from scripts.download_dataset import main as download_dataset
import sys

# Download Kodak dataset (small, good for testing)
sys.argv = ['download-dataset.py', '--name', 'kodak', '--datasets_root', '/content/datasets']
download_dataset()
```

### Example 5: Evaluate Model
```python
from eval_var_rate import main as eval_main
import sys

sys.argv = ['eval-var-rate.py', 
            '--model', 'qarv_base',
            '--dataset_name', 'kodak',
            '--device', 'cuda:0',
            '--steps', '8']
eval_main()
```

---

## Important Notes

1. **GPU Memory**: Both Colab and Kaggle provide limited GPU memory. Use smaller batch sizes if you encounter OOM errors.

2. **Session Limits**: 
   - Colab: Sessions timeout after ~12 hours of inactivity
   - Kaggle: GPU sessions limited to 30 hours/week

3. **Storage**:
   - Colab: ~80GB temporary storage
   - Kaggle: ~20GB working directory

4. **Datasets**: For large datasets like COCO, consider using Kaggle Datasets feature or Google Drive (for Colab).

5. **Model Weights**: Pre-trained models are downloaded automatically when you use `pretrained=True`.

---

## Troubleshooting

### Issue: CUDA out of memory
**Solution**: Reduce batch size or use CPU mode:
```python
device = 'cpu'
model = model.to(device)
```

### Issue: Module not found
**Solution**: Make sure you've installed the project:
```python
!pip install -e /content/DataCompression/lossy-vae
```

### Issue: Dataset path not found
**Solution**: Update paths in `lvae/paths.py`:
```python
from lvae.paths import known_datasets
known_datasets['kodak'] = '/content/datasets/kodak'
```

---

## Next Steps

- Check out `demo_colab_kaggle.ipynb` for a complete working example
- Read the main `README.md` for more details
- Explore model-specific READMEs in `lvae/models/*/README.md`

