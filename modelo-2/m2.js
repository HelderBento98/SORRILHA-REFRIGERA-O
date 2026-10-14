/* Sorrilha Refrigeração — Modelo 2
   1. Painel de temperatura (troca número, cor e textos conforme o aparelho)
   2. Avaliações: carrossel de cards (script junto da seção, igual ao site atual)
   3. Conversa de exemplo que aparece mensagem por mensagem
   4. Formulário que abre o WhatsApp */
(function () {
  'use strict';
  var calmo = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. Painel ---------- */
  var dial = document.querySelector('.dial');
  var dados = JSON.parse(document.getElementById('leituras').textContent);
  var q = function (s) { return dial.querySelector(s); };
  var elNum = q('.dial__num'), elUnit = q('.dial__unit'), elLabel = q('.dial__label'),
      elFrase = q('.dial__frase'), elWa = q('.dial__wa'), elMore = q('.dial__more');
  var opts = Array.prototype.slice.call(dial.querySelectorAll('.dial__opt'));
  var atual = JSON.parse(dial.getAttribute('data-abertura')).v, raf;

  function escreve(v) { elNum.textContent = (v < 0 ? '−' : '') + Math.abs(Math.round(v)); }
  function conta(de, para) {
    cancelAnimationFrame(raf);
    if (calmo) { escreve(para); atual = para; return; }
    var t0 = performance.now(), dur = Math.min(1100, 500 + Math.abs(para - de) * 4);
    (function passo(t) {
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      atual = de + (para - de) * e; escreve(atual);
      if (k < 1) raf = requestAnimationFrame(passo); else atual = para;
    })(t0);
  }
  function escolhe(slug, foco) {
    var d = dados[slug];
    opts.forEach(function (b) {
      var on = b.getAttribute('data-s') === slug;
      b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1;
      if (on && foco) b.focus();
    });
    dial.style.setProperty('--cor', d.cor);
    elLabel.textContent = d.nome; elUnit.textContent = d.u; elFrase.textContent = d.frase;
    elWa.href = d.wa; elWa.firstChild.textContent = 'Chamar sobre ' + d.nome.toLowerCase();
    elMore.href = d.href;
    conta(atual, d.v);
  }
  opts.forEach(function (b, i) {
    b.addEventListener('click', function () { escolhe(b.getAttribute('data-s')); });
    b.addEventListener('keydown', function (e) {
      var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!n) return;
      e.preventDefault();
      escolhe(opts[(i + n + opts.length) % opts.length].getAttribute('data-s'), true);
    });
  });
  /* abertura: começa no calor de Sertãozinho e esfria até o ar-condicionado */
  var primeiro = opts[0].getAttribute('data-s');
  if (calmo) escolhe(primeiro); else setTimeout(function () { escolhe(primeiro); }, 900);

  /* ---------- 3. Conversa ---------- */
  var lista = document.querySelector('.phone__msgs');
  if (lista && !calmo && 'IntersectionObserver' in window) {
    var msgs = Array.prototype.slice.call(lista.children);
    lista.parentNode.classList.add('js-chat');
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return;
      io.disconnect();
      var t = 300;
      msgs.forEach(function (m) {
        if (m.classList.contains('msg--ele')) {
          var dig = document.createElement('li');
          dig.className = 'typing'; dig.setAttribute('aria-hidden', 'true'); dig.innerHTML = '<i></i><i></i><i></i>';
          setTimeout(function () { lista.insertBefore(dig, m); }, t);
          t += 900;
          setTimeout(function () { dig.remove(); m.classList.add('is-on'); }, t);
        } else {
          setTimeout(function () { m.classList.add('is-on'); }, t);
        }
        t += 650;
      });
    }, { threshold: 0.2 });
    io.observe(lista);
  }

  /* ---------- 4. Formulário ---------- */
  document.querySelectorAll('.js-form').forEach(function (f) {
    var err = f.querySelector('.form__err'), prob = f.querySelector('textarea');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!prob.value.trim()) { err.hidden = false; prob.setAttribute('aria-invalid', 'true'); prob.focus(); return; }
      err.hidden = true; prob.removeAttribute('aria-invalid');
      var linhas = ['Olá, Gabriel! Vim pelo site.'];
      f.querySelectorAll('[data-campo]').forEach(function (c) {
        var v = c.value.trim(); if (v) linhas.push(c.getAttribute('data-campo') + ': ' + v);
      });
      window.open('https://wa.me/' + window.SORRILHA_WA + '?text=' + encodeURIComponent(linhas.join('\n')), '_blank', 'noopener');
    });
  });
})();
