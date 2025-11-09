# Running Lossy-VAE on Google Colab & Kaggle

Complete guide to run this project on free GPU platforms.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Google Colab Setup](#google-colab-setup)
3. [Kaggle Setup](#kaggle-setup)
4. [Usage Examples](#usage-examples)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Option 1: Use the Demo Notebook (Easiest)
1. Upload `demo_colab_kaggle.ipynb` to Colab or Kaggle
2. Run all cells
3. Done! ✅

### Option 2: Use the Quick Start Script
Copy and run this in a single cell:

```python
exec(open('colab_kaggle_quickstart.py').read())
```

### Option 3: Manual Setup
See detailed instructions below.

---

## 📘 Google Colab Setup

### Prerequisites
- Google account (free)
- Basic Python knowledge

### Step-by-Step

#### 1. Open Google Colab
- Go to https://colab.research.google.com/
- Click `File` → `New notebook`

#### 2. Enable GPU
- Click `Runtime` → `Change runtime type`
- Set `Hardware accelerator` to `GPU` (T4)
- Click `Save`

#### 3. Upload Project Files

**Method A: Direct Upload (Recommended)**
```python
# Run this in a cell to upload files
from google.colab import files
import zipfile
import os

# Upload the DataCompression folder as a zip file
uploaded = files.upload()

# Extract
for fn in uploaded.keys():
    with zipfile.ZipFile(fn, 'r') as zip_ref:
        zip_ref.extractall('/content/')
```

**Method B: Using File Browser**
1. Click the folder icon (📁) on left sidebar
2. Click `Upload` button
3. Upload your `DataCompression` folder
4. Wait for upload to complete

**Method C: Git Clone (if repo is public)**
```python
!git clone https://github.com/your-username/your-repo.git
```

#### 4. Run Setup
```python
%cd /content/DataCompression/lossy-vae
exec(open('colab_kaggle_quickstart.py').read())
```

Or manually:
```python
%cd /content/DataCompression/lossy-vae

# Install dependencies
!pip install -q tqdm timm compressai

# Install project
!pip install -e .

print("✅ Setup complete!")
```

#### 5. Verify Installation
```python
# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
model = get_model('qarv_base', pretrained=True)
print("✅ Model loaded!")
```

---

## 🎯 Kaggle Setup

### Prerequisites
- Kaggle account (free)
- Basic Python knowledge

### Step-by-Step

#### 1. Create Dataset
1. Go to https://www.kaggle.com/
2. Click `Datasets` → `New Dataset`
3. Upload your `DataCompression` folder (zip it first)
4. Name it (e.g., "lossy-vae-compression")
5. Click `Create`

#### 2. Create Notebook
1. Click `Code` → `New Notebook`
2. Click `Settings` (⚙️) → `Accelerator` → Select `GPU`
3. Click `Add data` → Search for your dataset → `Add`

#### 3. Setup Code
Run this in the first cell:

```python
import shutil
from pathlib import Path

# Find and copy project
input_path = Path('/kaggle/input')
for item in input_path.iterdir():
    if 'lossy' in item.name.lower() or 'datacompression' in item.name.lower():
        src = item / 'DataCompression'
        if src.exists():
            shutil.copytree(src, '/kaggle/working/DataCompression', dirs_exist_ok=True)
            print(f"✅ Copied from {src}")
            break

# Install dependencies
!pip install -q tqdm timm compressai

# Install project
%cd /kaggle/working/DataCompression/lossy-vae
!pip install -e .

print("✅ Setup complete!")
```

#### 4. Verify Installation
```python
# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model
import torch

model = get_model('qarv_base', pretrained=True)
model = model.to('cuda')
model.eval()
model.compress_mode(True)
print("✅ Ready to use!")
```

---

## 💻 Usage Examples

### Example 1: Basic Compression
```python
# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model
import torch

# Load model
model = get_model('qarv_base', pretrained=True)
model = model.to('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()
model.compress_mode(True)

# Compress an image
model.compress_file('/path/to/image.png', '/tmp/compressed.bits')

# Decompress
from torchvision.utils import save_image
reconstructed = model.decompress_file('/tmp/compressed.bits')
save_image(reconstructed, '/tmp/reconstructed.png')
```

### Example 2: Variable Rate Compression
```python
# Different quality levels
lambdas = [16, 64, 256, 1024]  # Lower = smaller file, lower quality

for lmb in lambdas:
    model.compress_file('image.png', f'/tmp/compressed_lmb{lmb}.bits', lmb=lmb)
    reconstructed = model.decompress_file(f'/tmp/compressed_lmb{lmb}.bits')
    save_image(reconstructed, f'/tmp/recon_lmb{lmb}.png')
```

### Example 3: Evaluate on Dataset
```python
from lvae.evaluation import imcoding_evaluate
from lvae.paths import known_datasets

# Set dataset path
known_datasets['kodak'] = '/content/datasets/kodak'

# Evaluate
results = imcoding_evaluate(model, 'kodak')
print(f"BPP: {results['bpp']:.4f}, PSNR: {results['psnr']:.2f} dB")
```

### Example 4: Download Test Dataset
```python
from torch.hub import download_url_to_file
from pathlib import Path
from tqdm import tqdm

def download_kodak(target_dir):
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    urls = [f'http://r0k.us/graphics/kodak/kodak/kodim{str(i).zfill(2)}.png' 
            for i in range(1, 25)]
    for url in tqdm(urls):
        download_url_to_file(url, target_dir / Path(url).name, progress=False)

download_kodak('/content/datasets/kodak')
```

---

## 🔧 Troubleshooting

### Problem: "ValueError: numpy.dtype size changed"
**Solution:** NumPy 2.x is incompatible with PyTorch. Install compatible version:
```python
# Step 1: Install compatible numpy
!pip install --force-reinstall numpy==1.26.4

# Step 2: RESTART RUNTIME (REQUIRED!)
# Colab: Runtime → Restart runtime
# Kaggle: Session → Restart Session

# Step 3: Run your cells again
```
**Important:** You MUST restart runtime after changing numpy version!

### Problem: "KeyError: 'qarv_base'" or "KeyError: 'qres34m'"
**Solution:** You need to import the model modules before using `get_model()`:
```python
# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model

model = get_model('qarv_base', pretrained=True)
```

### Problem: "ModuleNotFoundError: No module named 'lvae'"
**Solution:**
```python
%cd /content/DataCompression/lossy-vae  # or /kaggle/working/...
!pip install -e .
```

### Problem: "CUDA out of memory"
**Solutions:**
1. Use CPU mode:
   ```python
   model = model.to('cpu')
   ```
2. Reduce batch size in evaluation scripts
3. Process images one at a time

### Problem: "Dataset not found"
**Solution:**
```python
from lvae.paths import known_datasets
known_datasets['kodak'] = '/content/datasets/kodak'  # Update path
```

### Problem: Project files not found
**Colab:** Check files are in `/content/DataCompression/lossy-vae/`
**Kaggle:** Make sure you copied to `/kaggle/working/DataCompression/`

### Problem: GPU not available
**Check:**
```python
import torch
print(torch.cuda.is_available())
```
- Colab: Runtime → Change runtime type → GPU
- Kaggle: Settings → Accelerator → GPU

### Problem: Slow performance
- Make sure GPU is enabled
- Check GPU is being used: `model = model.to('cuda')`
- Verify: `next(model.parameters()).device` should show `cuda:0`

---

## 📊 Platform Comparison

| Feature | Google Colab | Kaggle |
|---------|-------------|--------|
| **GPU** | T4 (16GB) | P100 (16GB) |
| **Session Time** | ~12 hours | 30 hrs/week |
| **Storage** | ~80GB | ~20GB |
| **Best For** | Quick experiments | Longer training |
| **File Persistence** | Temporary | Can save outputs |

---

## 📚 Additional Resources

- **Main README**: `README.md` - Full project documentation
- **Quick Start**: `QUICK_START.md` - Simplified guide
- **Demo Notebook**: `demo_colab_kaggle.ipynb` - Interactive examples
- **Model Docs**: `lvae/models/*/README.md` - Model-specific guides

---

## 💡 Tips & Best Practices

1. **Save Your Work**
   - Colab: Download important files before session ends
   - Kaggle: Save outputs to `/kaggle/working/` (persists)

2. **Manage Storage**
   - Delete large datasets when done
   - Use `!du -sh /path` to check disk usage

3. **Session Management**
   - Colab: Sessions auto-disconnect after inactivity
   - Kaggle: Monitor GPU hours usage

4. **Performance**
   - Always use GPU for training/inference
   - Batch multiple operations when possible

5. **Debugging**
   - Use `print()` statements liberally
   - Check paths with `Path.exists()`
   - Verify device with `next(model.parameters()).device`

---

## 🎓 Next Steps

1. ✅ Complete setup (you're here!)
2. Run `demo_colab_kaggle.ipynb` for examples
3. Try compressing your own images
4. Experiment with different models (`qres34m`, `qarv_base`)
5. Evaluate on test datasets
6. Read model-specific documentation

---

## 🆘 Need Help?

1. Check `TROUBLESHOOTING` section above
2. Read the main `README.md`
3. Check model-specific READMEs in `lvae/models/*/`
4. Review error messages carefully

---

**Happy Compressing! 🎉**

