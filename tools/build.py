# -*- coding: utf-8 -*-
"""
Gera o site estático da Sorrilha Refrigeração (HTML puro) a partir de tools/conteudo.py.

Uso:  python3 tools/build.py
Saída: index.html, <serviço>/index.html, sitemap.xml, robots.txt, 404.html
"""
import json
import os
import re
import sys
from datetime import date
from html import escape
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conteudo import (EMPRESA, SITE_URL, DEPOIMENTOS, GOOGLE_PERFIL, GOOGLE_NOTA, GOOGLE_TOTAL, MARCAS_TODAS, INICIO,  # noqa: E402
                      SERVICOS, OPCOES_FORM, OPCAO_POR_SERVICO)

E = EMPRESA
HOJE = date.today().isoformat()
VERSAO_CSS = "3"


def wa(msg):
    return "https://wa.me/%s?text=%s" % (E["whatsapp"], quote(msg, safe=""))


# Ícones que não existem no Phosphor, desenhados como SVG no mesmo traço.
# "fridge": Tabler Icons (MIT), https://tabler.io/icons
SVG_ICONES = {
    "fridge": ('<svg class="ph ico ico-fridge%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M5 5a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2l0 -14"/>'
               '<path d="M5 10h14"/><path class="ico-fridge__h1" d="M9 6v1"/><path class="ico-fridge__h2" d="M9 13v3"/></svg>'),
    # "wash": Tabler Icons (MIT). O tambor (círculo + água) fica num grupo separado para girar sozinho.
    "wash": ('<svg class="ph ico ico-wash%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M5 5a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2l0 -14"/>'
             '<path d="M8 6h.01"/><path d="M11 6h.01"/><path d="M14 6h2"/>'
             '<g class="ico-wash__drum"><path d="M8 14a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"/>'
             '<path d="M8 14c1.333 -.667 2.667 -.667 4 0c1.333 .667 2.667 .667 4 0"/></g></svg>'),
}


def ic(nome, extra=""):
    if nome in SVG_ICONES:
        return SVG_ICONES[nome] % ((" " + extra) if extra else "")
    return '<i class="ph ph-%s%s" aria-hidden="true"></i>' % (nome, (" " + extra) if extra else "")


def ext(href):
    return 'href="%s" target="_blank" rel="noopener"' % escape(href)


def jsonld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Dados estruturados (Google)
# ---------------------------------------------------------------------------
def ld_empresa():
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "@id": SITE_URL + "/#empresa",
        "name": E["nome"],
        "url": SITE_URL + "/",
        "image": SITE_URL + "/assets/img/og.jpg",
        "logo": SITE_URL + "/assets/img/logo.png",
        "telephone": E["telefone_link"],
        "address": {"@type": "PostalAddress", "addressLocality": E["cidade"], "addressRegion": E["uf"], "addressCountry": "BR"},
        "areaServed": {"@type": "City", "name": "%s - %s" % (E["cidade"], E["uf"])},
        "sameAs": [E["instagram"]],
        "description": INICIO["description"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Serviços",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["h1"], "url": "%s/%s/" % (SITE_URL, s["slug"])}}
                for s in SERVICOS
            ],
        },
    }


def ld_faq(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq],
    }


def ld_servico(s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["h1"],
        "serviceType": s["nome"],
        "description": s["description"],
        "url": "%s/%s/" % (SITE_URL, s["slug"]),
        "provider": {"@id": SITE_URL + "/#empresa"},
        "areaServed": {"@type": "City", "name": "%s - %s" % (E["cidade"], E["uf"])},
    }


def ld_breadcrumb(s):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": s["nome"], "item": "%s/%s/" % (SITE_URL, s["slug"])},
        ],
    }


