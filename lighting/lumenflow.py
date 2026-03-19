#!/usr/bin/env python3
"""LumenFlow Studio: a self-contained lighting control application.

This app is intentionally dependency-free so it runs with stock Python.
It provides:
- real-time fixture control and grouping
- cue recording and playback
- theatre-style timeline automation
- effect and pixel-mapping engines
- showfile persistence
- a built-in browser UI with tutorial/help content
"""

from __future__ import annotations

import argparse
import json
import math
import threading
import time
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
DEFAULT_SHOW_PATH = DATA_DIR / "demo_show.json"

Color = Tuple[int, int, int]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def clamp_color(color: Tuple[float, float, float]) -> Color:
    return tuple(int(clamp(c, 0, 255)) for c in color)  # type: ignore[return-value]


@dataclass
class Fixture:
    fixture_id: str
    label: str
    fixture_type: str
    universe: int
    address: int
    group: str
    x: float
    y: float
    z: float = 0.0
    intensity: int = 0
    color: Color = (255, 255, 255)
    pan: float = 0.0
    tilt: float = 0.0
    beam: int = 25
    shutter_open: bool = True
    selected: bool = False


@dataclass
class Cue:
    name: str
    fade_s: float
    follow_s: float
    notes: str
    fixture_states: Dict[str, Dict[str, Any]]


@dataclass
class TimelineEvent:
    at_s: float
    cue_name: str
    trigger: str = "timeline"


@dataclass
class Effect:
    name: str
    effect_type: str
    speed: float
    size: float
    spread: float
    color_a: Color = (255, 64, 64)
    color_b: Color = (64, 128, 255)
    enabled: bool = False


@dataclass
class Palette:
    name: str
    palette_type: str
    value: Any


