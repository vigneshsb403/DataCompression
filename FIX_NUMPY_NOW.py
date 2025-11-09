"""
IMMEDIATE FIX for NumPy compatibility error
Run this cell, then RESTART RUNTIME, then continue
"""

import subprocess
import sys

print("=" * 60)
print("FIXING NUMPY COMPATIBILITY ISSUE")
print("=" * 60)

print("\nStep 1: Installing numpy 1.26.4 (compatible with PyTorch)...")
result = subprocess.run(
    [sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'numpy==1.26.4'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ NumPy 1.26.4 installed successfully!")
else:
    print("⚠️  Installation had warnings (may still work)")
    if result.stderr:
        print(result.stderr[:200])

print("\n" + "=" * 60)
print("⚠️  CRITICAL: RESTART RUNTIME NOW!")
print("=" * 60)
print("\nColab: Runtime → Restart runtime")
print("Kaggle: Session → Restart Session")
print("\nAfter restarting, run your model loading cell again.")
print("=" * 60)

