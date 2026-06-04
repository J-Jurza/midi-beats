"""HTTP server for the step sequencer UI."""

from __future__ import annotations

import json
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from midi_beats.core.pattern_model import ChainPreset
from midi_beats.genres.registry import generate_pattern_for_genre, get_genre
from midi_beats.library.parquet_store import PatternCatalog
from midi_beats.visualizer.serialize import pattern_to_ui_payload

STATIC_DIR = Path(__file__).parent / "static"


class VisualizerHandler(BaseHTTPRequestHandler):
    catalog: PatternCatalog | None = None

    def log_message(self, format, *args):
        pass

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path) -> None:
        if not path.is_file():
            self.send_error(404)
            return
        content = path.read_bytes()
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/pattern":
            params = urllib.parse.parse_qs(parsed.query)
            genre = (params.get("genre") or ["house"])[0]
            seed = params.get("seed", [None])[0]
            seed_base = int(seed) if seed not in (None, "", "null") else None
            chain = (params.get("chain") or ["ABAC"])[0]
            var = int((params.get("variation") or ["1"])[0])

            kwargs = {
                "variation_index": var,
                "seed_base": seed_base,
                "chain_preset": chain,
            }
            if genre == "house" and self.catalog is not None:
                kwargs["pattern_catalog"] = self.catalog

            pattern = generate_pattern_for_genre(genre, **kwargs)
            pattern.tempo = get_genre(genre).default_tempo
            self._send_json(pattern_to_ui_payload(pattern))
            return

        if parsed.path in ("/", "/index.html"):
            self._send_file(STATIC_DIR / "index.html")
            return

        if parsed.path.startswith("/static/"):
            rel = parsed.path[len("/static/") :]
            self._send_file(STATIC_DIR / rel)
            return

        self.send_error(404)


def run_server(host: str = "127.0.0.1", port: int = 8765, catalog: PatternCatalog | None = None) -> None:
    VisualizerHandler.catalog = catalog
    server = ThreadingHTTPServer((host, port), VisualizerHandler)
    print(f"Step sequencer UI: http://{host}:{port}/")
    server.serve_forever()