@dataclass
class PixelMap:
    width: int = 16
    height: int = 8
    effect: str = "wave"
    speed: float = 1.0
    frame: List[List[Color]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.frame:
            self.frame = [[(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]


@dataclass
class ShowFile:
    name: str = "LumenFlow Demo"
    bpm: int = 120
    output_enabled: bool = False
    tutorial_seen: bool = False
    fixtures: Dict[str, Fixture] = field(default_factory=dict)
    cues: Dict[str, Cue] = field(default_factory=dict)
    timeline: List[TimelineEvent] = field(default_factory=list)
    effects: Dict[str, Effect] = field(default_factory=dict)
    palettes: Dict[str, Palette] = field(default_factory=dict)
    pixel_map: PixelMap = field(default_factory=PixelMap)


class LumenFlowEngine:
    def __init__(self) -> None:
        self.show = ShowFile()
        self.playhead_s = 0.0
        self.status_message = "Ready"
        self.lock = threading.RLock()
        self._playback_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    # -----------------------------
    # Show programming
    # -----------------------------
    def patch_fixture(
        self,
        fixture_id: str,
        label: str,
        fixture_type: str,
        universe: int,
        address: int,
        group: str,
        x: float,
        y: float,
        z: float = 0.0,
    ) -> None:
        with self.lock:
            self.show.fixtures[fixture_id] = Fixture(
                fixture_id=fixture_id,
                label=label,
                fixture_type=fixture_type,
                universe=universe,
                address=address,
                group=group,
                x=x,
                y=y,
                z=z,
            )
            self.status_message = f"Patched {fixture_id}"

    def patch_template_stage(self) -> None:
        template = [
            ("MH1", "Downstage Left Spot", "Moving Spot", 1, 1, "spots", -3.0, 3.0),
            ("MH2", "Downstage Right Spot", "Moving Spot", 1, 21, "spots", 3.0, 3.0),
            ("W1", "Warm Wash Left", "LED Wash", 1, 41, "wash", -2.0, 1.2),
            ("W2", "Warm Wash Right", "LED Wash", 1, 61, "wash", 2.0, 1.2),
            ("B1", "Back Beam Left", "Beam", 1, 81, "beam", -1.0, 4.0),
            ("B2", "Back Beam Right", "Beam", 1, 101, "beam", 1.0, 4.0),
        ]
        for item in template:
            self.patch_fixture(*item)
        self.status_message = "Loaded quick-start stage patch"

    def select_fixtures(self, fixture_ids: List[str]) -> None:
        with self.lock:
            for fixture in self.show.fixtures.values():
                fixture.selected = fixture.fixture_id in fixture_ids
            self.status_message = f"Selected {len(fixture_ids)} fixtures"

    def fixtures_in_group(self, group: str) -> List[Fixture]:
        return [f for f in self.show.fixtures.values() if f.group == group]

    def update_fixture(self, fixture_id: str, **changes: Any) -> None:
        with self.lock:
            fixture = self.show.fixtures[fixture_id]
            for key, value in changes.items():
                if key == "color":
                    value = clamp_color(tuple(value))
                if hasattr(fixture, key):
                    setattr(fixture, key, value)
            self.status_message = f"Updated {fixture_id}"

    def set_group_intensity(self, group: str, intensity: int) -> None:
        with self.lock:
            for fixture in self.fixtures_in_group(group):
                fixture.intensity = int(clamp(intensity, 0, 255))
            self.status_message = f"Set group '{group}' to {intensity}"

    def apply_palette(self, palette_name: str, fixture_ids: Optional[List[str]] = None) -> None:
        with self.lock:
            palette = self.show.palettes[palette_name]
            target_ids = fixture_ids or list(self.show.fixtures.keys())
            for fid in target_ids:
                if fid not in self.show.fixtures:
                    continue
                fixture = self.show.fixtures[fid]
                if palette.palette_type == "color":
                    fixture.color = tuple(palette.value)  # type: ignore[assignment]
                elif palette.palette_type == "position":
                    fixture.pan = float(palette.value["pan"])
                    fixture.tilt = float(palette.value["tilt"])
                elif palette.palette_type == "beam":
                    fixture.beam = int(palette.value)
            self.status_message = f"Applied palette '{palette_name}'"

    def record_cue(self, name: str, fade_s: float = 1.0, follow_s: float = 0.0, notes: str = "") -> None:
        with self.lock:
            fixture_states = {}
            for fid, fixture in self.show.fixtures.items():
                fixture_states[fid] = {
                    "intensity": fixture.intensity,
                    "color": list(fixture.color),
                    "pan": fixture.pan,
                    "tilt": fixture.tilt,
                    "beam": fixture.beam,
                    "shutter_open": fixture.shutter_open,
                }
            self.show.cues[name] = Cue(name, fade_s, follow_s, notes, fixture_states)
            self.status_message = f"Recorded cue '{name}'"

    def execute_cue(self, cue_name: str) -> None:
        with self.lock:
            cue = self.show.cues[cue_name]
            for fid, state in cue.fixture_states.items():
                if fid not in self.show.fixtures:
                    continue
                fixture = self.show.fixtures[fid]
                fixture.intensity = int(state["intensity"])
                fixture.color = tuple(state["color"])  # type: ignore[assignment]
                fixture.pan = float(state["pan"])
                fixture.tilt = float(state["tilt"])
                fixture.beam = int(state.get("beam", fixture.beam))
                fixture.shutter_open = bool(state.get("shutter_open", True))
            self.status_message = f"Executed cue '{cue_name}'"

    def add_timeline_event(self, at_s: float, cue_name: str, trigger: str = "timeline") -> None:
        with self.lock:
            if cue_name not in self.show.cues:
                raise KeyError(f"Unknown cue: {cue_name}")
            self.show.timeline.append(TimelineEvent(at_s, cue_name, trigger))
            self.show.timeline.sort(key=lambda event: event.at_s)
            self.status_message = f"Added timeline event for '{cue_name}' at {at_s:.1f}s"

    # -----------------------------
    # Effects / pixel mapping
    # -----------------------------
    def add_effect(
        self,
        name: str,
        effect_type: str,
        speed: float,
        size: float,
        spread: float,
        color_a: Color = (255, 64, 64),
        color_b: Color = (64, 128, 255),
        enabled: bool = False,
    ) -> None:
        with self.lock:
            self.show.effects[name] = Effect(name, effect_type, speed, size, spread, color_a, color_b, enabled)
            self.status_message = f"Created effect '{name}'"

    def set_effect_enabled(self, effect_name: str, enabled: bool) -> None:
        with self.lock:
            self.show.effects[effect_name].enabled = enabled
            self.status_message = f"Effect '{effect_name}' {'enabled' if enabled else 'disabled'}"

    def render_effects(self, t: float) -> None:
        with self.lock:
            fixtures = list(self.show.fixtures.values())
            for index, fixture in enumerate(fixtures):
                for effect in self.show.effects.values():
                    if not effect.enabled:
                        continue
                    phase = t * effect.speed + index * effect.spread
                    if effect.effect_type == "intensity_sine":
                        intensity = int((math.sin(phase) * 0.5 + 0.5) * effect.size)
                        fixture.intensity = int(clamp(intensity, 0, 255))
                    elif effect.effect_type == "color_chase":
                        mix = math.sin(phase) * 0.5 + 0.5
                        fixture.color = clamp_color(
                            tuple(
                                effect.color_a[c] * (1.0 - mix) + effect.color_b[c] * mix
                                for c in range(3)
                            )
                        )
                    elif effect.effect_type == "pan_tilt_circle":
                        fixture.pan = math.sin(phase) * effect.size
                        fixture.tilt = math.cos(phase) * effect.size
            self.status_message = "Effects rendered"

    def render_pixel_map(self, t: float) -> None:
        with self.lock:
            pixel_map = self.show.pixel_map
            for y in range(pixel_map.height):
                for x in range(pixel_map.width):
                    phase = (x * 0.5 + y * 0.35) + t * pixel_map.speed
                    if pixel_map.effect == "wave":
                        level = int((math.sin(phase) * 0.5 + 0.5) * 255)
                        pixel_map.frame[y][x] = (level, 100, 255 - level)
                    elif pixel_map.effect == "rainbow":
                        pixel_map.frame[y][x] = (
                            int((math.sin(phase) * 0.5 + 0.5) * 255),
                            int((math.sin(phase + 2.1) * 0.5 + 0.5) * 255),
                            int((math.sin(phase + 4.2) * 0.5 + 0.5) * 255),
                        )
                    else:
                        sparkle = 255 if (x + y + int(t * 8)) % 7 == 0 else 25
                        pixel_map.frame[y][x] = (sparkle, sparkle, sparkle)

    # -----------------------------
    # Playback and transport
    # -----------------------------
    def start_timeline(self, loop: bool = False, tick_s: float = 0.1) -> None:
        if self._playback_thread and self._playback_thread.is_alive():
            return
        self._stop_event.clear()

        def runner() -> None:
            while not self._stop_event.is_set():
                self.run_timeline(loop=loop, tick_s=tick_s)
                if not loop:
                    break

        self._playback_thread = threading.Thread(target=runner, daemon=True)
        self._playback_thread.start()
        self.status_message = "Timeline playback started"

    def stop_timeline(self) -> None:
        self._stop_event.set()
        self.status_message = "Timeline playback stopped"

    def run_timeline(self, loop: bool = False, tick_s: float = 0.1) -> None:
        with self.lock:
            events = list(self.show.timeline)
        if not events:
            self.status_message = "Timeline empty"
            return

        start = time.time()
        event_index = 0
        duration_s = max(event.at_s for event in events) + 0.5
        self.playhead_s = 0.0
        while not self._stop_event.is_set():
            now = time.time() - start
            self.playhead_s = now
            while event_index < len(events) and events[event_index].at_s <= now:
                self.execute_cue(events[event_index].cue_name)
                event_index += 1
            self.render_effects(now)
            self.render_pixel_map(now)
            if now >= duration_s:
                if loop:
                    start = time.time()
                    event_index = 0
                    self.playhead_s = 0.0
                else:
                    break
            time.sleep(tick_s)
        self.status_message = "Timeline reached end"

    def bump_playhead(self, seconds: float) -> None:
        self.playhead_s = float(clamp(self.playhead_s + seconds, 0.0, 36000.0))
        self.status_message = f"Playhead set to {self.playhead_s:.1f}s"

    # -----------------------------
    # Prebuilt tools / helpers
    # -----------------------------
    def create_default_palettes(self) -> None:
        with self.lock:
            self.show.palettes["Warm Amber"] = Palette("Warm Amber", "color", [255, 160, 60])
            self.show.palettes["Electric Blue"] = Palette("Electric Blue", "color", [80, 120, 255])
            self.show.palettes["Audience Blind"] = Palette("Audience Blind", "beam", 45)
            self.show.palettes["Singer Special"] = Palette("Singer Special", "position", {"pan": 0, "tilt": -18})
            self.status_message = "Loaded default palettes"

    def create_default_effects(self) -> None:
        self.add_effect("Pulse", "intensity_sine", speed=4.0, size=255, spread=0.6)
        self.add_effect("Color Chase", "color_chase", speed=2.0, size=255, spread=0.8)
        self.add_effect("Orbit", "pan_tilt_circle", speed=1.2, size=30, spread=0.7)
        self.status_message = "Loaded default effects"

    def create_default_cues(self) -> None:
        self.apply_palette("Warm Amber")
        self.set_group_intensity("wash", 170)
        self.set_group_intensity("spots", 110)
        self.set_group_intensity("beam", 90)
        self.record_cue("Intro", fade_s=2.5, notes="Warm front wash for walk-in")

        self.apply_palette("Electric Blue")
        self.set_group_intensity("beam", 255)
        self.set_group_intensity("spots", 220)
        self.record_cue("Drop", fade_s=0.5, notes="Big chorus hit")

        for fixture in self.show.fixtures.values():
            fixture.intensity = 0
        self.record_cue("Blackout", fade_s=1.0, notes="Clean end cue")

        self.add_timeline_event(0.0, "Intro")
        self.add_timeline_event(6.0, "Drop")
        self.add_timeline_event(11.0, "Blackout")
        self.status_message = "Built default cues and timeline"

    def reset_demo_show(self) -> None:
        with self.lock:
            self.show = ShowFile(name="LumenFlow Demo")
            self.playhead_s = 0.0
        self.patch_template_stage()
        self.create_default_palettes()
        self.create_default_effects()
        self.create_default_cues()
        self.show.output_enabled = True
        self.render_pixel_map(0.0)
        self.status_message = "Demo show restored"

    # -----------------------------
    # Persistence and views
    # -----------------------------
    def serialize(self) -> Dict[str, Any]:
        with self.lock:
            payload = asdict(self.show)
            payload["playhead_s"] = self.playhead_s
            payload["status_message"] = self.status_message
            payload["groups"] = sorted({fixture.group for fixture in self.show.fixtures.values()})
            payload["pixel_map_preview"] = [
                [sum(pixel) // 3 for pixel in row[: min(12, self.show.pixel_map.width)]]
                for row in self.show.pixel_map.frame[: min(4, self.show.pixel_map.height)]
            ]
            return payload

    def save(self, path: Path = DEFAULT_SHOW_PATH) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.serialize(), indent=2), encoding="utf-8")
        self.status_message = f"Saved show to {path.name}"

    def load(self, path: Path = DEFAULT_SHOW_PATH) -> None:
        raw = json.loads(path.read_text(encoding="utf-8"))
        show = ShowFile(
            name=raw.get("name", "Imported Show"),
            bpm=int(raw.get("bpm", 120)),
            output_enabled=bool(raw.get("output_enabled", False)),
            tutorial_seen=bool(raw.get("tutorial_seen", False)),
        )
        for fid, fixture_data in raw.get("fixtures", {}).items():
            show.fixtures[fid] = Fixture(**fixture_data)
        for cue_name, cue_data in raw.get("cues", {}).items():
            show.cues[cue_name] = Cue(**cue_data)
        show.timeline = [TimelineEvent(**event) for event in raw.get("timeline", [])]
        for effect_name, effect_data in raw.get("effects", {}).items():
            show.effects[effect_name] = Effect(**effect_data)
        for palette_name, palette_data in raw.get("palettes", {}).items():
            show.palettes[palette_name] = Palette(**palette_data)
        show.pixel_map = PixelMap(**raw.get("pixel_map", {}))
        self.show = show
        self.playhead_s = float(raw.get("playhead_s", 0.0))
        self.status_message = f"Loaded show from {path.name}"


class LumenFlowRequestHandler(BaseHTTPRequestHandler):
    server_version = "LumenFlowHTTP/1.0"

    @property
    def engine(self) -> LumenFlowEngine:
        return self.server.engine  # type: ignore[attr-defined]

    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        self._send(status, "application/json; charset=utf-8", json.dumps(payload).encode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            body = (STATIC_DIR / "index.html").read_bytes()
            self._send(200, "text/html; charset=utf-8", body)
            return
        if parsed.path.startswith("/static/"):
            asset = STATIC_DIR / parsed.path.removeprefix("/static/")
            if not asset.exists() or not asset.is_file():
                self._send_json({"error": "Not found"}, 404)
                return
            content_type = "text/plain; charset=utf-8"
            if asset.suffix == ".css":
                content_type = "text/css; charset=utf-8"
            elif asset.suffix == ".js":
                content_type = "application/javascript; charset=utf-8"
            elif asset.suffix == ".json":
                content_type = "application/json; charset=utf-8"
            self._send(200, content_type, asset.read_bytes())
            return
        if parsed.path == "/api/state":
            self.engine.render_pixel_map(time.time())
            self._send_json(self.engine.serialize())
            return
        if parsed.path == "/api/tutorial":
            tutorial = (BASE_DIR / "TUTORIAL.md").read_text(encoding="utf-8")
            self._send_json({"tutorial": tutorial})
            return
        self._send_json({"error": f"Unknown route {parsed.path}"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length) if length else b"{}"
        payload: Dict[str, Any]
        if "application/json" in self.headers.get("Content-Type", ""):
            payload = json.loads(raw_body or b"{}")
        else:
            payload = {k: v[0] for k, v in parse_qs(raw_body.decode("utf-8")).items()}

        try:
            if parsed.path == "/api/reset-demo":
                self.engine.reset_demo_show()
                self.engine.save()
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/save":
                self.engine.save()
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/load":
                self.engine.load()
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/cue/record":
                self.engine.record_cue(
                    payload["name"],
                    fade_s=float(payload.get("fade_s", 1.0)),
                    follow_s=float(payload.get("follow_s", 0.0)),
                    notes=str(payload.get("notes", "")),
                )
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/cue/go":
                self.engine.execute_cue(payload["name"])
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/timeline/add":
                self.engine.add_timeline_event(float(payload["at_s"]), payload["cue_name"])
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/timeline/start":
                self.engine.start_timeline(loop=bool(payload.get("loop", False)))
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/timeline/stop":
                self.engine.stop_timeline()
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/fixture/update":
                fixture_id = str(payload["fixture_id"])
                changes = {}
                if "intensity" in payload:
                    changes["intensity"] = int(payload["intensity"])
                if "pan" in payload:
                    changes["pan"] = float(payload["pan"])
                if "tilt" in payload:
                    changes["tilt"] = float(payload["tilt"])
                if "beam" in payload:
                    changes["beam"] = int(payload["beam"])
                if "color" in payload:
                    changes["color"] = payload["color"]
                self.engine.update_fixture(fixture_id, **changes)
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/group/intensity":
                self.engine.set_group_intensity(str(payload["group"]), int(payload["intensity"]))
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/palette/apply":
                self.engine.apply_palette(str(payload["name"]))
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/effect/toggle":
                self.engine.set_effect_enabled(str(payload["name"]), bool(payload["enabled"]))
                self.engine.render_effects(time.time())
                return self._send_json({"ok": True, "state": self.engine.serialize()})
            if parsed.path == "/api/pixel-map":
                self.engine.show.pixel_map.effect = str(payload.get("effect", "wave"))
                self.engine.show.pixel_map.speed = float(payload.get("speed", 1.0))
                self.engine.render_pixel_map(time.time())
                return self._send_json({"ok": True, "state": self.engine.serialize()})
        except Exception as exc:  # local request handling safeguard
            return self._send_json({"ok": False, "error": str(exc)}, status=500)

        self._send_json({"error": f"Unknown route {parsed.path}"}, 404)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


class LumenFlowHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: Tuple[str, int], engine: LumenFlowEngine):
        super().__init__(server_address, LumenFlowRequestHandler)
        self.engine = engine


def write_default_files_if_missing() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)


def run_cli_demo() -> None:
    engine = LumenFlowEngine()
    engine.reset_demo_show()
    engine.render_effects(0.5)
    engine.render_pixel_map(0.5)
    engine.save()
    state = engine.serialize()
    print("LumenFlow Studio CLI Demo")
    print("=" * 72)
    print(f"Show: {state['name']} | Fixtures: {len(state['fixtures'])} | Cues: {len(state['cues'])}")
    print(f"Effects: {', '.join(state['effects'].keys())}")
    print(f"Groups: {', '.join(state['groups'])}")
    print("Pixel Map Preview:")
    for row in state["pixel_map_preview"]:
        print(" ".join(f"{value:03}" for value in row))
    print(f"Status: {state['status_message']}")


def run_server(host: str, port: int) -> None:
    write_default_files_if_missing()
    engine = LumenFlowEngine()
    if DEFAULT_SHOW_PATH.exists():
        engine.load(DEFAULT_SHOW_PATH)
    else:
        engine.reset_demo_show()
        engine.save(DEFAULT_SHOW_PATH)
    httpd = LumenFlowHTTPServer((host, port), engine)
    print(f"LumenFlow Studio running on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        engine.save(DEFAULT_SHOW_PATH)
        httpd.server_close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LumenFlow Studio lighting controller")
    parser.add_argument("--serve", action="store_true", help="Run the browser UI server")
    parser.add_argument("--host", default="127.0.0.1", help="Host for the browser UI server")
    parser.add_argument("--port", type=int, default=8765, help="Port for the browser UI server")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.serve:
        run_server(args.host, args.port)
    else:
        run_cli_demo()


if __name__ == "__main__":
    main()
