#!/usr/bin/env python3
"""
Simple demo script for image compression using Lossy-VAE models.
Usage: python demo_compress.py <input_image> [--output <output_image>] [--lmb <lambda>] [--model <model_name>]
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
import torch
from torchvision.utils import save_image

from lvae import get_model


def main():
    parser = argparse.ArgumentParser(description='Compress and decompress an image using Lossy-VAE')
    parser.add_argument('input_image', type=str, help='Path to input image')
    parser.add_argument('--output', type=str, default=None, help='Path to save reconstructed image (default: input_name_reconstructed.png)')
    parser.add_argument('--lmb', type=float, default=None, help='Lambda value for compression (lower = more compression, higher = better quality). Default uses model default.')
    parser.add_argument('--model', type=str, default='qarv_base', help='Model name (default: qarv_base)')
    parser.add_argument('--bits-file', type=str, default=None, help='Path to save compressed bits file (default: input_name_compressed.bits)')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_image)
    if not input_path.exists():
        print(f"Error: Input image not found: {input_path}")
        sys.exit(1)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    print(f"Loading model: {args.model}")
    model = get_model(args.model, pretrained=True)
    model = model.to(device)
    model.eval()
    model.compress_mode(True)
    print("✅ Model loaded successfully!")
    
    output_path = Path(args.output) if args.output else input_path.parent / f"{input_path.stem}_reconstructed.png"
    bits_path = Path(args.bits_file) if args.bits_file else input_path.parent / f"{input_path.stem}_compressed.bits"
    
    print(f"\nCompressing image: {input_path}")
    print(f"Lambda: {args.lmb if args.lmb else 'default'}")
    
    model.compress_file(str(input_path), str(bits_path), lmb=args.lmb)
    
    original_size = input_path.stat().st_size
    compressed_size = bits_path.stat().st_size
    compression_ratio = original_size / compressed_size
    
    print(f"\nCompression stats:")
    print(f"  Original size: {original_size:,} bytes ({original_size/1024:.2f} KB)")
    print(f"  Compressed size: {compressed_size:,} bytes ({compressed_size/1024:.2f} KB)")
    print(f"  Compression ratio: {compression_ratio:.2f}x")
    
    img = Image.open(input_path)
    bpp = (compressed_size * 8) / (img.height * img.width)
    print(f"  Bits per pixel (BPP): {bpp:.4f}")
    
    print(f"\nDecompressing...")
    reconstructed = model.decompress_file(str(bits_path))
    
    save_image(reconstructed, str(output_path))
    print(f"✅ Reconstructed image saved to: {output_path}")
    print(f"✅ Compressed bits saved to: {bits_path}")
    
    print(f"\nYou can now:")
    print(f"  1. View the reconstructed image: {output_path}")
    print(f"  2. Share the compressed file: {bits_path}")
    print(f"  3. Decompress later using: model.decompress_file('{bits_path}')")


if __name__ == '__main__':
    main()

