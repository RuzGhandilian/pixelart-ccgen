
# Dataset and dataloader helpers for class-conditional training.

class PixelArtDataset:
    def __init__(self, root: str, labels_csv: str | None, image_size: int = 16, num_classes: int = 5):
        raise NotImplementedError("Implement PixelArtDataset in src/data/datasets.py")
