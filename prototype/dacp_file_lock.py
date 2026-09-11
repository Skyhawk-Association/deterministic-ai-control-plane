from __future__ import annotations

import os
import time
from pathlib import Path
from types import TracebackType
from typing import IO


class LockTimeoutError(TimeoutError):
    pass


class InterProcessFileLock:
    """Small stdlib-only advisory exclusive lock that is released by the OS on crash."""

    def __init__(self, path: str | Path, *, timeout_seconds: float = 10.0, poll_seconds: float = 0.025):
        if timeout_seconds < 0:
            raise ValueError("timeout_seconds must be nonnegative")
        if poll_seconds <= 0:
            raise ValueError("poll_seconds must be positive")
        self.path = Path(path).expanduser().resolve()
        self.timeout_seconds = timeout_seconds
        self.poll_seconds = poll_seconds
        self._handle: IO[bytes] | None = None

    def _try_lock(self, handle: IO[bytes]) -> bool:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                return True
            except OSError:
                return False

        import fcntl

        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False

    def _unlock(self, handle: IO[bytes]) -> None:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            return

        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def acquire(self) -> "InterProcessFileLock":
        if self._handle is not None:
            raise RuntimeError("lock is already acquired by this instance")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = self.path.open("a+b")
        if handle.seek(0, os.SEEK_END) == 0:
            handle.write(b"0")
            handle.flush()
            os.fsync(handle.fileno())
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            if self._try_lock(handle):
                self._handle = handle
                return self
            if time.monotonic() >= deadline:
                handle.close()
                raise LockTimeoutError(f"timed out acquiring lock: {self.path}")
            time.sleep(self.poll_seconds)

    def release(self) -> None:
        handle = self._handle
        if handle is None:
            return
        self._handle = None
        try:
            self._unlock(handle)
        finally:
            handle.close()

    def __enter__(self) -> "InterProcessFileLock":
        return self.acquire()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.release()
