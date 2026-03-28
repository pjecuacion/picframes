from __future__ import annotations

import logging
import os
import threading
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

from .processor import ProcessingJob, ProcessingOptions, ProcessingResult, process_single_job

_log = logging.getLogger(__name__)

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
    """Run jobs in a thread/process pool; progress and cancellation are managed on a daemon thread."""

    def _work() -> None:
        results: list[ProcessingResult] = []
        total = len(jobs)

        # When AI removal is active, use a single thread rather than a subprocess.
        # onnxruntime releases the GIL during inference so threading is effective,
        # and it avoids frozen-app DLL search-path issues in spawned subprocesses.
        # For non-AI jobs, use a process pool to parallelise CPU-bound work.
        if options.remove_bg:
            executor_cls = ThreadPoolExecutor
            max_workers = 1
        else:
            executor_cls = ProcessPoolExecutor
            max_workers = _WORKERS

        _log.info("executor=%s max_workers=%s jobs=%s remove_bg=%s",
                  executor_cls.__name__, max_workers, total, options.remove_bg)
        try:
            with executor_cls(max_workers=max_workers) as executor:
                futures = {executor.submit(process_single_job, job, options): job for job in jobs}
                completed = 0
                for future in as_completed(futures):
                    if cancel_event and cancel_event.is_set():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    completed += 1
                    try:
                        result = future.result()
                    except Exception as exc:
                        _log.error("Job failed with exception:\n%s", traceback.format_exc())
                        job = futures[future]
                        result = ProcessingResult(job.source, job.destination, "failed", str(exc))
                    results.append(result)
                    after_fn(0, lambda i=completed, t=total, r=result: on_progress(i, t, r))
        except Exception:
            _log.error("Executor crashed:\n%s", traceback.format_exc())
            raise

        after_fn(0, lambda r=results: on_finish(r, output_dir))

    threading.Thread(target=_work, daemon=True).start()
