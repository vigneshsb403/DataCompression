# AWS Setup Guide for Lossy-VAE

## Recommended AMI: Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.8 (Amazon Linux 2023)

**AMI ID (x86):** `ami-0ed1f9c6688900cdf`  
**AMI ID (Arm):** `ami-00189455fa2afc745`

## Why This AMI?

- ✅ PyTorch 2.8 pre-installed (project requires >= 1.9)
- ✅ CUDA and GPU drivers pre-configured
- ✅ Minimal setup required
- ✅ Free tier eligible

## Setup Steps

### 1. Launch EC2 Instance

1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Search for AMI ID: `ami-0ed1f9c6688900cdf` (x86) or `ami-00189455fa2afc745` (Arm)
4. Select instance type with GPU (e.g., `g4dn.xlarge` for free tier, or `g4dn.2xlarge` for better performance)
5. Configure security group to allow SSH (port 22)
6. Launch instance

### 2. Connect to Instance

```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

### 3. Upload Project Files

**Option A: Using SCP**
```bash
scp -r -i your-key.pem /path/to/DataCompression ec2-user@your-instance-ip:~/
```

**Option B: Using Git (if repo is on GitHub)**
```bash
git clone https://github.com/your-username/your-repo.git
```

### 4. Run Setup Script

```bash
cd ~/DataCompression/lossy-vae
python3 setup_aws.py
```

### 5. Verify Installation

```python
python3
>>> import torch
>>> print(f"PyTorch: {torch.__version__}")
>>> print(f"CUDA available: {torch.cuda.is_available()}")
>>> from lvae import get_model
>>> model = get_model('qarv_base', pretrained=True)
>>> model.eval()
>>> model.compress_mode(True)
>>> print("✅ Setup successful!")
```

## Alternative: Ubuntu Linux

If you prefer Ubuntu, use a basic Ubuntu 22.04 AMI and install manually:

### 1. Install CUDA and GPU Drivers

```bash
sudo apt update
sudo apt install -y nvidia-driver-535
sudo reboot
```

After reboot, verify:
```bash
nvidia-smi
```

### 2. Install PyTorch

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. Install Project Dependencies

```bash
pip3 install numpy==1.26.4 tqdm timm compressai
```

### 4. Install Project

```bash
cd ~/DataCompression/lossy-vae
pip3 install -e .
```

## Troubleshooting

### NumPy Compatibility Issues

If you get numpy compatibility errors:
```bash
pip3 install --force-reinstall numpy==1.26.4
```

### CUDA Not Available

Check GPU:
```bash
nvidia-smi
```

Verify PyTorch CUDA:
```python
import torch
print(torch.cuda.is_available())
```

### Out of Memory

- Use smaller batch sizes in training scripts
- Consider using a larger instance type (e.g., `g4dn.2xlarge`)

## Instance Type Recommendations

- **Free Tier / Testing:** `g4dn.xlarge` (1 GPU, 4 vCPU, 16 GB RAM)
- **Training:** `g4dn.2xlarge` (1 GPU, 8 vCPU, 32 GB RAM) or `g4dn.4xlarge` (1 GPU, 16 vCPU, 64 GB RAM)
- **Large Scale:** `p3.2xlarge` (1 GPU, 8 vCPU, 61 GB RAM) - not free tier

## Cost Optimization Tips

1. Use Spot Instances for training (up to 90% discount)
2. Stop instances when not in use
3. Use smaller instance types for inference/testing
4. Consider AWS Batch for batch processing jobs

