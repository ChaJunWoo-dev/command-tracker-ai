import tempfile
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from src.config.constants import TempDir


class TempStorage:
    @asynccontextmanager
    async def job_dir(self, job_id: str) -> AsyncGenerator[Path, None]:
        path = Path(tempfile.mkdtemp(
            prefix=f"video-job-{job_id}-",
            dir=TempDir.BASE_DIR
        ))
        try:
            yield path
        finally:
            self._cleanup(path)

    @asynccontextmanager
    async def temp_file(self, suffix: str) -> AsyncGenerator[Path, None]:
        f = tempfile.NamedTemporaryFile(
            dir=TempDir.BASE_DIR,
            suffix=suffix,
            delete=False
        )
        f.close()
        path = Path(f.name)
        try:
            yield path
        finally:
            self._cleanup(path)

    def _cleanup(self, path: Path) -> None:
        try:
            if path.is_symlink() or path.is_file():
                path.unlink(missing_ok=True)
            elif path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
        except Exception:
            pass
