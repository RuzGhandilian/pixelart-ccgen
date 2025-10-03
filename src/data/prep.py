# minimal preprocessing:
# - if in_dir has class folders, uses folder name as label
# - if in_dir is flat, uses one label "pixel"
# - outputs images to out_dir/images and a labels.csv (filename,label)

from pathlib import Path
from PIL import Image
import csv
import json

# pillow nearest (compat across versions)
try:
    RES_NEAREST = Image.NEAREST
except AttributeError:
    RES_NEAREST = Image.Resampling.NEAREST

# dither enums (compat)
try:
    DITHER_FS = Image.Dither.FLOYDSTEINBERG
    DITHER_NONE = Image.Dither.NONE
except AttributeError:
    DITHER_FS = Image.FLOYDSTEINBERG
    DITHER_NONE = 0

def _load_palette(path: str | None):
    if not path:
        return None
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    colors = data.get("colors", data) if isinstance(data, dict) else data

    rgb = []
    for c in colors[:256]:
        if isinstance(c, str):
            s = c.strip().lstrip("#")
            if len(s) == 3:  # "abc" -> "aabbcc"
                s = "".join(ch * 2 for ch in s)
            v = int(s, 16)
            rgb.append(((v >> 16) & 255, (v >> 8) & 255, v & 255))
        else:
            r, g, b = c
            rgb.append((int(r), int(g), int(b)))

    # flatten + pad to 256*3 for pillow palettes
    flat = []
    for r, g, b in rgb:
        flat += [r, g, b]
    flat += [0] * (256 * 3 - len(flat))
    return flat

def _quantize(img: Image.Image, flat_pal):
    if flat_pal is None:
        return img
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(flat_pal)
    q = img.convert("RGB").quantize(palette=pal_img, dither=DITHER_FS)
    return q.convert("RGB")

def prepare_dataset(in_dir: str, out_dir: str, size=(16, 16), palette_json: str | None = None) -> int:
    in_dir = Path(in_dir)
    out_dir = Path(out_dir)
    out_img = out_dir / "images"
    out_img.mkdir(parents=True, exist_ok=True)

    if not in_dir.exists():
        print(f"in_dir not found: {in_dir}")
        return 0

    pal = _load_palette(palette_json)
    rows = []
    exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    subdirs = [d for d in in_dir.iterdir() if d.is_dir()]
    if subdirs:
        # label = subfolder name
        for d in sorted(subdirs):
            label = d.name
            for p in sorted(d.rglob("*")):
                if p.suffix.lower() not in exts:
                    continue
                try:
                    im = Image.open(p).convert("RGBA").resize(size, RES_NEAREST).convert("RGB")
                    im = _quantize(im, pal)
                    name = f"{p.stem}_{label}.png"
                    im.save(out_img / name)
                    rows.append((name, label))
                except Exception:
                    pass
    else:
        # flat folder → single label
        label = "pixel"
        for p in sorted(in_dir.rglob("*")):
            if p.suffix.lower() not in exts:
                continue
            try:
                im = Image.open(p).convert("RGBA").resize(size, RES_NEAREST).convert("RGB")
                im = _quantize(im, pal)
                name = f"{p.stem}_{label}.png"
                im.save(out_img / name)
                rows.append((name, label))
            except Exception:
                pass

    with open(out_dir / "labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["filename", "label"])
        w.writerows(rows)

    print(f"done: {len(rows)} images -> {out_img.as_posix()}")
    return len(rows)

if __name__ == "__main__":
    # optional cli: python -m src.data.prep <in_dir> <out_dir> [palette.json]
    import sys
    if len(sys.argv) < 3:
        print("usage: python -m src.data.prep <in_dir> <out_dir> [palette.json]")
        raise SystemExit(2)
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    pal = sys.argv[3] if len(sys.argv) >= 4 else None
    prepare_dataset(in_dir, out_dir, size=(16, 16), palette_json=pal)
