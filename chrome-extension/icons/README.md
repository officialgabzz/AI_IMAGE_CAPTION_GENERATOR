# Chrome Extension Icons

This directory should contain the extension icons in the following sizes:

- `icon16.png` - 16x16 pixels
- `icon48.png` - 48x48 pixels  
- `icon128.png` - 128x128 pixels

## Creating Icons

You can create simple placeholder icons using any image editor, or use the following approach:

1. Create a square canvas (128x128)
2. Add a simple icon representing an image/caption (e.g., a picture frame with "AI" text)
3. Use your brand colors (purple/blue gradient recommended)
4. Export in three sizes: 16x16, 48x48, 128x128

For a quick solution, you can use online tools like:
- Canva (free)
- Figma (free)
- GIMP (free, open-source)

Or generate programmatically with Python:

```python
from PIL import Image, ImageDraw, ImageFont

sizes = [16, 48, 128]
for size in sizes:
    img = Image.new('RGB', (size, size), '#6366f1')
    draw = ImageDraw.Draw(img)
    # Add simple shapes or text
    img.save(f'icon{size}.png')
```

## Temporary Placeholder

Until proper icons are created, Chrome will use a default icon. The extension will still function normally.
