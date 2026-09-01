#!/usr/bin/env python3
import sys
import os
import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "161seconds")

def download_github_avatar(username=USERNAME, save_path="avatar.png"):
    url = f"https://github.com/{username}.png"
    print(f"[INFO] Fetching GitHub avatar from {url}...")
    resp = requests.get(url, headers={"User-Agent": "profile-bot/1.0"}, timeout=15)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(resp.content)
    print(f"[OK] Downloaded GitHub avatar ({len(resp.content):,} bytes) to {save_path}")
    return save_path

def prep(image_path=None, output_path="source-prepped.png"):
    try:
        import cv2
        import numpy as np
        from PIL import Image
    except ImportError as e:
        print(f"[ERR] Missing dependencies: {e}")
        print("Run: pip install pillow numpy opencv-python-headless")
        return False

    if not image_path or not os.path.exists(image_path):
        image_path = download_github_avatar()

    print(f"[INFO] Processing photo: {image_path}...")
    img = Image.open(image_path)

    # If rembg is available, remove background; otherwise handle alpha cleanly
    try:
        from rembg import remove
        print("[INFO] Applying rembg background removal...")
        nobg = remove(img)
    except Exception:
        nobg = img

    # Composite onto solid white background
    if nobg.mode == 'RGBA':
        bg = Image.new("RGB", nobg.size, (255, 255, 255))
        bg.paste(nobg, mask=nobg.split()[3])
        img_rgb = np.array(bg)
    else:
        img_rgb = np.array(nobg.convert("RGB"))

    # Grayscale & CLAHE contrast boost
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_gray)

    cv2.imwrite(output_path, img_clahe)
    print(f"[OK] Prepped photo saved as {output_path}")
    return True

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    prep(path)
