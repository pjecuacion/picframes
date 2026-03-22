# Purpose: Unit tests for my_app.processor (core file processing logic)
# Expected behavior: job discovery, job building, and result structures work correctly
# Related: template/processor.py stub
# Preconditions: No external dependencies required for these structural tests

from __future__ import annotations

import tempfile
from pathlib import Path

from my_app.processor import (
    ProcessingJob,
    ProcessingOptions,
    ProcessingResult,
    SUPPORTED_EXTENSIONS,
    build_jobs,
    discover_files,
)


def test_supported_extensions_is_a_set_of_strings():
    assert isinstance(SUPPORTED_EXTENSIONS, set)
    assert all(ext.startswith(".") for ext in SUPPORTED_EXTENSIONS)


def test_discover_files_raises_on_missing_folder():
    from my_app.processor import ProcessingError
    try:
        discover_files(Path("/nonexistent/path/xyz"))
        assert False, "Expected ProcessingError"
    except ProcessingError:
        pass


def test_discover_files_raises_on_file_not_dir():
    from my_app.processor import ProcessingError
    with tempfile.NamedTemporaryFile(suffix=list(SUPPORTED_EXTENSIONS)[0], delete=False) as f:
        p = Path(f.name)
    try:
        discover_files(p)
        assert False, "Expected ProcessingError"
    except ProcessingError:
        pass


def test_build_jobs_returns_empty_for_unsupported_extension():
    sources = [Path("file.unsupported_xyz")]
    jobs = build_jobs(sources, Path("output"), ProcessingOptions())
    assert jobs == []


def test_processing_result_status_values():
    job = ProcessingJob(source=Path("a.txt"), destination=Path("b.txt"))
    result_ok = ProcessingResult(job.source, job.destination, "processed")
    result_skip = ProcessingResult(job.source, job.destination, "skipped")
    result_fail = ProcessingResult(job.source, job.destination, "failed", "some error")

    assert result_ok.status == "processed"
    assert result_skip.status == "skipped"
    assert result_fail.status == "failed"
    assert result_fail.message == "some error"


# TODO: Add tests for your actual _process_file() implementation once you port your logic.
# Example test shape:
#
# def test_my_transformation_produces_expected_output():
#     with tempfile.TemporaryDirectory() as tmp:
#         source = Path(tmp) / "input.txt"
#         source.write_text("hello", encoding="utf-8")
#         destination = Path(tmp) / "output.txt"
#         _process_file(source, destination, ProcessingOptions())
#         assert destination.read_text() == "HELLO"  # whatever your transform does
