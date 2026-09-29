/* Sorrilha Refrigeração — interações do site */
(function () {
  document.documentElement.classList.add('js');

  /* ---------- WhatsApp ----------
     Troque o número aqui e todos os botões do site mudam juntos.
     Formato: 55 + DDD + número, só dígitos. */
  var WHATSAPP = '5575999062183';

  var MENSAGENS = {
    geral:    'Olá, Gabriel! Vim pelo site e gostaria de um orçamento.',
    ar:       'Olá, Gabriel! Vim pelo site e preciso de serviço em ar-condicionado (instalação, limpeza ou conserto).',
    freezer:  'Olá, Gabriel! Vim pelo site e preciso de assistência em geladeira/freezer.',
    lavar:    'Olá, Gabriel! Vim pelo site e preciso de assistência/limpeza de máquina de lavar.',
    fogao:    'Olá, Gabriel! Vim pelo site e preciso de assistência em fogão.',
    reparos:  'Olá, Gabriel! Vim pelo site e preciso de um reparo em casa (tomada, lustre, encanamento...).',
    comercio: 'Olá, Gabriel! Vim pelo site. Tenho um comércio e preciso de atendimento em câmara fria/refrigeração.'
  };

  document.querySelectorAll('[data-wa]').forEach(function (el) {
    var msg = MENSAGENS[el.getAttribute('data-wa')] || MENSAGENS.geral;
    el.href = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(msg);
    el.target = '_blank';
    el.rel = 'noopener';
  });

  /* ---------- Menu mobile ---------- */
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav__toggle');
  var icon = toggle.querySelector('.ph');

  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    icon.className = 'ph ' + (open ? 'ph-x' : 'ph-list');
  }
  toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('is-open')); });
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    a.addEventListener('click', function () { setMenu(false); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* ---------- Sombra da navegação + botão flutuante ---------- */
  var fab = document.querySelector('.fab');
  var hero = document.querySelector('.hero');
  function onScroll() {
    var y = window.scrollY;
    nav.classList.toggle('is-scrolled', y > 8);
    fab.classList.toggle('is-visible', y > hero.offsetHeight * 0.6);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Revelar seções ao rolar ---------- */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Ano no rodapé ---------- */
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();
})();