# ---------------------------------------------------------------------------
# Partes comuns
# ---------------------------------------------------------------------------
def head(title, description, caminho, R, lds, keywords=""):
    url = SITE_URL + "/" + caminho
    kw = '\n  <meta name="keywords" content="%s">' % escape(keywords) if keywords else ""
    return """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">{kw}
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0f3550">
  <meta name="geo.region" content="BR-SP">
  <meta name="geo.placename" content="{cidade}">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="{nome}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{site}/assets/img/og.jpg">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" type="image/png" href="{R}assets/img/favicon.png">
  <link rel="apple-touch-icon" href="{R}assets/img/apple-touch-icon.png">
  <link rel="preload" href="{R}assets/fonts/outfit-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{R}assets/icons/icons.css">
  <link rel="stylesheet" href="{R}assets/css/site.css?v={v}">
  {lds}
</head>
<body>
  <a class="skip" href="#conteudo">Pular para o conteúdo</a>
  <span id="menu" class="menu-anchor" aria-hidden="true"></span>
  <div class="progress" aria-hidden="true"></div>
""".format(title=escape(title), desc=escape(description), kw=kw, url=escape(url), cidade=E["cidade"],
           nome=E["nome"], site=SITE_URL, R=R, v=VERSAO_CSS, lds="\n  ".join(jsonld(x) for x in lds))


def cabecalho(R, ativo=""):
    sub = "\n".join(
        '            <li><a href="{R}{slug}/"{cur}>{icone}<span><strong>{nome}</strong><small>{resumo}</small></span></a></li>'.format(
            R=R, slug=s["slug"], nome=s["nome"], resumo=escape(s["resumo"]), icone=ic(s["icone"]),
            cur=' aria-current="page"' if ativo == s["slug"] else "")
        for s in SERVICOS)
    return """
  <div class="topbar">
    <div class="wrap topbar__inner">
      <span>{ic_pin} Atendimento em {cidade} - {uf}</span>
      <span class="topbar__right">
        <a href="tel:{tel}">{ic_tel} {tel_ex}</a>
        <a {insta}>{ic_insta} {insta_u}</a>
      </span>
    </div>
  </div>

  <header class="nav">
    <div class="wrap nav__inner">
      <a href="{R}" class="nav__brand" aria-label="{nome}, página inicial">
        <img src="{R}assets/img/logo.png" alt="{nome}" width="806" height="200" fetchpriority="high">
      </a>

      <nav class="nav__links" aria-label="Principal">
        <div class="nav__drop">
          <a href="{R}#servicos" class="nav__droplabel">Serviços {ic_caret}</a>
          <ul class="nav__sub">
{sub}
          </ul>
        </div>
        <a href="{R}camara-fria/"{cur_cf}>Para comércios</a>
        <a href="{R}#duvidas">Dúvidas</a>
        <a href="{R}#contato">Fale conosco</a>
        <a class="btn btn--primary btn--sm nav__cta" {wa}>{ic_wa} Chamar no WhatsApp</a>
      </nav>

      <a class="nav__toggle nav__toggle--open" href="#menu" aria-label="Abrir menu">{ic_list}</a>
      <a class="nav__toggle nav__toggle--close" href="#fechar" aria-label="Fechar menu">{ic_x}</a>
    </div>
  </header>
""".format(ic_pin=ic("map-pin"), cidade=E["cidade"], uf=E["uf"], tel=E["telefone_link"], ic_tel=ic("phone"),
           tel_ex=E["telefone_exibicao"], insta=ext(E["instagram"]), ic_insta=ic("instagram-logo"),
           insta_u=E["instagram_usuario"], R=R, nome=E["nome"], ic_caret=ic("caret-down"), sub=sub,
           cur_cf=' aria-current="page"' if ativo == "camara-fria" else "",
           wa=ext(wa("Olá, Gabriel! Vim pelo site e gostaria de um orçamento.")), ic_wa=ic("whatsapp-logo"),
           ic_list=ic("list"), ic_x=ic("x"))


