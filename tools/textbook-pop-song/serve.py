"""Serve the local song player with byte-range support for MP3 and WAV seeking."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import re


class AudioHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.remaining = None
        path = Path(self.translate_path(self.path))
        if not path.is_file() or path.suffix.lower() not in [".mp3",".wav"]:
            return super().send_head()
        size = path.stat().st_size
        first,last = 0,size-1
        requested = self.headers.get("Range")
        if requested:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)",requested.strip())
            if match and any(match.groups()):
                start,end = match.groups()
                if start:
                    first = int(start)
                    last = min(int(end),size-1) if end else size-1
                else:
                    first = max(0,size-int(end))
            else:
                first = size
            if first>=size or first>last:
                self.send_response(416)
                self.send_header("Content-Range",f"bytes */{size}")
                self.send_header("Content-Length","0")
                self.end_headers()
                return None
        file = path.open("rb")
        file.seek(first)
        self.remaining = last-first+1
        self.send_response(206 if requested else 200)
        self.send_header("Content-Type",self.guess_type(str(path)))
        self.send_header("Content-Length",str(self.remaining))
        self.send_header("Accept-Ranges","bytes")
        self.send_header("Cache-Control","no-store")
        if requested:
            self.send_header("Content-Range",f"bytes {first}-{last}/{size}")
        self.end_headers()
        return file

    def copyfile(self,source,outputfile):
        try:
            if self.remaining is None:
                return super().copyfile(source,outputfile)
            while self.remaining:
                block = source.read(min(65536,self.remaining))
                if not block:
                    break
                outputfile.write(block)
                self.remaining -= len(block)
        except (BrokenPipeError,ConnectionResetError):
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=8787)
    parser.add_argument("--directory",type=Path,default=Path(__file__).resolve().parents[2]/"outputs"/"textbook-pop-song")
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1",args.port),partial(AudioHandler,directory=str(args.directory.resolve())))
    print(f"Song player: http://127.0.0.1:{args.port}/preview.html",flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__=="__main__":
    main()
