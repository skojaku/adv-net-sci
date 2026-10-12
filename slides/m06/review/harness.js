(function () {
  var out = document.createElement('pre'); out.id = 'harness'; out.style.display = 'none';
  document.body.appendChild(out);
  var log = [];
  function w() { out.textContent = log.join('\n'); }
  window.addEventListener('error', function (e) { log.push('ERROR ' + e.message); w(); });
  window.addEventListener('unhandledrejection', function (e) { log.push('REJECT ' + e.reason); w(); });
  var q = new URLSearchParams(location.search);
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function txt(n) { return n ? n.textContent.replace(/\s+/g, ' ').trim() : null; }
  async function run() {
    await wait(1500);
    var onPower = location.hash === '#2';
    var stage = document.getElementById(onPower ? 'power-step' : 'katz-dial');
    var sec = stage.closest('section');
    log.push('slide ' + location.hash + ' stage ' + stage.id + ' mounted=' + stage.getAttribute('data-anim-mounted'));
    log.push('initial step=' + txt(stage.querySelector('[data-anim-step]')) + ' note=' + txt(stage.querySelector('[data-anim-note]')));
    if (onPower) {
      var n = +(q.get('n') || 5);
      for (var i = 0; i < n; i++) {
        stage.querySelector('[data-anim-next]').click();
        await wait(1200);
        var vals = Array.prototype.map.call(stage.querySelectorAll('.ps-val'), txt).join(' ');
        var rings = Array.prototype.map.call(stage.querySelectorAll('.ps-ring'), function (c) { return getComputedStyle(c).opacity; }).join('');
        log.push('click ' + (i + 1) + ': step=' + txt(stage.querySelector('[data-anim-step]')) + ' | ' + vals + ' | rank=' + txt(stage.querySelector('.ps-rank')) + ' | rings=' + rings + ' | note(' + txt(stage.querySelector('[data-anim-note]')).length + ')=' + txt(stage.querySelector('[data-anim-note]')));
      }
    } else {
      stage.querySelector('[data-anim-next]').click();
      await wait(800);
      var ks = (q.get('ks') || '0,50,90,100,101,120').split(',').map(Number);
      var track = stage.querySelector('.anim-track');
      for (var j = 0; j < ks.length; j++) {
        var r = track.getBoundingClientRect();
        var x = r.left + (ks[j] / 120) * r.width, y = r.top + r.height / 2;
        track.dispatchEvent(new PointerEvent('pointerdown', { clientX: x, clientY: y, bubbles: true, cancelable: true }));
        window.dispatchEvent(new PointerEvent('pointerup', { bubbles: true }));
        await wait(400);
        var fills = Array.prototype.map.call(stage.querySelectorAll('.kd-node'), function (c) { return c.style.fill.replace(/rgb\(|\)| /g, ''); });
        log.push('k=' + ks[j] + ': ' + txt(stage.querySelector('.kd-alpha')) + ' | share="' + txt(stage.querySelector('.kd-share')) + '" warn="' + txt(stage.querySelector('.kd-warn')) + '" knobLeft=' + stage.querySelector('.anim-knob').style.left + ' | fills ' + fills.slice(0, 2).join(' ; ') + ' .. ' + fills.slice(12, 14).join(' ; '));
      }
    }
    log.push('overflow section.scrollHeight-clientHeight = ' + (sec.scrollHeight - sec.clientHeight) + ' (' + sec.scrollHeight + '/' + sec.clientHeight + ')');
    var sr = stage.getBoundingClientRect();
    log.push('stage rect w=' + Math.round(sr.width) + ' h=' + Math.round(sr.height));
    log.push('DONE');
    w();
  }
  run();
})();