def formulario(form_id, marcado="Ar-condicionado", titulo="Descreva o problema", sub=""):
    ops = "\n".join('                <option%s>%s</option>' % (" selected" if o == marcado else "", escape(o)) for o in OPCOES_FORM)
    return """
        <form class="form js-wa-form" id="{fid}" action="https://wa.me/{num}" method="get" target="_blank" aria-labelledby="{fid}-t">
          <div class="form__head">
            <p class="form__title" id="{fid}-t">{ic_wa} {titulo}</p>
            {sub}
          </div>
          <div class="form__row">
            <div class="field">
              <label for="{fid}-nome">Seu nome</label>
              <input id="{fid}-nome" data-campo="Nome" type="text" autocomplete="name" placeholder="Ex.: Maria">
            </div>
            <div class="field">
              <label for="{fid}-bairro">Bairro</label>
              <input id="{fid}-bairro" data-campo="Bairro" type="text" autocomplete="address-level3" placeholder="Ex.: Centro">
            </div>
          </div>
          <div class="field">
            <label for="{fid}-servico">Tipo de serviço</label>
            <div class="select">
              <select id="{fid}-servico" data-campo="Serviço">
{ops}
              </select>
              {ic_caret}
            </div>
          </div>
          <div class="field">
            <label for="{fid}-problema">O que está acontecendo?</label>
            <textarea id="{fid}-problema" data-campo="Problema" name="text" rows="3" required minlength="8"
              placeholder="Ex.: Ar-condicionado Samsung 12.000 BTUs pingando água no quarto."></textarea>
          </div>
          <button class="btn btn--primary btn--lg form__submit" type="submit">{ic_send} Enviar pelo WhatsApp</button>
          <p class="form__note">Abre o WhatsApp com a mensagem pronta. Você confere antes de enviar.</p>
        </form>""".format(fid=form_id, num=E["whatsapp"], ic_wa=ic("whatsapp-logo"), titulo=escape(titulo),
                          sub=('<p class="form__sub">%s</p>' % escape(sub)) if sub else "", ops=ops,
                          ic_caret=ic("caret-down"), ic_send=ic("paper-plane-tilt"))


def faixa_marcas():
    itens = "".join('<li>%s</li>' % escape(m) for m in MARCAS_TODAS)
    return """
    <section class="brands" aria-labelledby="marcas-t">
      <div class="wrap brands__head">
        <h2 id="marcas-t" class="brands__title">Atendemos todas as marcas</h2>
        <p class="brands__note">Assistência técnica independente. Não somos assistência autorizada dos fabricantes.</p>
      </div>
      <div class="marquee" aria-label="Marcas atendidas">
        <ul class="marquee__track">{i}</ul>
        <ul class="marquee__track" aria-hidden="true">{i}</ul>
      </div>
    </section>""".format(i=itens)


def depoimentos(lista=None, perfil=None):
    """Cards de avaliações do Google. Com a lista vazia, a seção não aparece."""
    lista = DEPOIMENTOS if lista is None else lista
    perfil = GOOGLE_PERFIL if perfil is None else perfil
    if not lista:
        return ""
    cards = []
    for d in lista:
        n = max(1, min(5, int(d.get("estrelas", 5))))
        nome = d["nome"].strip()
        inicial = escape(nome[:1].upper())
        cards.append("""
          <li class="review">
            <div class="review__top">
              <span class="review__avatar" aria-hidden="true">{ini}</span>
              <span class="review__who"><strong>{nome}</strong><small>{q}</small></span>
            </div>
            <div class="review__stars" role="img" aria-label="{n} de 5 estrelas"><span>{cheias}</span><span class="review__off">{vazias}</span></div>
            <blockquote>{t}</blockquote>
            {src}
          </li>""".format(ini=inicial, nome=escape(nome), q=escape(d.get("quando", "")), n=n,
                           cheias="★" * n, vazias="★" * (5 - n), t=escape(d["texto"]),
                           src=('<a class="review__src" %s>Ver avaliação no Google %s</a>' % (ext(d["link"]), ic("arrow-up-right")))
                           if d.get("link") else '<p class="review__src">Avaliação no Google</p>'))
    link = ('<a class="btn btn--ghost" %s>Ver no Google %s</a>' % (ext(perfil), ic("arrow-up-right"))) if perfil else ""
    nota = ""
    if GOOGLE_NOTA and GOOGLE_TOTAL:
        nota = ('<span class="rating__n">%s</span><span class="rating__meta"><span class="rating__stars" aria-hidden="true">★★★★★</span>'
                '<small>%d avaliações no Google</small></span>') % (escape(str(GOOGLE_NOTA)), int(GOOGLE_TOTAL))
    return """
    <section class="section section--soft" id="avaliacoes" aria-labelledby="av-t">
      <div class="wrap">
        <div class="section__head section__head--row reveal">
          <div>
            <p class="eyebrow">Avaliações no Google</p>
            <h2 id="av-t">Quem já chamou a Sorrilha</h2>
          </div>
          <div class="rating">
            {nota}
            {link}
          </div>
        </div>
      </div>
      <div class="reviews-rail reveal">
        <ul class="reviews" tabindex="0" aria-label="Avaliações de clientes">{cards}
        </ul>
      </div>
    </section>""".format(nota=nota, link=link, cards="".join(cards))


