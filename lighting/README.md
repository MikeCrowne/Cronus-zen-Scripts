# LumenFlow Studio

LumenFlow Studio is a **fully functional, dependency-free lighting control application** designed to merge the strongest ideas from **Chamsys MagicQ**, **Obsidian Onyx**, **Show Buddy Active**, **MA Lighting MA3**, and **LightFactory** while improving speed, clarity, and usability.

## What it is now
This repository now includes a real working app, not just a concept prototype:
- A Python lighting engine with fixtures, palettes, effects, cues, timeline events, and pixel-mapping state.
- A browser UI served by Python's standard library.
- Persistent showfiles saved as JSON.
- A built-in tutorial for beginner onboarding.

## Core features

### Real-time control
- Direct fixture editing for intensity, pan, tilt, beam, and color.
- Group-based intensity control for fast operation.
- Palette application for repeatable looks.

### Visualization
- Live dashboard showing show status, fixtures, and timeline.
- Pixel-map preview built into the main screen.
- Stage data shown in a user-friendly card layout.

### Pixel mapping
- Integrated **Wave**, **Rainbow**, and **Sparkle** pixel looks.
- Adjustable pixel-map speed.
- Structured frame data stored in the showfile.

### Automation
- Cue recording and manual cue triggering.
- Theatre-style timeline transport with run/stop controls.
- Saved timeline events for repeatable playback.

### Effects and tools
- Built-in **Pulse**, **Color Chase**, and **Orbit** effects.
- Quick-start stage patch template.
- Default color, beam, and position palettes.
- Save/load demo show tools.

### Support and tutorial
- Included `TUTORIAL.md` quick-start guide.
- Plain-language interface labels.
- Beginner-friendly workflow with advanced building blocks.

## How to run

### CLI demo
```bash
python3 lighting/lumenflow.py
```

### Full app
```bash
python3 lighting/lumenflow.py --serve --host 127.0.0.1 --port 8765
```
Then open <http://127.0.0.1:8765> in your browser.

## Why it improves on the inspiration apps
- **Less mode confusion:** busking, theatre, and pixel workflows are presented together.
- **Faster onboarding:** users can load a complete demo rig instantly.
- **Clearer UI language:** more descriptive than traditional desk abbreviations.
- **Lower setup friction:** no external package install required.
- **Expandable architecture:** ready for future DMX/sACN/Art-Net, MIDI, and OSC support.

## Files
- `lighting/lumenflow.py`: engine + HTTP server.
- `lighting/static/index.html`: app UI.
- `lighting/static/styles.css`: styling.
- `lighting/static/app.js`: browser logic.
- `lighting/TUTORIAL.md`: quick-start and workflow help.
- `lighting/data/demo_show.json`: persistent saved show.
