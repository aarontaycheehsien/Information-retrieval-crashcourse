"""Serve generated previews locally, with byte ranges for video playback."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re


class MediaHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.media_range = None
        path = Path(self.translate_path(self.path))
        if path.suffix.lower() != ".mp4" or not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        first, last = 0, size - 1
        requested = self.headers.get("Range")
        if requested:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested.strip())
            if not match or not any(match.groups()):
                self.send_error(416, "Unsupported byte range")
                return None
            start, end = match.groups()
            if start:
                first = int(start)
                last = min(int(end), size - 1) if end else size - 1
            else:
                first = max(0, size - int(end))
            if first > last or first >= size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
        handle = path.open("rb")
        handle.seek(first)
        self.media_range = last - first + 1
        self.send_response(206 if requested else 200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(self.media_range))
        if requested:
            self.send_header("Content-Range", f"bytes {first}-{last}/{size}")
        self.end_headers()
        return handle

    def copyfile(self, source, outputfile):
        try:
            if self.media_range is None:
                return super().copyfile(source, outputfile)
            remaining = self.media_range
            while remaining:
                block = source.read(min(65536, remaining))
                if not block:
                    break
                outputfile.write(block)
                remaining -= len(block)
        except (BrokenPipeError, ConnectionResetError):
            # Browsers routinely cancel a range when the viewer seeks.
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8770)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parents[2] / "outputs" / "promo-video")
    args = parser.parse_args()
    handler = partial(MediaHandler, directory=str(args.directory.resolve()))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Preview: http://127.0.0.1:{args.port}/preview.html", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