def faq_html(faq, titulo="Dúvidas frequentes", sid="duvidas"):
    itens = "\n".join("""          <details class="faq__item">
            <summary>{p}<span class="faq__icon" aria-hidden="true"></span></summary>
            <p>{r}</p>
          </details>""".format(p=escape(p), r=escape(r)) for p, r in faq)
    return """
    <section class="section" id="{sid}" aria-labelledby="{sid}-t">
      <div class="wrap faq">
        <div class="faq__intro reveal">
          <p class="eyebrow">Dúvidas</p>
          <h2 id="{sid}-t">{titulo}</h2>
          <p class="section__sub">Não achou sua dúvida? Pergunte direto pelo WhatsApp.</p>
          <a class="link-arrow" {wa}>Perguntar no WhatsApp {ic}</a>
        </div>
        <div class="faq__list reveal">
{itens}
        </div>
      </div>
    </section>""".format(sid=sid, titulo=escape(titulo), itens=itens,
                         wa=ext(wa("Olá, Gabriel! Vim pelo site e tenho uma dúvida.")), ic=ic("arrow-right"))


def contato(R):
    return """
    <section class="contact" id="contato" aria-labelledby="contato-t">
      <div class="wrap contact__grid">
        <div class="contact__copy reveal">
          <p class="eyebrow eyebrow--light">Fale conosco</p>
          <h2 id="contato-t">Fale direto com quem faz o serviço.</h2>
          <p class="contact__lead">Quem responde e quem vai até você é o {resp}. Sem central de atendimento e sem intermediário.</p>
        </div>
        <ul class="channels reveal">
          <li><a class="channel" {wa}>{ic_wa}<span><small>WhatsApp</small><strong>{tel_ex}</strong></span>{arr}</a></li>
          <li><a class="channel" href="tel:{tel}">{ic_tel}<span><small>Ligar</small><strong>{tel_ex}</strong></span>{arr}</a></li>
          <li><a class="channel" {insta}>{ic_insta}<span><small>Instagram</small><strong>{insta_u}</strong></span>{arr}</a></li>
          <li><div class="channel channel--static">{ic_pin}<span><small>Área de atendimento</small><strong>{cidade} - {uf}</strong></span></div></li>
        </ul>
      </div>
    </section>""".format(resp=E["responsavel"], wa=ext(wa("Olá, Gabriel! Vim pelo site e gostaria de um orçamento.")),
                         ic_wa=ic("whatsapp-logo"), tel_ex=E["telefone_exibicao"], tel=E["telefone_link"],
                         ic_tel=ic("phone"), insta=ext(E["instagram"]), ic_insta=ic("instagram-logo"),
                         insta_u=E["instagram_usuario"], ic_pin=ic("map-pin"), cidade=E["cidade"], uf=E["uf"],
                         arr=ic("arrow-up-right", "channel__arr"))


