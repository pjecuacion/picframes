from __future__ import annotations

import os
import threading
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

from .processor import ProcessingJob, ProcessingOptions, ProcessingResult, process_single_job

ProgressCallback = Callable[[int, int, ProcessingResult], None]
FinishCallback = Callable[[list[ProcessingResult], Path], None]

_WORKERS = os.cpu_count() or 1


def run_jobs(
    jobs: list[ProcessingJob],
    options: ProcessingOptions,
    output_dir: Path,
    after_fn: Callable,
    on_progress: ProgressCallback,
    on_finish: FinishCallback,
    cancel_event: threading.Event | None = None,
) -> None:
    """Run jobs in a process pool; progress and cancellation are managed on a daemon thread."""

    def _work() -> None:
        results: list[ProcessingResult] = []
        total = len(jobs)

        with ProcessPoolExecutor(max_workers=_WORKERS) as executor:
            futures = {executor.submit(process_single_job, job, options): job for job in jobs}
            completed = 0
            for future in as_completed(futures):
                if cancel_event and cancel_event.is_set():
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                completed += 1
                result = future.result()
                results.append(result)
                after_fn(0, lambda i=completed, t=total, r=result: on_progress(i, t, r))

        after_fn(0, lambda r=results: on_finish(r, output_dir))

    threading.Thread(target=_work, daemon=True).start()
