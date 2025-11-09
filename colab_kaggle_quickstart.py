"""
Quick start script for Google Colab and Kaggle
Run this in a single cell to set up everything!
"""

import os
import sys
import subprocess
from pathlib import Path

def detect_platform():
    if 'COLAB_GPU' in os.environ:
        return 'colab'
    elif 'KAGGLE_KERNEL_TYPE' in os.environ:
        return 'kaggle'
    return 'local'

def setup():
    platform = detect_platform()
    print(f"🚀 Platform detected: {platform.upper()}")
    
    if platform == 'colab':
        project_dir = Path('/content/DataCompression/lossy-vae')
        datasets_root = Path('/content/datasets')
    elif platform == 'kaggle':
        project_dir = Path('/kaggle/working/DataCompression/lossy-vae')
        datasets_root = Path('/kaggle/input/datasets')
        
        if not project_dir.exists():
            print("📦 Copying project from input to working directory...")
            import shutil
            input_path = Path('/kaggle/input')
            for item in input_path.iterdir():
                if 'datacompression' in item.name.lower() or 'lossy' in item.name.lower():
                    src = item / 'DataCompression'
                    if src.exists():
                        shutil.copytree(src, '/kaggle/working/DataCompression', dirs_exist_ok=True)
                        print(f"✅ Copied from {src}")
                        break
    else:
        project_dir = Path('.')
        datasets_root = Path('./datasets')
    
    if not project_dir.exists():
        print(f"❌ ERROR: Project not found at {project_dir}")
        print("Please upload the project files first!")
        return None, None
    
    os.chdir(project_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    print("\n🔧 Fixing numpy compatibility...")
    print("   Installing numpy 1.26.4 (compatible with PyTorch)...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'numpy==1.26.4'], check=False)
    
    print("\n📦 Installing dependencies...")
    deps = ['tqdm', 'timm', 'compressai']
    for dep in deps:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', dep], check=False)
    
    print("\n🔍 Checking PyTorch...")
    try:
        import torch
        print(f"   PyTorch: {torch.__version__}")
        print(f"   CUDA: {'✅ Available' if torch.cuda.is_available() else '❌ Not available'}")
        if torch.cuda.is_available():
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("   Installing PyTorch...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'torch', 'torchvision', 'torchaudio', 
                       '--index-url', 'https://download.pytorch.org/whl/cu118'], check=False)
    
    print("\n⚙️  Installing project...")
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Project installed successfully!")
    else:
        print(f"   ⚠️  Installation warning (may be OK): {result.stderr[:100]}")
    
    datasets_root.mkdir(parents=True, exist_ok=True)
    print(f"\n📂 Datasets directory: {datasets_root}")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Import models: from lvae.models import qarv, qresvae, rd")
    print("2. Load a model: from lvae import get_model")
    print("3. Get model: model = get_model('qarv_base', pretrained=True)")
    print("4. Move to GPU: model = model.to('cuda')")
    print("5. Enable compression: model.compress_mode(True)")
    
    return project_dir, datasets_root

if __name__ == '__main__':
    setup()