def rodape(R):
    links = "\n".join('          <li><a href="%s%s/">%s</a></li>' % (R, s["slug"], escape(s["h1"])) for s in SERVICOS)
    return """
  <footer class="footer">
    <div class="wrap footer__grid">
      <div class="footer__brand">
        <img src="{R}assets/img/logo.png" alt="{nome}" width="806" height="200" loading="lazy" decoding="async">
        <p>Refrigeração, eletrodomésticos e pequenos reparos em {cidade} - {uf}. Assistência técnica independente, todas as marcas.</p>
      </div>
      <nav class="footer__col" aria-label="Serviços">
        <p class="footer__h">Serviços</p>
        <ul>
{links}
        </ul>
      </nav>
      <div class="footer__col">
        <p class="footer__h">Contato</p>
        <ul>
          <li>{resp}</li>
          <li><a href="tel:{tel}">{tel_ex}</a> (WhatsApp e ligação)</li>
          <li><a {insta}>{insta_u}</a></li>
          <li>{cidade} - {uf}</li>
        </ul>
      </div>
    </div>
    <div class="wrap footer__bottom">
      <p>© {ano} {nome}. Todos os direitos reservados.</p>
      <p>As marcas citadas pertencem aos seus fabricantes.</p>
    </div>
  </footer>

  <a class="fab" {wa} aria-label="Chamar no WhatsApp">{ic_wa}</a>

  <script>
    /* Junta os campos do formulário numa mensagem e abre o WhatsApp.
       Sem este script o formulário continua funcionando e envia só a descrição. */
    document.querySelectorAll('.js-wa-form').forEach(function (f) {{
      f.addEventListener('submit', function (e) {{
        e.preventDefault();
        var linhas = ['Olá, Gabriel! Vim pelo site.'];
        f.querySelectorAll('[data-campo]').forEach(function (c) {{
          var v = c.value.trim(); if (v) linhas.push(c.getAttribute('data-campo') + ': ' + v);
        }});
        var a = document.createElement('a');
        a.href = 'https://wa.me/{num}?text=' + encodeURIComponent(linhas.join('\\n'));
        a.target = '_blank'; a.rel = 'noopener';
        document.body.appendChild(a); a.click(); a.remove();
      }});
    }});
  </script>
</body>
</html>
""".format(R=R, nome=E["nome"], cidade=E["cidade"], uf=E["uf"], links=links, resp=E["responsavel"],
           tel=E["telefone_link"], tel_ex=E["telefone_exibicao"], insta=ext(E["instagram"]),
           insta_u=E["instagram_usuario"], ano=date.today().year,
           wa=ext(wa("Olá, Gabriel! Vim pelo site e gostaria de um orçamento.")), ic_wa=ic("whatsapp-logo"),
           num=E["whatsapp"])


def faixa_ondas():
    return """
      <div class="waves" aria-hidden="true">
        <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path class="waves__coral" d="M0,56 C260,112 520,18 820,40 C1080,60 1260,86 1440,48 L1440,120 L0,120 Z"/>
          <path class="waves__blue" d="M0,76 C300,118 560,44 860,62 C1110,76 1280,98 1440,72 L1440,120 L0,120 Z"/>
        </svg>
      </div>"""


def cta_final(msg):
    return """
    <section class="cta">
      <div class="wrap cta__inner reveal">
        <h2>Aparelho com defeito? Mande uma mensagem agora.</h2>
        <p>Conte o problema, mande uma foto e combine a visita.</p>
        <div class="cta__btns">
          <a class="btn btn--primary btn--lg" {wa}>{ic_wa} Chamar no WhatsApp</a>
          <a class="btn btn--ghost-light btn--lg" href="tel:{tel}">{ic_tel} {tel_ex}</a>
        </div>
      </div>
    </section>""".format(wa=ext(wa(msg)), ic_wa=ic("whatsapp-logo"), tel=E["telefone_link"], ic_tel=ic("phone"),
                         tel_ex=E["telefone_exibicao"])


