"""Seekable read-only file object backed by `rclone cat --offset/--count`.

Python's zipfile only needs seek() + read(). A ZIP's table of contents lives at the
END of the file, so listing an archive costs a few small range requests instead of
downloading it. Members can also be streamed (decompressed in memory) from here.
"""
import io
import subprocess

DRIVE_ARGS = ["--drive-shared-with-me", "-q"]


class RcloneRangeFile(io.RawIOBase):
    def __init__(self, remote_path, size, chunk=4 * 2**20, extra_args=DRIVE_ARGS):
        self.path = remote_path
        self.size = size
        self.chunk = chunk
        self.args = list(extra_args)
        self.pos = 0
        self.buf_start = 0
        self.buf = b""
        self.bytes_fetched = 0
        self.requests = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        else:
            self.pos = self.size + offset
        return self.pos

    def _fetch(self, start, count):
        cmd = ["rclone", "cat", self.path, "--offset", str(start), "--count", str(count), *self.args]
        for attempt in range(3):
            res = subprocess.run(cmd, capture_output=True)
            if res.returncode == 0 and len(res.stdout) == count:
                self.requests += 1
                self.bytes_fetched += count
                return res.stdout
        raise IOError(f"rclone range read failed {self.path} @{start}+{count}: "
                      f"{res.stderr.decode(errors='replace')[-300:]}")

    def read(self, n=-1):
        if self.pos >= self.size:
            return b""
        if n is None or n < 0:
            n = self.size - self.pos
        n = min(n, self.size - self.pos)
        end = self.pos + n
        if not (self.buf_start <= self.pos and end <= self.buf_start + len(self.buf)):
            start = self.pos
            count = max(n, self.chunk)
            # Reads near the end (ZIP directory lookups): grab the whole tail in one request.
            if start + count > self.size:
                start = max(0, self.size - count)
            count = min(count, self.size - start)
            self.buf, self.buf_start = self._fetch(start, count), start
        off = self.pos - self.buf_start
        data = self.buf[off:off + n]
        self.pos += len(data)
        return data

    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)


SERVE_URL = "http://127.0.0.1:8765"


def http_range(archive, start, end, base=SERVE_URL, retries=5):
    """Bytes [start, end] (inclusive) of an archive via the local `rclone serve http` (scripts/serve_drive.sh)."""
    import time
    import urllib.parse
    import urllib.request
    url = f"{base}/{urllib.parse.quote(archive)}"
    err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                if r.status == 206 and len(data) == end - start + 1:
                    return data
                err = f"status {r.status}, got {len(data)} bytes"
        except Exception as e:
            err = repr(e)
        time.sleep(2 ** attempt)
    raise IOError(f"range read failed {archive} @{start}-{end}: {err}")


class HttpRangeFile(RcloneRangeFile):
    """Same as RcloneRangeFile but one long-lived rclone server instead of a process per read (~7s faster each)."""

    def __init__(self, archive, size, chunk=2**20):
        super().__init__(archive, size, chunk=chunk)

    def _fetch(self, start, count):
        data = http_range(self.path, start, start + count - 1)
        self.requests += 1
        self.bytes_fetched += count
        return data
