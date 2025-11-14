# Lossy-VAE

---

Data Compression Project By:

Vignesh S B 22MID0190

Adit Ranganathan Suresh 22MID0197

S. Chandramuke 22MID0163

---

A PyTorch library for lossy image and video compression using state-of-the-art Variational Autoencoder (VAE) models. Features continuously variable-rate compression with competitive performance against traditional codecs.

## Features

- **Variable-rate compression**: Single model supports bitrates from 0.2 to 2.2 bpp
- **State-of-the-art performance**: Outperforms VTM 18.0 by 5-9% in BD-rate
- **Multiple architectures**: QARV and QRes-VAE models available
- **Easy to use**: Simple Python API and command-line tools
- **Web demo**: Interactive browser-based compression interface

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from lvae import get_model
import torch

# Load pre-trained model
model = get_model('qarv_base', pretrained=True)
model.eval()
model.compress_mode(True)

# Compress an image
model.compress_file('input.png', 'compressed.bits')

# Decompress
reconstructed = model.decompress_file('compressed.bits')
```

### Command-Line Demo

```bash
python demo_compress.py input.png --output reconstructed.png --model qarv_base
```

### Web Demo

```bash
python web_demo.py
# Open http://localhost:5000 in your browser
```

## Models

| Model | Parameters | Bpp Range | BD-rate (vs VTM 18.0) |
|-------|-----------|-----------|------------------------|
| `qarv_base` | 93.4M | 0.21 - 2.21 | -5.9% (Kodak) |

## Evaluation

```bash
python eval-var-rate.py --model qarv_base --dataset_name kodak --device cuda:0
```

## Training

```bash
python train-var-rate.py --model qarv_base --batch_size 32 --iterations 2_000_000
```

## Documentation

- [QARV Model Details](lvae/models/qarv/README.md)
- [QRes-VAE Model Details](lvae/models/qresvae/README.md)