# ---------------------------------------------------------------------------
# Página inicial
# ---------------------------------------------------------------------------
def pagina_inicio():
    R = ""
    I = INICIO
    servicos = "\n".join("""
          <li class="svc reveal">
            <a class="svc__link" href="{slug}/">
              <span class="svc__icon">{icone}</span>
              <span class="svc__body">
                <strong class="svc__name">{nome}</strong>
                <span class="svc__desc">{resumo}</span>
              </span>
              <span class="svc__arr">{arr}</span>
            </a>
          </li>""".format(slug=s["slug"], icone=ic(s["icone"]), nome=escape(s["nome"]), resumo=escape(s["resumo"]),
                          arr=ic("arrow-right")) for s in SERVICOS)

    corpo = """
  <main id="conteudo">
    <section class="hero">
      <div class="wrap hero__grid">
        <div class="hero__copy">
          <p class="eyebrow load" style="--d:0">{ic_pin} {cidade} - {uf}</p>
          <h1 class="hero__title load" style="--d:1">{h1}</h1>
          <p class="hero__sub load" style="--d:2">{sub}</p>
          <ul class="hero__points load" style="--d:3">
            <li>{ic_ok} Atendimento em domicílio</li>
            <li>{ic_ok} Todas as marcas</li>
            <li>{ic_ok} Casa e comércio</li>
          </ul>
          <div class="hero__ctas load" style="--d:4">
            <a class="btn btn--primary btn--lg" {wa}>{ic_wa} Chamar no WhatsApp</a>
            <a class="btn btn--ghost btn--lg" href="#servicos">Ver serviços</a>
          </div>
        </div>
        <div class="hero__form load" style="--d:3" id="orcamento">
{form}
        </div>
      </div>
{ondas}
    </section>

    <section class="section" id="servicos" aria-labelledby="servicos-t">
      <div class="wrap">
        <div class="section__head reveal">
          <p class="eyebrow">Serviços</p>
          <h2 id="servicos-t">O que a Sorrilha faz por você</h2>
        </div>
        <ul class="svcs">{servicos}
        </ul>
      </div>
    </section>
{depo}

    <section class="section section--flush-top" id="casa-e-comercio" aria-label="Casa e comércio">
      <div class="wrap duo">
        <article class="duo__card reveal">
          <p class="eyebrow">Para sua casa</p>
          <h2>Conforto e eletrodomésticos funcionando</h2>
          <p>Instalação e limpeza do ar-condicionado, conserto de geladeira, freezer, máquina de lavar e fogão, e os pequenos reparos que ficam esperando na lista.</p>
          <a class="link-arrow" href="#servicos">Ver todos os serviços {arr}</a>
        </article>
        <article class="duo__card duo__card--dark reveal">
          <p class="eyebrow eyebrow--light">Para seu comércio</p>
          <h2>Câmara fria parada é mercadoria perdida</h2>
          <p>Instalação, manutenção e conserto de câmaras frias, freezers e expositores para mercados, açougues, padarias e restaurantes.</p>
          <a class="link-arrow link-arrow--light" href="camara-fria/">Câmara fria para comércios {arr}</a>
        </article>
      </div>
    </section>

    <section class="section section--soft" id="como-funciona" aria-labelledby="como-t">
      <div class="wrap">
        <div class="section__head reveal">
          <p class="eyebrow">Como funciona</p>
          <h2 id="como-t">Do primeiro contato ao serviço feito</h2>
        </div>
        <ol class="steps">
          <li class="step reveal"><span class="step__n">1</span><h3>Você manda a mensagem</h3><p>Pelo WhatsApp ou pelo formulário. Uma foto ou vídeo do aparelho ajuda muito.</p></li>
          <li class="step reveal"><span class="step__n">2</span><h3>Combinamos a visita</h3><p>Você escolhe o melhor horário e o técnico vai até a sua casa ou o seu comércio.</p></li>
          <li class="step reveal"><span class="step__n">3</span><h3>Diagnóstico e orçamento</h3><p>O problema é avaliado no local e você recebe o valor antes do conserto.</p></li>
          <li class="step reveal"><span class="step__n">4</span><h3>Serviço resolvido</h3><p>O conserto é feito e o aparelho é testado na sua frente.</p></li>
        </ol>
      </div>
    </section>
{faq}
{contato}
  </main>
""".format(ic_pin=ic("map-pin"), cidade=E["cidade"], uf=E["uf"], h1=escape(I["h1"]), sub=escape(I["sub"]),
           ic_ok=ic("check-circle"), wa=ext(wa("Olá, Gabriel! Vim pelo site e gostaria de um orçamento.")),
           ic_wa=ic("whatsapp-logo"), form=formulario("f-inicio", titulo="Peça seu orçamento",
                                                      sub="Preencha e envie pelo WhatsApp."),
           ondas=faixa_ondas(), servicos=servicos,
           arr=ic("arrow-right"), depo=depoimentos(), faq=faq_html(I["faq"]), contato=contato(R))

    html = head(I["title"], I["description"], "", R, [ld_empresa(), ld_faq(I["faq"])],
                keywords="refrigeração Sertãozinho, ar-condicionado Sertãozinho, câmara fria Sertãozinho, "
                         "conserto de geladeira Sertãozinho, conserto de máquina de lavar Sertãozinho, conserto de fogão Sertãozinho")
    html += cabecalho(R) + corpo + rodape(R)
    return html


