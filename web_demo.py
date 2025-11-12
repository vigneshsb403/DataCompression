#!/usr/bin/env python3
"""
Web-based demo for image compression using Lossy-VAE models.
Run with: python web_demo.py
Then open http://localhost:5000 in your browser.
"""

import os
import io
import base64
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import torch
from torchvision.utils import save_image
import numpy as np

from lvae import get_model

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Loading model on device: {device}")

model = None
model_name = 'qarv_base'

def load_model():
    global model
    if model is None:
        print(f"Loading model: {model_name}")
        model = get_model(model_name, pretrained=True)
        model = model.to(device)
        model.eval()
        model.compress_mode(True)
        print("✅ Model loaded successfully!")
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        lmb = request.form.get('lmb', type=float)
        
        file_data = file.read()
        img = Image.open(io.BytesIO(file_data))
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        upload_path = Path(app.config['UPLOAD_FOLDER']) / file.filename
        bits_path = Path(app.config['OUTPUT_FOLDER']) / f"{Path(file.filename).stem}.bits"
        output_path = Path(app.config['OUTPUT_FOLDER']) / f"{Path(file.filename).stem}_reconstructed.png"
        
        img.save(upload_path)
        original_size = upload_path.stat().st_size
        
        model = load_model()
        model.compress_file(str(upload_path), str(bits_path), lmb=lmb)
        
        reconstructed = model.decompress_file(str(bits_path))
        save_image(reconstructed, str(output_path))
        
        compressed_size = bits_path.stat().st_size
        original_file_size = upload_path.stat().st_size
        compression_ratio = original_file_size / compressed_size
        bpp = (compressed_size * 8) / (img.height * img.width)
        
        with open(output_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        
        return jsonify({
            'success': True,
            'original_size': original_file_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(compression_ratio, 2),
            'bpp': round(bpp, 4),
            'image_width': img.width,
            'image_height': img.height,
            'reconstructed_image': f"data:image/png;base64,{img_data}",
            'bits_file': str(bits_path),
            'output_file': str(output_path)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decompress', methods=['POST'])
def decompress():
    try:
        if 'bits_file' not in request.files:
            return jsonify({'error': 'No bits file provided'}), 400
        
        file = request.files['bits_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        bits_path = Path(app.config['UPLOAD_FOLDER']) / file.filename
        output_path = Path(app.config['OUTPUT_FOLDER']) / f"{Path(file.filename).stem}_decompressed.png"
        
        file.save(bits_path)
        compressed_size = bits_path.stat().st_size
        
        model = load_model()
        reconstructed = model.decompress_file(str(bits_path))
        save_image(reconstructed, str(output_path))
        
        img = Image.open(output_path)
        
        with open(output_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        
        return jsonify({
            'success': True,
            'compressed_size': compressed_size,
            'image_width': img.width,
            'image_height': img.height,
            'reconstructed_image': f"data:image/png;base64,{img_data}",
            'output_file': str(output_path)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    file_path = Path(app.config['OUTPUT_FOLDER']) / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    upload_path = Path(app.config['UPLOAD_FOLDER']) / filename
    if upload_path.exists():
        return send_file(upload_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Lossy-VAE Web Demo")
    print("="*50)
    print(f"Server starting on http://localhost:5000")
    print(f"Device: {device}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

