
# FID/KID helpers (optional via torch-fidelity).

def compute_fid_kid(real_dir: str, fake_dir: str) -> tuple[float, float]:
    raise NotImplementedError("Implement compute_fid_kid in src/eval/fid_kid.py")
