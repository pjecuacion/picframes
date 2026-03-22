from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

# TODO: Replace with the file extensions your app accepts as input.
SUPPORTED_EXTENSIONS = {".txt"}  # placeholder — update before shipping


class ProcessingError(Exception):
    pass


@dataclass(frozen=True)
class ProcessingOptions:
    # TODO: Add your app-specific processing options here.
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
    """Return all supported files under root."""
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
    """Map source files to destination paths."""
    jobs: list[ProcessingJob] = []
    for source in sources:
        if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        destination_dir = output_dir
        # TODO: uncomment if your app should mirror the source folder tree:
        # if source_root:
        #     destination_dir = output_dir / source.parent.relative_to(source_root)
        jobs.append(
            ProcessingJob(
                source=source,
                # TODO: update destination filename/extension to match your output format
                destination=destination_dir / source.name,
            )
        )
    return jobs


def process_single_job(job: ProcessingJob, options: ProcessingOptions) -> ProcessingResult:
    """Top-level picklable worker called by ProcessPoolExecutor.

    TODO: implement your actual file transformation here.
    """
    try:
        if job.destination.exists() and not options.overwrite:
            return ProcessingResult(job.source, job.destination, "skipped", "Destination exists")
        _process_file(job.source, job.destination, options)
        return ProcessingResult(job.source, job.destination, "processed")
    except Exception as exc:
        return ProcessingResult(job.source, job.destination, "failed", str(exc))


def _process_file(source: Path, destination: Path, options: ProcessingOptions) -> None:
    """TODO: implement your file transformation logic here."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError(
        "Replace _process_file() with your actual processing logic."
    )
