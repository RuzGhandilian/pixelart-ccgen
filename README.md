
# pixelart-ccgen
Class-Conditional Pixel Art Generation (GAN vs Diffusion) @ 16×16, 8-color palette.

## Quickstart
```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows
# or: python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Open notebooks in this order:
- notebooks/00_data_overview.ipynb
- notebooks/01_prep_pipeline.ipynb
- notebooks/gan/10_gan_baseline.ipynb
- notebooks/diffusion/20_ddpm_baseline.ipynb
- notebooks/90_eval_compare.ipynb
