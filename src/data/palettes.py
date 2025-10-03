
# Palette I/O & quantization helpers (8-color global palette).

def load_palette(path: str):
    raise NotImplementedError("Implement load_palette in src/data/palettes.py")

def quantize_image(rgb_image, palette):
    raise NotImplementedError("Implement quantize_image in src/data/palettes.py")
