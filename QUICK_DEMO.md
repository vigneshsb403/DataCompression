# Quick Demo Guide

## 🚀 Fastest Way to See It Work

### Step 1: Compress an Image (30 seconds)

```bash
cd /home/ec2-user/DataCompression/lossy-vae
python demo_compress.py images/collie128.png
```

This will:
- ✅ Load the model
- ✅ Compress the image
- ✅ Decompress it back
- ✅ Show you compression stats
- ✅ Save the results

**Output files:**
- `images/collie128_reconstructed.png` - See the quality
- `images/collie128_compressed.bits` - The compressed file

### Step 2: Try Your Own Image

```bash
# Copy your image to the project directory first
python demo_compress.py your_image.jpg
```

### Step 3: Adjust Quality

```bash
# More compression (smaller file, lower quality)
python demo_compress.py your_image.jpg --lmb 64

# Better quality (larger file, higher quality)
python demo_compress.py your_image.jpg --lmb 512
```

## 🌐 Web Interface (Best for Presentations)

### Option A: Direct Access (Port 5000)

```bash
# Install Flask if needed
pip install flask

# Start server
python web_demo.py
```

**Access:** `http://YOUR_EC2_PUBLIC_IP:5000`

**Note:** Requires port 5000 open in security group.

### Option B: Via Nginx (Port 80) - Recommended

**Setup nginx reverse proxy (one-time setup):**

```bash
cd /home/ec2-user/DataCompression/lossy-vae
chmod +x setup_nginx.sh
./setup_nginx.sh
```

**Then start Flask app:**
```bash
python web_demo.py
```

**Access:** `http://YOUR_EC2_PUBLIC_IP` (no port needed!)

**Note:** Only requires port 80 open in security group (usually already open).

### Use It

1. Upload an image (drag & drop or click)
2. Adjust the quality slider
3. Click "Compress Image"
4. See side-by-side comparison
5. Download the results

## 📥 Downloading Results

### From AWS to Your Computer

```bash
# From your local machine
scp ec2-user@YOUR_EC2_IP:/home/ec2-user/DataCompression/lossy-vae/images/*_reconstructed.png ./
```

Or use the web interface download buttons!

## 🎓 For Your Faculty Presentation

**Option 1: Show Command Line**
```bash
python demo_compress.py your_image.png
# Show the output and statistics
```

**Option 2: Show Web Interface** (Recommended)
```bash
python web_demo.py
# Open in browser, upload image, show interactive compression
```

**What to Show:**
- Original vs compressed image side-by-side
- Compression ratio (e.g., "3.5x smaller")
- Bits per pixel (BPP) metric
- File size comparison
- Quality slider demonstration

## 💡 Tips

- **Lambda values:** 16-128 = more compression, 512-2048 = better quality
- **Best for demo:** Use λ=256 (default) for balanced results
- **Large images:** May take longer, but will work
- **CPU is fine:** Works on CPU-only instances (just slower)

## 🐛 Troubleshooting

**"No module named flask"**
```bash
pip install flask
```

**"Model not found"**
```bash
pip install -e .
```

**Web interface not accessible**
- Check AWS security group (port 5000)
- Try `localhost:5000` first to test locally

That's it! You're ready to demo! 🎉

