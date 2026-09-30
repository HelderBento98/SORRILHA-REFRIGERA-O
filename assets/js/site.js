/* Sorrilha Refrigeração — script do site
   1. Formulário: junta os campos numa mensagem e abre o WhatsApp.
   2. Origem: se o visitante veio de anúncio (gclid / fbclid / utm), a mensagem do WhatsApp diz de onde veio.
   3. Medição: conta cliques em WhatsApp, ligação e envio do formulário (Google Analytics, Google Ads, Meta).
   4. Aviso de cookies: só aparece quando a medição está ligada (códigos preenchidos em tools/conteudo.py).
   A configuração chega em window.SORRILHA, gerada pelo tools/build.py. */
(function () {
  'use strict';
  var CFG = window.SORRILHA || {};
  var CHAVE_CONSENT = 'sorrilha-consent';
  var CHAVE_ORIGEM = 'sorrilha-origem';

  function ler(store, k) { try { return window[store].getItem(k); } catch (e) { return null; } }
  function gravar(store, k, v) { try { window[store].setItem(k, v); } catch (e) { /* navegação privada */ } }

  /* ---------- 2. Origem do visitante ---------- */
  function descobreOrigem() {
    var q = new URLSearchParams(location.search);
    var src = q.get('utm_source'), camp = q.get('utm_campaign');
    if (src) return src + (camp ? ' / ' + camp : '');
    if (q.get('gclid') || q.get('gbraid') || q.get('wbraid')) return 'anúncio do Google';
    if (q.get('fbclid')) return 'Instagram/Facebook';
    return null;
  }
  var origem = descobreOrigem();
  if (origem) gravar('sessionStorage', CHAVE_ORIGEM, origem);
  else origem = ler('sessionStorage', CHAVE_ORIGEM);

  function marcaOrigem(texto) {
    if (!origem || texto.indexOf('(via ') !== -1) return texto;
    return texto.replace('Vim pelo site', 'Vim pelo site (via ' + origem + ')');
  }
  if (origem) {
    document.querySelectorAll('a[href^="https://wa.me/"]').forEach(function (a) {
      try {
        var u = new URL(a.href);
        var t = u.searchParams.get('text');
        /* monta na mão com encodeURIComponent: o WhatsApp mostra "+" literal se usar o formato de formulário */
        if (t) a.href = u.origin + u.pathname + '?text=' + encodeURIComponent(marcaOrigem(t));
      } catch (e) { /* link sem parâmetros */ }
    });
  }

  /* ---------- 3. Medição ---------- */
  var servico = document.body.getAttribute('data-servico') || 'inicio';
  function evento(tipo) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'generate_lead', { method: tipo, servico: servico });
      if (CFG.adsConversao) window.gtag('event', 'conversion', { send_to: CFG.adsConversao });
    }
    if (typeof window.fbq === 'function') window.fbq('track', 'Contact', { content_name: tipo, content_category: servico });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a');
    if (!a || a.hasAttribute('data-sem-evento')) return;
    var h = a.getAttribute('href') || '';
    if (h.indexOf('https://wa.me/') === 0) evento('whatsapp');
    else if (h.indexOf('tel:') === 0) evento('ligacao');
  }, true);

  /* ---------- 1. Formulário ---------- */
  document.querySelectorAll('.js-wa-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var linhas = [marcaOrigem('Olá, Gabriel! Vim pelo site.')];
      f.querySelectorAll('[data-campo]').forEach(function (c) {
        var v = c.value.trim(); if (v) linhas.push(c.getAttribute('data-campo') + ': ' + v);
      });
      evento('formulario');
      var a = document.createElement('a');
      a.href = 'https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent(linhas.join('\n'));
      a.target = '_blank'; a.rel = 'noopener'; a.setAttribute('data-sem-evento', '');
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* ---------- 4. Aviso de cookies e carregamento dos pixels ---------- */
  if (!CFG.rastreio) return;

  function carregaMeta() {
    if (!CFG.metaPixel || window.fbq) return;
    /* código padrão do Pixel da Meta */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', CFG.metaPixel);
    window.fbq('track', 'PageView');
  }

  function aplica(escolha) {
    var g = escolha === 'aceito' ? 'granted' : 'denied';
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', { ad_storage: g, ad_user_data: g, ad_personalization: g, analytics_storage: g });
    }
    if (escolha === 'aceito') carregaMeta();
  }

  var banner;
  function mostraAviso() {
    if (banner) { banner.hidden = false; return; }
    banner = document.createElement('div');
    banner.className = 'cookies';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Aviso de cookies');
    banner.innerHTML =
      '<p>Usamos cookies para medir as visitas e saber quais anúncios trazem clientes. ' +
      'Você escolhe. <a href="' + CFG.raiz + 'politica-de-privacidade/">Política de Privacidade</a></p>' +
      '<div class="cookies__btns">' +
      '<button type="button" class="btn btn--ghost btn--sm" data-escolha="recusado">Recusar</button>' +
      '<button type="button" class="btn btn--primary btn--sm" data-escolha="aceito">Aceitar</button></div>';
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-escolha]');
      if (!b) return;
      var escolha = b.getAttribute('data-escolha');
      gravar('localStorage', CHAVE_CONSENT, escolha);
      aplica(escolha);
      banner.hidden = true;
    });
    document.body.appendChild(banner);
  }

  var salvo = ler('localStorage', CHAVE_CONSENT);
  if (salvo === 'aceito') carregaMeta();
  if (!salvo) mostraAviso();
  document.querySelectorAll('.js-cookies').forEach(function (l) {
    l.hidden = false;
    l.addEventListener('click', function (e) { e.preventDefault(); mostraAviso(); });
  });
})();
