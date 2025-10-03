from pathlib import Path
import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_datasets(slug: str, out_dir: str = "data/raw", config_dir: str | None = None) -> str:
    if config_dir:
        os.environ["KAGGLE_CONFIG_DIR"] = str(Path(config_dir))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    api = KaggleApi()
    api.authenticate()  # uses C:\Users\<you>\.kaggle\kaggle.json
    api.dataset_download_files(slug, path=str(out), unzip=True)
    return str(out.resolve())
