import sys
import os

def prep(image_path, output_path="source-prepped.png"):
    try:
        import cv2
        import numpy as np
        from PIL import Image
        from rembg import remove
    except ImportError as e:
        print(f"[ERR] Missing dependencies: {e}")
        print("Run: pip install pillow numpy opencv-python-headless rembg")
        return False

    print(f"[INFO] Processing photo: {image_path}...")
    input_img = Image.open(image_path)
    nobg = remove(input_img)

    # Composite onto solid white background
    bg = Image.new("RGB", nobg.size, (255, 255, 255))
    if nobg.mode == 'RGBA':
        bg.paste(nobg, mask=nobg.split()[3])
    else:
        bg.paste(nobg)

    # Grayscale & CLAHE contrast boost
    img_gray = cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_gray)

    cv2.imwrite(output_path, img_clahe)
    print(f"[OK] Prepped photo saved as {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <path-to-photo.jpg>")
    else:
        prep(sys.argv[1])