# ---------------------------------------------------------------------------
# Páginas de serviço
# ---------------------------------------------------------------------------
def pagina_servico(s):
    R = "../"
    faz = "\n".join('              <li>%s %s</li>' % (ic("check"), escape(x)) for x in s["faz"])
    probs = "\n".join('          <li><a class="chip" %s>%s</a></li>' % (
        ext(wa("Olá, Gabriel! Vim pelo site. %s: %s." % (s["nome"], p.lower()))), escape(p)) for p in s["problemas"])
    blocos = "\n".join("""
        <div class="prose__block reveal">
          <h2>{t}</h2>
          <p>{p}</p>
        </div>""".format(t=escape(t), p=escape(p)) for t, p in s["blocos"])
    marcas = ""
    if s["marcas"]:
        marcas = """
    <section class="section section--tight" aria-labelledby="m-t">
      <div class="wrap">
        <div class="brandlist reveal">
          <h2 id="m-t" class="brandlist__t">Marcas atendidas</h2>
          <ul>{m}</ul>
          <p class="brands__note">Assistência técnica independente. Não somos assistência autorizada dos fabricantes.</p>
        </div>
      </div>
    </section>""".format(m="".join("<li>%s</li>" % escape(x) for x in s["marcas"]))
    outros = "\n".join("""          <li><a class="other" href="../{slug}/">{icone}<span>{nome}</span>{arr}</a></li>""".format(
        slug=o["slug"], icone=ic(o["icone"]), nome=escape(o["nome"]), arr=ic("arrow-right")) for o in SERVICOS if o is not s)

    corpo = """
  <main id="conteudo">
    <section class="hero hero--page">
      <div class="wrap hero__grid hero__grid--page">
        <div class="hero__copy">
          <nav class="crumbs load" style="--d:0" aria-label="Você está em">
            <a href="../">Início</a> {ic_c} <span aria-current="page">{nome}</span>
          </nav>
          <h1 class="hero__title hero__title--page load" style="--d:1">{h1}</h1>
          <p class="hero__sub load" style="--d:2">{intro}</p>
          <div class="hero__ctas load" style="--d:3">
            <a class="btn btn--primary btn--lg" {wa}>{ic_wa} Chamar no WhatsApp</a>
            <a class="btn btn--ghost btn--lg" href="#orcamento">Descrever o problema</a>
          </div>
        </div>
        <aside class="scope load" style="--d:3" aria-label="O que fazemos">
          <p class="scope__t">{icone} O que fazemos</p>
          <ul>
{faz}
          </ul>
          <p class="scope__foot">{cidade} - {uf} · Atendimento no local</p>
        </aside>
      </div>
{ondas}
    </section>

    <section class="section" aria-labelledby="p-t">
      <div class="wrap">
        <div class="section__head reveal">
          <p class="eyebrow">Problemas que resolvemos</p>
          <h2 id="p-t">Reconhece algum destes?</h2>
          <p class="section__sub">Toque no problema e a mensagem vai pronta para o WhatsApp.</p>
        </div>
        <ul class="chips chips--solo reveal">
{probs}
        </ul>
      </div>
    </section>

    <section class="section section--soft section--tight-top" aria-label="Mais informações">
      <div class="wrap prose">{blocos}
      </div>
    </section>
{faq}

    <section class="section section--soft" id="orcamento" aria-labelledby="orc-t">
      <div class="wrap orc">
        <div class="orc__copy reveal">
          <p class="eyebrow">Orçamento</p>
          <h2 id="orc-t">Conte o que está acontecendo</h2>
          <p class="section__sub">Preencha e toque em enviar. O WhatsApp abre com a mensagem pronta para o {resp}.</p>
        </div>
        <div class="reveal">
{form}
        </div>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="o-t">
      <div class="wrap">
        <h2 id="o-t" class="others__t">Outros serviços em {cidade}</h2>
        <ul class="others">
{outros}
        </ul>
      </div>
    </section>
  </main>
""".format(ic_c=ic("caret-right"), nome=escape(s["nome"]), h1=escape(s["h1"]), intro=escape(s["intro"]),
           wa=ext(wa(s["wa"])), ic_wa=ic("whatsapp-logo"), icone=ic(s["icone"]), faz=faz, cidade=E["cidade"],
           uf=E["uf"], ondas=faixa_ondas(), probs=probs, blocos=blocos,
           faq=faq_html(s["faq"], "Dúvidas sobre " + s["nome"].lower(), "duvidas"),
           resp=E["responsavel"], form=formulario("f-" + s["slug"], OPCAO_POR_SERVICO[s["slug"]], "Descreva o problema"),
           outros=outros)

    html = head(s["title"], s["description"], s["slug"] + "/", R,
                [ld_servico(s), ld_breadcrumb(s), ld_faq(s["faq"])], keywords=s["keywords"])
    html += cabecalho(R, s["slug"]) + corpo + rodape(R)
    return html


