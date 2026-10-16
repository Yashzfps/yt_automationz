from __future__ import annotations

import hashlib
from pathlib import Path


def file_fingerprint(path: Path) -> str:
    stat = path.stat()
    digest = hashlib.sha256()
    digest.update(str(path.resolve()).encode("utf-8"))
    digest.update(str(stat.st_size).encode("utf-8"))
    digest.update(str(int(stat.st_mtime_ns)).encode("utf-8"))
    with path.open("rb") as f:
        head = f.read(65536)
        digest.update(head)
        if stat.st_size > 65536:
            f.seek(max(stat.st_size - 65536, 0))
            digest.update(f.read(65536))
    return digest.hexdigest()
