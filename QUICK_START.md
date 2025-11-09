# Quick Start Guide: Google Colab & Kaggle

## 🚀 Google Colab (Recommended for Beginners)

### Step 1: Open Colab
1. Go to https://colab.research.google.com/
2. Click `File` → `New notebook`

### Step 2: Enable GPU
1. Click `Runtime` → `Change runtime type`
2. Set `Hardware accelerator` to `GPU`
3. Click `Save`

### Step 3: Upload Project
**Method A: Direct Upload**
1. Click the folder icon (📁) on the left sidebar
2. Click `Upload` button
3. Upload your entire `DataCompression` folder
4. Wait for upload to complete

**Method B: Using Git (if your repo is on GitHub)**
```python
!git clone https://github.com/your-username/your-repo.git
```

### Step 4: Run the Demo Notebook
1. Upload `demo_colab_kaggle.ipynb` to Colab
2. Open it and run all cells
3. Or copy the cells from the notebook into your own notebook

### Step 5: Quick Test
Run this in a cell:
```python
# Install dependencies
!pip install -q tqdm timm compressai

# Navigate to project
%cd /content/DataCompression/lossy-vae
!pip install -e .

# Import models to register them (IMPORTANT!)
from lvae.models import qarv, qresvae, rd
from lvae import get_model
import torch

model = get_model('qarv_base', pretrained=True)
model = model.to('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()
model.compress_mode(True)
print("✅ Model loaded!")
```

---

## 🎯 Kaggle

### Step 1: Create Dataset
1. Go to https://www.kaggle.com/
2. Click `Datasets` → `New Dataset`
3. Upload your `DataCompression` folder as a zip file
4. Name it (e.g., "lossy-vae-project")
5. Click `Create`

### Step 2: Create Notebook
1. Click `Code` → `New Notebook`
2. Click `Settings` → `Accelerator` → Select `GPU`
3. Click `Add data` → Search for your dataset → `Add`

### Step 3: Setup Code
In the first cell, run:
```python
import shutil
from pathlib import Path

# Copy project to working directory
input_path = Path('/kaggle/input')
for item in input_path.iterdir():
    if 'lossy' in item.name.lower() or 'datacompression' in item.name.lower():
        shutil.copytree(item / 'DataCompression', 
                      '/kaggle/working/DataCompression', 
                      dirs_exist_ok=True)
        break

# Install dependencies
!pip install -q tqdm timm compressai

# Install project
%cd /kaggle/working/DataCompression/lossy-vae
!pip install -e .

print("✅ Setup complete!")
```

### Step 4: Use the Project
```python
from lvae import get_model
import torch

model = get_model('qarv_base', pretrained=True)
model = model.to('cuda')
model.eval()
model.compress_mode(True)
print("✅ Model loaded!")
```

---

## 📝 Example: Compress an Image

```python
from PIL import Image
from torchvision.utils import save_image

# Compress
model.compress_file('/path/to/image.png', '/tmp/compressed.bits')

# Decompress
reconstructed = model.decompress_file('/tmp/compressed.bits')
save_image(reconstructed, '/tmp/reconstructed.png')

print("✅ Done!")
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'lvae'"
**Solution**: Make sure you ran `pip install -e .` in the project directory

### "CUDA out of memory"
**Solution**: Use CPU mode or reduce batch size
```python
model = model.to('cpu')  # Use CPU instead
```

### "Dataset not found"
**Solution**: Update paths manually
```python
from lvae.paths import known_datasets
known_datasets['kodak'] = '/content/datasets/kodak'
```

### Project files not found
**Colab**: Check that files are in `/content/DataCompression/lossy-vae/`
**Kaggle**: Make sure you copied files to `/kaggle/working/`

---

## 📚 Next Steps

1. Open `demo_colab_kaggle.ipynb` for complete examples
2. Read `COLAB_KAGGLE_SETUP.md` for detailed instructions
3. Check `README.md` for full documentation

---

## 💡 Tips

- **Colab**: Files are temporary - download important results before session ends
- **Kaggle**: Use `/kaggle/working/` for outputs you want to save
- **Both**: GPU sessions have time limits - save your work frequently
- **Performance**: GPU is ~10x faster than CPU for this project

---

## 🎓 Learning Resources

- Main README: `README.md`
- Model docs: `lvae/models/*/README.md`
- Evaluation scripts: `eval-*.py`

Happy compressing! 🎉

