"""HTTP server for the step sequencer UI."""

from __future__ import annotations

import json
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from midi_beats.core.mutate import MutateKind
from midi_beats.library.parquet_store import PatternCatalog
from midi_beats.visualizer.pattern_bridge import (
    export_ui_pattern,
    generate_ui_pattern,
    mutate_slot,
    pattern_from_ui_state,
)
from midi_beats.visualizer.serialize import pattern_to_ui_payload

STATIC_DIR = Path(__file__).parent / "static"
DEFAULT_EXPORT_DIR = Path(__file__).resolve().parents[2] / "output" / "ui_export"


class VisualizerHandler(BaseHTTPRequestHandler):
    catalog: PatternCatalog | None = None
    export_dir: Path = DEFAULT_EXPORT_DIR

    def log_message(self, format, *args):
        pass

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
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

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_header()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/pattern":
            params = urllib.parse.parse_qs(parsed.query)
            genre = (params.get("genre") or ["house"])[0]
            seed = params.get("seed", [None])[0]
            seed_base = int(seed) if seed not in (None, "", "null") else None
            chain = (params.get("chain") or ["ABAC"])[0]
            catalog = self.catalog if genre == "house" else None
            payload = generate_ui_pattern(
                genre,
                seed_base=seed_base,
                chain_preset=chain,
                pattern_catalog=catalog,
            )
            self._send_json(payload)
            return

        if parsed.path in ("/", "/index.html"):
            self._send_file(STATIC_DIR / "index.html")
            return

        if parsed.path.startswith("/static/"):
            rel = parsed.path[len("/static/") :]
            self._send_file(STATIC_DIR / rel)
            return

        self.send_error(404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            body = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        if parsed.path == "/api/mutate":
            target = body.get("target", "B")
            kind_name = body.get("kind", "mini")
            kind = MutateKind(kind_name)
            try:
                payload = mutate_slot(body, target, kind)
                self._send_json(payload)
            except ValueError as e:
                self._send_json({"error": str(e)}, 400)
            return

        if parsed.path == "/api/export":
            out = body.get("output_dir") or str(self.export_dir)
            layout = body.get("layout", "both")
            try:
                result = export_ui_pattern(body, out, layout=layout)
                self._send_json({"ok": True, **result})
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        if parsed.path == "/api/pattern/sync":
            try:
                pattern = pattern_from_ui_state(body)
                self._send_json(pattern_to_ui_payload(pattern))
            except Exception as e:
                self._send_json({"error": str(e)}, 400)
            return

        self.send_error(404)


def run_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    catalog: PatternCatalog | None = None,
    export_dir: str | Path | None = None,
) -> None:
    VisualizerHandler.catalog = catalog
    if export_dir:
        VisualizerHandler.export_dir = Path(export_dir)
    DEFAULT_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), VisualizerHandler)
    print(f"Step sequencer UI: http://{host}:{port}/")
    print(f"MIDI export dir: {VisualizerHandler.export_dir}")
    server.serve_forever()
