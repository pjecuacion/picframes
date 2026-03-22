from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}


class ProcessingError(Exception):
    pass


_ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


@dataclass(frozen=True)
class ProcessingOptions:
    frame_shape: str = "circle"      # "circle" | "square" | "rounded_square"
    corner_radius_pct: int = 25      # 5–50, only used for rounded_square
    padding: int = 0                 # px of inset padding around subject
    remove_bg: bool = True
    output_format: str = "png"       # "png" | "ico"
    overwrite: bool = True


@dataclass(frozen=True)
class ProcessingJob:
    source: Path
    destination: Path


@dataclass(frozen=True)
class ProcessingResult:
    source: Path
    destination: Path
    status: str  # "processed" | "skipped" | "failed"
    message: str = ""


ProgressCallback = Callable[[int, int, ProcessingResult], None]


def discover_files(root: Path, recursive: bool = True) -> list[Path]:
    """Return all supported image files under root."""
    if not root.exists():
        raise ProcessingError(f"Input folder does not exist: {root}")
    if not root.is_dir():
        raise ProcessingError(f"Input path is not a folder: {root}")
    pattern = "**/*" if recursive else "*"
    return sorted(
        p for p in root.glob(pattern)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def build_jobs(
    sources: list[Path],
    output_dir: Path,
    options: ProcessingOptions,
    source_root: Path | None = None,
) -> list[ProcessingJob]:
    """Map source image files to destination paths (.png or .ico)."""
    ext = ".ico" if options.output_format == "ico" else ".png"
    jobs: list[ProcessingJob] = []
    for source in sources:
        if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        jobs.append(
            ProcessingJob(
                source=source,
                destination=output_dir / (source.stem + ext),
            )
        )
    return jobs


def process_single_job(job: ProcessingJob, options: ProcessingOptions) -> ProcessingResult:
    """Top-level picklable worker called by ProcessPoolExecutor."""
    try:
        if job.destination.exists() and not options.overwrite:
            return ProcessingResult(job.source, job.destination, "skipped", "Destination exists")
        _process_file(job.source, job.destination, options)
        return ProcessingResult(job.source, job.destination, "processed")
    except Exception as exc:
        return ProcessingResult(job.source, job.destination, "failed", str(exc))


def _process_file(source: Path, destination: Path, options: ProcessingOptions) -> None:
    from PIL import Image  # noqa: F401 — re-imported in helpers too
    img = Image.open(source).convert("RGBA")

    if options.remove_bg:
        from rembg import remove
        img = remove(img)

    img = _to_square(img)
    size = img.width

    if options.padding > 0:
        img = _apply_padding(img, options.padding)

    mask = _get_mask(options.frame_shape, size, options.corner_radius_pct)
    if mask is not None:
        img = _apply_mask(img, mask)

    destination.parent.mkdir(parents=True, exist_ok=True)
    if options.output_format == "ico":
        _save_ico(img, destination)
    else:
        img.save(destination, "PNG")


def _save_ico(img, destination: Path) -> None:
    """Save RGBA image as a multi-size ICO file."""
    from PIL import Image
    # Ensure the base image is at least 256×256 for best quality downsampling.
    base_size = max(img.width, 256)
    base = img.resize((base_size, base_size), Image.LANCZOS) if img.width < base_size else img
    # Filter to sizes no larger than the source to avoid upscaling artefacts.
    sizes = [(s, s) for (s, _) in _ICO_SIZES if s <= base_size]
    if not sizes:
        sizes = [(img.width, img.height)]
    base.save(destination, format="ICO", sizes=sizes)


def _to_square(img) -> object:
    """Center-crop the image to a square."""
    from PIL import Image
    w, h = img.width, img.height
    if w == h:
        return img
    short = min(w, h)
    left = (w - short) // 2
    top = (h - short) // 2
    return img.crop((left, top, left + short, top + short))


def _apply_padding(img, padding: int) -> object:
    """Shrink the subject within the canvas, adding transparent inset padding."""
    from PIL import Image
    size = img.width
    subject_size = size - 2 * padding
    if subject_size <= 0:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shrunken = img.resize((subject_size, subject_size), Image.LANCZOS)
    canvas.paste(shrunken, (padding, padding), shrunken)
    return canvas


def _get_mask(frame_shape: str, size: int, corner_radius_pct: int):
    """Return an 'L'-mode alpha mask image, or None for square (no masking)."""
    from PIL import Image, ImageDraw
    if frame_shape not in ("circle", "rounded_square"):
        return None
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    if frame_shape == "circle":
        draw.ellipse([0, 0, size - 1, size - 1], fill=255)
    else:  # rounded_square
        radius = max(1, int(size * corner_radius_pct / 100))
        draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return mask


def _apply_mask(img, mask) -> object:
    """Multiply the image's alpha channel by the mask."""
    from PIL import Image, ImageChops
    r, g, b, a = img.split()
    new_a = ImageChops.multiply(a, mask)
    return Image.merge("RGBA", (r, g, b, new_a))