def pagina_404():
    R = "/SORRILHA-REFRIGERA-O/" if "github.io" in SITE_URL else "/"
    corpo = """
  <main id="conteudo">
    <section class="hero hero--page">
      <div class="wrap">
        <p class="eyebrow">Erro 404</p>
        <h1 class="hero__title hero__title--page">Página não encontrada</h1>
        <p class="hero__sub">O endereço pode ter mudado. Volte para o início ou fale com a gente pelo WhatsApp.</p>
        <div class="hero__ctas">
          <a class="btn btn--primary btn--lg" href="{R}">Ir para o início</a>
          <a class="btn btn--ghost btn--lg" {wa}>Chamar no WhatsApp</a>
        </div>
      </div>
    </section>
  </main>
""".format(R=R, wa=ext(wa("Olá, Gabriel! Vim pelo site e gostaria de um orçamento.")))
    html = head("Página não encontrada | " + E["nome"], "Página não encontrada.", "404.html", R, [])
    html = html.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">')
    return html + cabecalho(R) + corpo + rodape(R)


# ---------------------------------------------------------------------------
def salvar(caminho, texto):
    completo = os.path.join(RAIZ, caminho)
    os.makedirs(os.path.dirname(completo), exist_ok=True)
    with open(completo, "w", encoding="utf-8") as f:
        f.write(texto)
    print("  gerado:", caminho)


def main():
    print("Gerando site em", RAIZ)
    salvar("index.html", pagina_inicio())
    for s in SERVICOS:
        salvar(os.path.join(s["slug"], "index.html"), pagina_servico(s))
    salvar("404.html", pagina_404())

    urls = [("", "1.0")] + [(s["slug"] + "/", "0.8") for s in SERVICOS]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join("  <url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (SITE_URL, u, HOJE, p)
                       for u, p in urls)
    sitemap += "</urlset>\n"
    salvar("sitemap.xml", sitemap)
    salvar("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)

    # lista de ícones usados (para gerar o subconjunto da fonte de ícones)
    usados = set()
    for raiz, _, arqs in os.walk(RAIZ):
        if "/.git" in raiz or "/tools" in raiz:
            continue
        for a in arqs:
            if a.endswith(".html"):
                usados |= set(re.findall(r"ph-([a-z0-9-]+)", open(os.path.join(raiz, a), encoding="utf-8").read()))
    with open(os.path.join(RAIZ, "tools", "icones-usados.txt"), "w") as f:
        f.write("\n".join(sorted(usados)) + "\n")
    print("  %d ícones usados" % len(usados))


if __name__ == "__main__":
    main()
