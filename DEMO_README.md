# Lossy-VAE Demo Guide

This guide shows you how to use the Lossy-VAE image compression demos.

## Quick Start

### Option 1: Command-Line Demo (Simple)

The simplest way to compress an image:

```bash
python demo_compress.py path/to/your/image.png
```

This will:
- Compress the image
- Decompress it back
- Save the reconstructed image as `image_reconstructed.png`
- Save the compressed bits as `image_compressed.bits`
- Show compression statistics

**Advanced usage:**

```bash
# Specify output file
python demo_compress.py input.png --output result.png

# Use different compression quality (lambda)
python demo_compress.py input.png --lmb 128  # Lower = more compression
python demo_compress.py input.png --lmb 512  # Higher = better quality

# Use different model
python demo_compress.py input.png --model qres34m

# Save compressed bits to specific location
python demo_compress.py input.png --bits-file my_compressed.bits
```

**Lambda values:**
- Lower values (16-128): More compression, smaller files, lower quality
- Higher values (512-2048): Less compression, larger files, higher quality
- Default: Model-specific (usually around 256)

### Option 2: Web Interface (Interactive)

**First, install Flask (if not already installed):**
```bash
pip install flask
```

Start the web server:

```bash
python web_demo.py
```

Then open your browser to: `http://localhost:5000`

**Features:**
- Drag & drop image upload
- Real-time quality adjustment slider
- Side-by-side comparison of original vs compressed
- Download compressed image and bits file
- Beautiful, modern UI

**To access from another machine:**
The server runs on `0.0.0.0:5000` by default, so you can access it from other machines on your network:
- Find your IP address: `hostname -I` (Linux) or `ipconfig` (Windows)
- Access from another machine: `http://YOUR_IP:5000`

**For AWS instances:**
1. Make sure port 5000 is open in your security group
2. Access via: `http://YOUR_EC2_PUBLIC_IP:5000`

## Examples

### Example 1: Basic Compression

```bash
python demo_compress.py images/collie128.png
```

Output:
```
Using device: cpu
Loading model: qarv_base
✅ Model loaded successfully!

Compressing image: images/collie128.png
Lambda: default

Compression stats:
  Original size: 45,234 bytes (44.17 KB)
  Compressed size: 12,456 bytes (12.16 KB)
  Compression ratio: 3.63x
  Bits per pixel (BPP): 0.1523

Decompressing...
✅ Reconstructed image saved to: images/collie128_reconstructed.png
✅ Compressed bits saved to: images/collie128_compressed.bits
```

### Example 2: High Quality Compression

```bash
python demo_compress.py my_photo.jpg --lmb 1024 --output high_quality_result.png
```

### Example 3: Maximum Compression

```bash
python demo_compress.py my_photo.jpg --lmb 16 --output compressed_result.png
```

## Sharing Results

### For Your Faculty Presentation

1. **Compress an image:**
   ```bash
   python demo_compress.py your_image.png
   ```

2. **You'll get:**
   - `your_image_reconstructed.png` - The decompressed image (to show quality)
   - `your_image_compressed.bits` - The compressed file (to show compression)

3. **Show the comparison:**
   - Open both original and reconstructed images side-by-side
   - Show the compression statistics
   - Demonstrate the file size reduction

4. **Use the web interface:**
   - Start the web demo: `python web_demo.py`
   - Show the interactive interface
   - Upload images and adjust quality in real-time
   - Download results directly

### Downloading Files from AWS

If you're running on AWS:

```bash
# From your local machine, use SCP to download files
scp ec2-user@YOUR_EC2_IP:/home/ec2-user/DataCompression/lossy-vae/outputs/*.png ./
scp ec2-user@YOUR_EC2_IP:/home/ec2-user/DataCompression/lossy-vae/outputs/*.bits ./
```

Or use the web interface download buttons!

## Understanding the Output

### Compression Ratio
- **3x** means the compressed file is 3 times smaller than the original
- Higher is better (more compression)

### Bits Per Pixel (BPP)
- Lower BPP = more compression
- Typical values: 0.1-0.5 BPP for good quality
- Original uncompressed: ~24 BPP (8 bits per channel × 3 channels)

### Lambda (λ)
- Controls the trade-off between compression and quality
- Lower λ: More compression, lower quality
- Higher λ: Less compression, higher quality
- Range: 16-2048 (model dependent)

## Troubleshooting

### "Model not found" error
Make sure you've installed the project:
```bash
pip install -e .
```

### "CUDA not available" warning
This is normal on CPU-only instances. The model will run on CPU (slower but works fine).

### Web interface not accessible
- Check firewall settings
- Make sure port 5000 is open
- Try accessing via `localhost:5000` first

### Out of memory errors
- Use smaller images
- Use lower lambda values (more compression)
- Close other applications

## Next Steps

- Try different models: `qarv_base`, `qres34m`, `rd_model_base`
- Experiment with different lambda values
- Compress multiple images and compare results
- Use the evaluation scripts for batch processing

For more advanced usage, check the main README.md and the scripts in the `scripts/` directory.

