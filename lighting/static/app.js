const state = { show: null };

const $ = (selector) => document.querySelector(selector);
const toHex = (rgb) => `#${rgb.map((v) => Number(v).toString(16).padStart(2, '0')).join('')}`;
const fromHex = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));

async function post(url, payload = {}) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return response.json();
}

async function loadState() {
  const response = await fetch('/api/state');
  state.show = await response.json();
  render();
}

async function loadTutorial() {
  const response = await fetch('/api/tutorial');
  const data = await response.json();
  $('#tutorialContent').textContent = data.tutorial;
}

function renderSummary() {
  const show = state.show;
  $('#showSummary').innerHTML = [
    ['Show', show.name],
    ['Fixtures', Object.keys(show.fixtures).length],
    ['Cues', Object.keys(show.cues).length],
    ['Effects', Object.keys(show.effects).length],
  ].map(([label, value]) => `<div class="summary-card"><strong>${label}</strong><p>${value}</p></div>`).join('');
  $('#statusBadge').textContent = show.status_message;
}

function renderFixtures() {
  const fixtures = Object.values(state.show.fixtures);
  $('#fixtureSelect').innerHTML = fixtures.map((fixture) => `<option value="${fixture.fixture_id}">${fixture.fixture_id} · ${fixture.label}</option>`).join('');
  $('#groupSelect').innerHTML = state.show.groups.map((group) => `<option value="${group}">${group}</option>`).join('');
  $('#fixtureCards').innerHTML = fixtures.map((fixture) => `
    <div class="fixture-card">
      <strong>${fixture.fixture_id}</strong>
      <p>${fixture.label}</p>
      <p>${fixture.fixture_type} · ${fixture.group}</p>
      <p>Intensity ${fixture.intensity} · Pan ${fixture.pan.toFixed(0)} · Tilt ${fixture.tilt.toFixed(0)}</p>
    </div>
  `).join('');
  syncFixtureForm();
}

function syncFixtureForm() {
  const fixture = state.show.fixtures[$('#fixtureSelect').value] || Object.values(state.show.fixtures)[0];
  if (!fixture) return;
  $('#fixtureIntensity').value = fixture.intensity;
  $('#fixturePan').value = fixture.pan;
  $('#fixtureTilt').value = fixture.tilt;
  $('#fixtureBeam').value = fixture.beam;
  $('#fixtureColor').value = toHex(fixture.color);
}

function renderCues() {
  $('#cueButtons').innerHTML = Object.values(state.show.cues).map((cue) => `
    <button data-cue="${cue.name}" class="secondary cue-go">Go ${cue.name}</button>
  `).join('');
  document.querySelectorAll('.cue-go').forEach((button) => {
    button.addEventListener('click', async () => {
      await post('/api/cue/go', { name: button.dataset.cue });
      await loadState();
    });
  });
}

function renderTimeline() {
  $('#timelineList').innerHTML = state.show.timeline.map((event) => `
    <div class="timeline-event"><strong>${event.cue_name}</strong><p>${event.at_s.toFixed(1)}s · ${event.trigger}</p></div>
  `).join('');
}

function renderPalettes() {
  $('#paletteButtons').innerHTML = Object.values(state.show.palettes).map((palette) => `
    <button class="secondary palette-apply" data-palette="${palette.name}">${palette.name}</button>
  `).join('');
  document.querySelectorAll('.palette-apply').forEach((button) => {
    button.addEventListener('click', async () => {
      await post('/api/palette/apply', { name: button.dataset.palette });
      await loadState();
    });
  });
}

function renderEffects() {
  $('#effectToggles').innerHTML = Object.values(state.show.effects).map((effect) => `
    <label class="toggle-item">
      <span><strong>${effect.name}</strong><br><small>${effect.effect_type}</small></span>
      <input type="checkbox" data-effect="${effect.name}" ${effect.enabled ? 'checked' : ''}>
    </label>
  `).join('');
  document.querySelectorAll('[data-effect]').forEach((checkbox) => {
    checkbox.addEventListener('change', async () => {
      await post('/api/effect/toggle', { name: checkbox.dataset.effect, enabled: checkbox.checked });
      await loadState();
    });
  });
}

function renderPixelMap() {
  $('#pixelPreview').textContent = state.show.pixel_map_preview
    .map((row) => row.map((value) => value.toString().padStart(3, '0')).join(' '))
    .join('\n');
}

function render() {
  if (!state.show) return;
  renderSummary();
  renderFixtures();
  renderCues();
  renderTimeline();
  renderPalettes();
  renderEffects();
  renderPixelMap();
}

function bindEvents() {
  $('#fixtureSelect').addEventListener('change', syncFixtureForm);
  $('#applyFixture').addEventListener('click', async () => {
    await post('/api/fixture/update', {
      fixture_id: $('#fixtureSelect').value,
      intensity: Number($('#fixtureIntensity').value),
      pan: Number($('#fixturePan').value),
      tilt: Number($('#fixtureTilt').value),
      beam: Number($('#fixtureBeam').value),
      color: fromHex($('#fixtureColor').value),
    });
    await loadState();
  });
  $('#applyGroup').addEventListener('click', async () => {
    await post('/api/group/intensity', {
      group: $('#groupSelect').value,
      intensity: Number($('#groupIntensity').value),
    });
    await loadState();
  });
  $('#recordCue').addEventListener('click', async () => {
    await post('/api/cue/record', {
      name: $('#cueName').value,
      fade_s: Number($('#cueFade').value),
    });
    await loadState();
  });
  $('#timelineStart').addEventListener('click', async () => {
    await post('/api/timeline/start', { loop: false });
    await loadState();
  });
  $('#timelineStop').addEventListener('click', async () => {
    await post('/api/timeline/stop');
    await loadState();
  });
  $('#applyPixelMap').addEventListener('click', async () => {
    await post('/api/pixel-map', {
      effect: $('#pixelEffect').value,
      speed: Number($('#pixelSpeed').value),
    });
    await loadState();
  });
  $('#resetDemo').addEventListener('click', async () => {
    await post('/api/reset-demo');
    await loadState();
  });
  $('#saveShow').addEventListener('click', async () => {
    await post('/api/save');
    await loadState();
  });
  $('#loadShow').addEventListener('click', async () => {
    await post('/api/load');
    await loadState();
  });
}

bindEvents();
Promise.all([loadState(), loadTutorial()]);
setInterval(loadState, 2000);
