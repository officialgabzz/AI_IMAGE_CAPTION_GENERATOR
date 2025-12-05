# Example Images for Testing

This directory contains sample images for testing the AI Image Caption Generator.

## Adding Test Images

You can add your own test images here to try out the application. Supported formats:

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- BMP (.bmp)

## Quick Test

Once you have some images in this directory, you can test the captioner from the command line:

```bash
# From the project root
python -c "from src.captioner import caption_image; print(caption_image('examples/sample_images/your_image.jpg'))"
```

## Example Test Images

For quick testing, you can download free images from:

- Unsplash (https://unsplash.com)
- Pexels (https://pexels.com)
- Pixabay (https://pixabay.com)

Suggested test scenarios:
1. **Nature scenes** - landscapes, animals, plants
2. **Urban environments** - cities, streets, buildings
3. **People** - portraits, groups, activities
4. **Objects** - single items, collections
5. **Abstract** - patterns, textures, art

## Testing Tips

- Try images with different complexity levels
- Test with various resolutions and aspect ratios
- Compare results between BLIP and GIT models
- Test multilingual translation with different target languages
- Try edge cases: very dark/bright images, blurry photos, etc.
