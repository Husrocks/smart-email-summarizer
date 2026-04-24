from PIL import Image, ImageDraw

def create_icon(size, filename):
    img = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle with gradient-like look
    margin = size // 8
    draw.ellipse([margin, margin, size - margin, size - margin], fill=(99, 102, 241))
    
    # Draw a simple "S" or envelope shape
    inner_margin = size // 3
    draw.rectangle([inner_margin, inner_margin, size - inner_margin, size - inner_margin], fill=(255, 255, 255))
    
    img.save(filename)

import os
os.makedirs('extension/icons', exist_ok=True)
create_icon(16, 'extension/icons/icon16.png')
create_icon(48, 'extension/icons/icon48.png')
create_icon(128, 'extension/icons/icon128.png')
print("Icons created successfully.")
