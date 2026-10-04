"""Content-addressed files are created exclusively and verified on every reuse."""
import os
from pathlib import Path

from services.data.contracts import DataError, digest


def archive(data, root):
    checksum = digest(data)
    path = Path(root) / checksum[:2] / (checksum + ".csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    except FileExistsError:
        if path.read_bytes() != data:
            raise DataError("archive_corrupt", checksum)
    else:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    if digest(path.read_bytes()) != checksum:
        raise DataError("archive_corrupt", checksum)
    return checksum, str(path.resolve())
