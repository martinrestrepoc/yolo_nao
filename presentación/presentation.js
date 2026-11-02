(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  const previous = document.getElementById('previous-button');
  const next = document.getElementById('next-button');
  const indexDialog = document.getElementById('index-dialog');
  const notesDialog = document.getElementById('notes-dialog');
  const helpDialog = document.getElementById('help-dialog');
  const announcer = document.getElementById('announcement');
  const indexNav = document.getElementById('slide-index');
  let current = 0;

  const indexLinks = slides.map((slide, i) => {
    const a = document.createElement('a');
    a.href = `#${i + 1}`;
    const number = document.createElement('span');
    number.textContent = String(i + 1).padStart(2, '0');
    a.append(number, document.createTextNode(slide.dataset.title));
    a.addEventListener('click', event => {
      event.preventDefault();
      indexDialog.close();
      goTo(i);
      document.getElementById('deck').focus({ preventScroll: true });
    });
    indexNav.appendChild(a);
    return a;
  });

  function updateNotes() {
    document.getElementById('notes-slide-title').textContent = `${current + 1}. ${slides[current].dataset.title}`;
    document.getElementById('notes-content').textContent = slides[current].querySelector('.speaker-notes')?.textContent || 'Esta diapositiva no tiene notas adicionales.';
  }
  function goTo(index, announce = true) {
    current = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => {
      const active = i === current;
      slide.classList.toggle('active', active);
      slide.hidden = !active;
      slide.inert = !active;
      if (active) slide.scrollTop = 0;
      indexLinks[i].setAttribute('aria-current', String(active));
    });
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    document.getElementById('slide-count').innerHTML = `${String(current + 1).padStart(2, '0')} <span>/ ${slides.length}</span>`;
    document.getElementById('section-name').textContent = slides[current].dataset.title;
    document.getElementById('progress-fill').style.width = `${(current + 1) / slides.length * 100}%`;
    history.replaceState(null, '', `#${current + 1}`);
    document.title = `${current + 1}/${slides.length} · ${slides[current].dataset.title} · YOLO26`;
    updateNotes();
    if (announce) announcer.textContent = `Diapositiva ${current + 1} de ${slides.length}: ${slides[current].dataset.title}`;
  }
  previous.addEventListener('click', () => goTo(current - 1));
  next.addEventListener('click', () => goTo(current + 1));
  document.getElementById('index-button').addEventListener('click', () => indexDialog.showModal());
  document.getElementById('notes-button').addEventListener('click', () => { updateNotes(); notesDialog.showModal(); });
  document.getElementById('help-button').addEventListener('click', () => helpDialog.showModal());
  document.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
  document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  }));
  async function toggleFullscreen() {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
    } catch {
      announcer.textContent = 'No se pudo activar pantalla completa. Puedes usar el menú de tu navegador.';
    }
  }
  const fullscreenButton = document.getElementById('fullscreen-button');
  fullscreenButton.disabled = !document.fullscreenEnabled;
  fullscreenButton.addEventListener('click', toggleFullscreen);
  document.addEventListener('fullscreenchange', () => fullscreenButton.setAttribute('aria-label', document.fullscreenElement ? 'Salir de pantalla completa' : 'Activar pantalla completa'));

  document.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey || document.querySelector('dialog[open]')) return;
    if (event.target.closest('input, select, textarea, [contenteditable=true]')) return;
    const key = event.key.toLowerCase();
    if (key === ' ' && event.target.closest('button, a')) return;
    if (['arrowright', 'arrowdown', ' ', 'pagedown'].includes(key)) { event.preventDefault(); goTo(current + 1); }
    else if (['arrowleft', 'arrowup', 'pageup'].includes(key)) { event.preventDefault(); goTo(current - 1); }
    else if (key === 'home') { event.preventDefault(); goTo(0); }
    else if (key === 'end') { event.preventDefault(); goTo(slides.length - 1); }
    else if (!event.repeat && key === 'i') indexDialog.showModal();
    else if (!event.repeat && key === 'n') { updateNotes(); notesDialog.showModal(); }
    else if (!event.repeat && key === 'f' && document.fullscreenEnabled) toggleFullscreen();
    else if (!event.repeat && key === 'p') { event.preventDefault(); window.print(); }
    else if (!event.repeat && key === '?') helpDialog.showModal();
  });
  window.addEventListener('hashchange', () => {
    const number = Number(location.hash.slice(1));
    if (Number.isInteger(number) && number >= 1 && number <= slides.length) goTo(number - 1);
  });
  let touchStart = null;
  document.getElementById('deck').addEventListener('touchstart', event => {
    if (event.target.closest('button, a')) return;
    touchStart = { x: event.changedTouches[0].clientX, y: event.changedTouches[0].clientY };
  }, { passive: true });
  document.getElementById('deck').addEventListener('touchend', event => {
    if (!touchStart) return;
    const dx = event.changedTouches[0].clientX - touchStart.x;
    const dy = event.changedTouches[0].clientY - touchStart.y;
    if (Math.abs(dx) > 80 && Math.abs(dx) > Math.abs(dy) * 1.8) goTo(current + (dx < 0 ? 1 : -1));
    touchStart = null;
  }, { passive: true });

  document.getElementById('copy-command').addEventListener('click', async () => {
    const command = document.getElementById('demo-command').textContent;
    const status = document.getElementById('copy-status');
    let copied = false;
    try {
      if (navigator.clipboard?.writeText) {
        await Promise.race([
          navigator.clipboard.writeText(command),
          new Promise((_, reject) => setTimeout(() => reject(new Error('clipboard-timeout')), 900)),
        ]);
        copied = true;
      }
    } catch { /* Usar copia compatible con apertura local. */ }
    if (!copied) {
      const field = document.createElement('textarea');
      field.value = command;
      field.setAttribute('aria-label', 'Comando de demostración');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      try { copied = document.execCommand('copy'); } catch { copied = false; }
      field.remove();
      document.getElementById('copy-command').focus();
    }
    status.textContent = copied
      ? 'Comando copiado. Pégalo en la terminal del proyecto.'
      : 'Selecciona el comando y cópialo manualmente para pegarlo en la terminal.';
  });

  const data = window.DECK_DATA;
  const NS = 'http://www.w3.org/2000/svg';
  function svgElement(type, attributes, text) {
    const element = document.createElementNS(NS, type);
    Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
    if (text !== undefined) element.textContent = text;
    return element;
  }
  function drawLineChart(container, series, domain, ticks, markBest) {
    const width = 560, height = 300;
    const margin = { left: 52, right: 18, top: 28, bottom: 42 };
    const x = epoch => margin.left + (epoch - 1) / 49 * (width - margin.left - margin.right);
    const y = value => height - margin.bottom - (value - domain[0]) / (domain[1] - domain[0]) * (height - margin.top - margin.bottom);
    const svg = svgElement('svg', { viewBox: `0 0 ${width} ${height}`, 'aria-hidden': 'true' });
    ticks.forEach(tick => {
      svg.appendChild(svgElement('line', { x1: margin.left, y1: y(tick), x2: width - margin.right, y2: y(tick), stroke: '#c9ccc1', 'stroke-width': 1 }));
      svg.appendChild(svgElement('text', { x: margin.left - 10, y: y(tick) + 5, 'text-anchor': 'end', fill: '#5f6b65', 'font-size': 15, 'font-family': 'Fira Sans, sans-serif' }, String(tick)));
    });
    [1, 10, 20, 30, 40, 50].forEach(epoch => svg.appendChild(svgElement('text', { x: x(epoch), y: height - 16, 'text-anchor': 'middle', fill: '#5f6b65', 'font-size': 15, 'font-family': 'Fira Sans, sans-serif' }, epoch)));
    series.forEach(({ key, color }) => {
      const path = data.epochs.map((row, i) => `${i ? 'L' : 'M'}${x(row.epoch).toFixed(2)},${y(row[key]).toFixed(2)}`).join(' ');
      svg.appendChild(svgElement('path', { d: path, fill: 'none', stroke: color, 'stroke-width': 2.7, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
    });
    if (markBest) {
      const best = data.epochs.reduce((a, b) => a.map > b.map ? a : b);
      svg.appendChild(svgElement('circle', { cx: x(best.epoch), cy: y(best.map), r: 5, fill: '#34634e', stroke: '#f4f1e9', 'stroke-width': 2 }));
      svg.appendChild(svgElement('text', { x: x(best.epoch) - 10, y: y(best.map) - 15, 'text-anchor': 'end', fill: '#34634e', 'font-size': 16, 'font-weight': 500, 'font-family': 'Fira Sans, sans-serif' }, `Mejor: época ${best.epoch}`));
    }
    svg.appendChild(svgElement('text', { x: width - 16, y: height - 1, 'text-anchor': 'end', fill: '#5f6b65', 'font-size': 12, 'font-family': 'Fira Sans, sans-serif' }, 'Época'));
    container.appendChild(svg);
  }
  if (data?.epochs?.length) {
    drawLineChart(document.getElementById('map-chart'), [{ key: 'map', color: '#34634e' }], [.65, .95], [.65, .75, .85, .95], true);
    drawLineChart(document.getElementById('loss-chart'), [{ key: 'trainBox', color: '#ad462b' }, { key: 'valBox', color: '#34634e' }], [0, 1.3], [0, .4, .8, 1.2], false);
  }
  function renderComparison(metric) {
    const container = document.getElementById('comparison-chart');
    container.replaceChildren();
    const label = metric === 'test' ? 'test' : 'validación';
    const values = data.models[metric];
    document.getElementById('gap-small').textContent = '+' + (values[0] - values[1]).toFixed(1);
    document.getElementById('gap-medium').textContent = '+' + (values[0] - values[2]).toFixed(1);
    document.getElementById('gap-small-label').textContent = `puntos frente a small en ${label}`;
    document.getElementById('gap-medium-label').textContent = `puntos frente a medium en ${label}`;
    ['Nano', 'Small', 'Medium'].forEach((name, i) => {
      const row = document.createElement('div'); row.className = 'bar-row';
      const model = document.createElement('span'); model.className = 'bar-name'; model.textContent = name;
      const track = document.createElement('div'); track.className = 'bar-track';
      const fill = document.createElement('div'); fill.className = 'bar-fill'; fill.style.width = `${values[i]}%`; track.appendChild(fill);
      const value = document.createElement('span'); value.className = 'bar-value'; value.textContent = `${values[i].toFixed(1)} %`;
      row.append(model, track, value); container.appendChild(row);
    });
    const axis = document.createElement('div'); axis.className = 'bar-axis';
    [0, 25, 50, 75, 100].forEach(value => { const label = document.createElement('span'); label.textContent = value; axis.appendChild(label); });
    const caption = document.createElement('p'); caption.className = 'bar-caption'; caption.textContent = `mAP50-95 de ${label} (%) · escala 0–100`;
    container.append(axis, caption);
    container.setAttribute('aria-label', `mAP50-95 de ${label}: nano ${values[0]} por ciento, small ${values[1]} por ciento, medium ${values[2]} por ciento.`);
    document.querySelectorAll('[data-metric]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.metric === metric)));
  }
  renderComparison('test');
  document.querySelectorAll('[data-metric]').forEach(button => button.addEventListener('click', () => {
    renderComparison(button.dataset.metric);
    announcer.textContent = document.getElementById('comparison-chart').getAttribute('aria-label');
  }));
  const initial = Number(location.hash.slice(1));
  goTo(Number.isInteger(initial) && initial >= 1 && initial <= slides.length ? initial - 1 : 0, false);
})();
