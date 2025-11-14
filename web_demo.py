#!/usr/bin/env python3
"""
Web-based demo for image compression using Lossy-VAE models.
Run with: python web_demo.py
Then open http://localhost:5000 in your browser.
"""

import os
import io
import base64
import tempfile
import struct
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
from torchvision.utils import save_image

from lvae import get_model

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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

def decompress_from_bytes(bits_data):
    """Decompress from bytes data instead of file path."""
    # Create a temporary file to use with decompress_file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.bits') as tmp_file:
        tmp_file.write(bits_data)
        tmp_path = tmp_file.name
    
    try:
        model = load_model()
        reconstructed = model.decompress_file(tmp_path)
        return reconstructed
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def validate_bits_file(bits_data):
    """Validate that the bits file has the correct format."""
    if len(bits_data) < 4:
        raise ValueError("File is too small to be a valid bits file (must be at least 4 bytes)")
    
    # Check header (first 4 bytes should be image dimensions)
    try:
        header = bits_data[:4]
        img_h, img_w = struct.unpack('2H', header)
        if img_h == 0 or img_w == 0 or img_h > 100000 or img_w > 100000:
            raise ValueError("Invalid image dimensions in bits file header")
    except struct.error as e:
        raise ValueError(f"Invalid bits file format: {str(e)}")
    
    # Check that there's enough data for at least lambda + shape + packed strings
    if len(bits_data) < 4 + 4 + 6 + 1:  # header + lambda + shape + at least 1 byte for packed strings
        raise ValueError("File is too small - missing compression data")
    
    return True

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
        
        original_size = len(file_data)
        
        # Use temporary files for compression/decompression
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
            img.save(tmp_img.name)
            tmp_img_path = tmp_img.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bits') as tmp_bits:
            tmp_bits_path = tmp_bits.name
        
        try:
            model = load_model()
            model.compress_file(tmp_img_path, tmp_bits_path, lmb=lmb)
            
            # Read compressed size and data
            compressed_size = os.path.getsize(tmp_bits_path)
            with open(tmp_bits_path, 'rb') as f:
                bits_data = f.read()
            bits_data_b64 = base64.b64encode(bits_data).decode()
            
            # Decompress to get reconstructed image
            reconstructed = model.decompress_file(tmp_bits_path)
            
            # Save reconstructed image to memory
            img_buffer = io.BytesIO()
            save_image(reconstructed, img_buffer, format='PNG')
            img_buffer.seek(0)
            img_data = base64.b64encode(img_buffer.read()).decode()
            
            compression_ratio = original_size / compressed_size
            bpp = (compressed_size * 8) / (img.height * img.width)
            
            return jsonify({
                'success': True,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': round(compression_ratio, 2),
                'bpp': round(bpp, 4),
                'image_width': img.width,
                'image_height': img.height,
                'reconstructed_image': f"data:image/png;base64,{img_data}",
                'bits_file_data': bits_data_b64,
                'bits_file_name': f"{Path(file.filename).stem}.bits"
            })
        finally:
            # Clean up temporary files
            if os.path.exists(tmp_img_path):
                os.unlink(tmp_img_path)
            if os.path.exists(tmp_bits_path):
                os.unlink(tmp_bits_path)
    
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
        
        # Read file data into memory
        bits_data = file.read()
        compressed_size = len(bits_data)
        
        # Validate the bits file format
        try:
            validate_bits_file(bits_data)
        except ValueError as e:
            return jsonify({'error': f'Invalid bits file: {str(e)}'}), 400
        
        # Decompress from bytes
        reconstructed = decompress_from_bytes(bits_data)
        
        # Extract image dimensions from the bits file header
        img_h, img_w = struct.unpack('2H', bits_data[:4])
        
        # Save reconstructed image to memory
        img_buffer = io.BytesIO()
        save_image(reconstructed, img_buffer, format='PNG')
        img_buffer.seek(0)
        img_data = base64.b64encode(img_buffer.read()).decode()
        
        return jsonify({
            'success': True,
            'compressed_size': compressed_size,
            'image_width': img_w,
            'image_height': img_h,
            'reconstructed_image': f"data:image/png;base64,{img_data}",
        })
    
    except struct.error as e:
        return jsonify({'error': f'Invalid bits file format: The file does not match the expected compression format. {str(e)}'}), 400
    except Exception as e:
        import traceback
        error_msg = str(e)
        # Provide more helpful error messages
        if 'pattern' in error_msg.lower() or 'unpack' in error_msg.lower():
            error_msg = 'Invalid bits file format: The file does not match the expected compression format. Please ensure you are uploading a valid .bits file created by this compression tool.'
        return jsonify({'error': error_msg}), 500

@app.route('/download/<filename>')
def download_file(filename):
    # This endpoint is kept for backward compatibility but files are now stored in memory
    # In a production app, you might want to implement a proper download mechanism
    return jsonify({'error': 'File download not available. Files are processed in memory.'}), 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Lossy-VAE Web Demo")
    print("="*50)
    print(f"Server starting on http://localhost:5000")
    print(f"Device: {device}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

