import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, check=True):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result

def detect_platform():
    if 'COLAB_GPU' in os.environ:
        return 'colab'
    elif 'KAGGLE_KERNEL_TYPE' in os.environ:
        return 'kaggle'
    else:
        return 'unknown'

def setup_environment():
    platform = detect_platform()
    print(f"Detected platform: {platform}")
    
    print("\n=== Installing dependencies ===")
    
    if platform == 'colab':
        run_command("pip install -q tqdm timm compressai")
    else:
        run_command("pip install -q tqdm timm compressai")
    
    print("\n=== Checking PyTorch installation ===")
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("PyTorch not found. Installing...")
        run_command("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    
    print("\n=== Setting up project ===")
    
    if platform == 'colab':
        project_dir = Path('/content/DataCompression/lossy-vae')
    else:
        project_dir = Path('/kaggle/working/DataCompression/lossy-vae')
    
    project_dir.parent.mkdir(parents=True, exist_ok=True)
    
    if not (project_dir / 'lvae').exists():
        print("Project not found. Please upload the project files or clone from git.")
        print(f"Expected location: {project_dir}")
    else:
        print(f"Project found at: {project_dir}")
        os.chdir(project_dir)
        run_command("pip install -e .", check=False)
    
    print("\n=== Setting up dataset paths ===")
    if platform == 'colab':
        datasets_root = Path('/content/datasets')
    else:
        datasets_root = Path('/kaggle/input') / 'datasets'
    
    datasets_root.mkdir(parents=True, exist_ok=True)
    print(f"Datasets root: {datasets_root}")
    
    print("\n=== Setup complete! ===")
    print(f"Project directory: {project_dir}")
    print(f"Datasets directory: {datasets_root}")
    
    return project_dir, datasets_root

if __name__ == '__main__':
    setup_environment()

