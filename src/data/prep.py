
# Data preparation pipeline (resize to 16x16, dedupe, 8-color quantization).
# Expose: prepare_dataset(in_dir, out_dir, size=16, palette_json=None)

def prepare_dataset(in_dir: str, out_dir: str, size: int = 16, palette_json: str | None = None) -> None:
    raise NotImplementedError("Implement prepare_dataset in src/data/prep.py")
