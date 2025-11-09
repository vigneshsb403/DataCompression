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

def setup_aws_environment():
    print("=== AWS Deep Learning AMI Setup ===")
    
    print("\n=== Checking PyTorch installation ===")
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("ERROR: PyTorch not found. This script expects PyTorch to be pre-installed.")
        print("If using Ubuntu, install PyTorch manually:")
        print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        return False
    
    print("\n=== Fixing NumPy compatibility ===")
    print("Installing numpy 1.26.4 (compatible with PyTorch)...")
    run_command("pip install --force-reinstall numpy==1.26.4", check=False)
    
    print("\n=== Installing project dependencies ===")
    deps = ['tqdm', 'timm', 'compressai']
    for dep in deps:
        print(f"Installing {dep}...")
        run_command(f"pip install -q {dep}", check=False)
    
    print("\n=== Setting up project ===")
    project_dir = Path.cwd()
    if not (project_dir / 'lvae').exists():
        print(f"ERROR: Project not found at {project_dir}")
        print("Please navigate to the lossy-vae directory first:")
        print(f"  cd /path/to/DataCompression/lossy-vae")
        return False
    
    print(f"Project directory: {project_dir}")
    os.chdir(project_dir)
    print("Installing project in development mode...")
    run_command("pip install -e .", check=False)
    
    print("\n=== Verifying installation ===")
    try:
        import torch
        import timm
        import compressai
        print("✅ Core dependencies imported successfully")
        
        from lvae.models import qarv, qresvae, rd
        from lvae import get_model
        print("✅ Project modules imported successfully")
        
        print("\n=== Setup complete! ===")
        print(f"Project directory: {project_dir}")
        print("\nQuick test:")
        print("  from lvae import get_model")
        print("  model = get_model('qarv_base', pretrained=True)")
        print("  model.eval()")
        print("  model.compress_mode(True)")
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == '__main__':
    success = setup_aws_environment()
    sys.exit(0 if success else 1)

