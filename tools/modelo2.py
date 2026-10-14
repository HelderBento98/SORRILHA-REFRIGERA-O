# -*- coding: utf-8 -*-
"""
Modelo 2 da página inicial (proposta de redesenho, para comparar com o site atual).
Usa os mesmos textos de tools/conteudo.py. Gera modelo-2/index.html.

    python3 tools/modelo2.py

Ideia central: as cores da marca viram temperatura. Azul é frio, coral é quente.
Cada serviço tem o "número" que importa para ele (4 °C na geladeira, −18 °C na câmara fria,
180 °C no forno...), e o painel do topo muda de número e de cor conforme o serviço escolhido.
"""
import json
import os
from html import escape
from urllib.parse import quote

from conteudo import EMPRESA, INICIO, SERVICOS, DEPOIMENTOS, GOOGLE_PERFIL, MARCAS_TODAS, OPCOES_FORM

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "modelo-2", "index.html")

# O número de cada serviço: valor, unidade, cor do painel e uma frase que explica o número.
LEITURA = {
    "ar-condicionado": (23, "°C", "#1d74a0", "Entre 22 e 24 °C o ambiente fica confortável e o aparelho gasta menos luz."),
    "camara-fria": (-18, "°C", "#0f3550", "Congelados se conservam a −18 °C ou menos. Se a câmara não chega lá, a mercadoria corre risco."),
    "geladeira-e-freezer": (4, "°C", "#1f6593", "Uma geladeira bem regulada fica perto de 4 °C. Acima disso, a comida estraga mais rápido."),
    "maquina-de-lavar": (700, "rpm", "#35566c", "É mais ou menos a rotação da centrifugação. Quando o cesto não chega lá, a roupa sai encharcada."),
    "fogao": (180, "°C", "#c93a33", "A temperatura de quase toda receita de bolo. Forno que não chega nela precisa de conserto."),
    "reparos-em-casa": (127, "V", "#2b3d4c", "Tomadas, interruptores, lustres e vazamentos. Serviço pequeno, feito com a energia desligada."),
}

ABERTURA = (34, "°C", "#c93a33", "Tarde de verão em Sertãozinho")


def wa(msg):
    return "https://wa.me/%s?text=%s" % (EMPRESA["whatsapp"], quote(msg, safe=""))


def ic(nome):
    return '<i class="ph ph-%s" aria-hidden="true"></i>' % nome


def num(v):
    return ("−%d" % abs(v)) if v < 0 else str(v)


WA_GERAL = wa("Olá, Gabriel! Vim pelo site e gostaria de um orçamento.")


def cabecalho():
    return """
<header class="top">
  <nav class="top__bar" aria-label="Principal">
    <a class="top__logo" href="#inicio"><img src="../assets/img/logo.png" alt="Sorrilha Refrigeração" width="170" height="42"></a>
    <ul class="top__links">
      <li><a href="#servicos">Serviços</a></li>
      <li><a href="#avaliacoes">Avaliações</a></li>
      <li><a href="#como-funciona">Como funciona</a></li>
      <li><a href="#duvidas">Dúvidas</a></li>
    </ul>
    <a class="pill pill--wa top__cta" href="%s" target="_blank" rel="noopener">WhatsApp<span class="pill__ico">%s</span></a>
  </nav>
</header>""" % (WA_GERAL, ic("whatsapp-logo"))


def painel():
    # botões do seletor
    botoes = []
    dados = {}
    for s in SERVICOS:
        v, u, cor, frase = LEITURA[s["slug"]]
        dados[s["slug"]] = {"v": v, "u": u, "cor": cor, "frase": frase, "nome": s["nome"],
                            "resumo": s["resumo"], "href": "../%s/" % s["slug"], "wa": wa(s["wa"])}
        botoes.append('<button type="button" class="dial__opt" role="tab" aria-selected="false" data-s="%s">%s</button>'
                      % (s["slug"], escape(s["nome"])))
    v, u, cor, rotulo = ABERTURA
    primeiro = SERVICOS[0]
    return """
<div class="dial" style="--cor:%s" data-abertura='%s'>
  <div class="dial__screen" aria-live="polite">
    <p class="dial__label">%s</p>
    <p class="dial__read"><span class="dial__num">%s</span><span class="dial__unit">%s</span></p>
    <p class="dial__frase">Lá fora o sol aperta. Do lado de dentro, a temperatura certa depende do aparelho.</p>
    <div class="dial__acts">
      <a class="pill pill--light dial__wa" href="%s" target="_blank" rel="noopener">Chamar sobre %s<span class="pill__ico">%s</span></a>
      <a class="dial__more" href="%s">Ver o serviço</a>
    </div>
  </div>
  <div class="dial__opts" role="tablist" aria-label="Escolha o aparelho">%s</div>
</div>
<script type="application/json" id="leituras">%s</script>""" % (
        cor, json.dumps({"v": v, "u": u, "cor": cor, "rotulo": rotulo}),
        rotulo, num(v), u,
        escape(wa(primeiro["wa"])), escape(primeiro["nome"].lower()), ic("arrow-up-right"), "../%s/" % primeiro["slug"],
        "".join(botoes), json.dumps(dados, ensure_ascii=False))


def inicio():
    return """
<section class="hero" id="inicio">
  <div class="wrap hero__grid">
    <div class="hero__txt">
      <h1>%s</h1>
      <p class="hero__sub">%s</p>
      <div class="hero__acts">
        <a class="pill pill--wa" href="%s" target="_blank" rel="noopener">Pedir orçamento no WhatsApp<span class="pill__ico">%s</span></a>
        <a class="link" href="tel:%s">ou ligue %s</a>
      </div>
      <p class="hero__who"><img src="../assets/img/mark.png" alt="" width="36" height="36"> Atendimento feito pelo próprio Gabriel Sorrilha, em casas e comércios.</p>
    </div>
    %s
  </div>
</section>""" % (escape(INICIO["h1"]), escape(INICIO["sub"]), WA_GERAL, ic("whatsapp-logo"),
                  EMPRESA["telefone_link"], EMPRESA["telefone_exibicao"], painel())


def servicos():
    linhas = []
    for s in SERVICOS:
        v, u, cor, _ = LEITURA[s["slug"]]
        linhas.append("""
      <li><a class="svc" href="../%s/" style="--cor:%s">
        <span class="svc__read">%s<small>%s</small></span>
        <span class="svc__name">%s</span>
        <span class="svc__sum">%s</span>
        <span class="svc__go">%s</span>
      </a></li>""" % (s["slug"], cor, num(v), u, escape(s["nome"]), escape(s["resumo"]), ic("arrow-up-right")))
    return """
<section class="sec" id="servicos">
  <div class="wrap">
    <div class="sec__head">
      <h2>Serviços</h2>
      <p>Cada aparelho tem a sua página, com os defeitos mais comuns e o que fazer até o técnico chegar.</p>
    </div>
    <ul class="svcs">%s
    </ul>
  </div>
</section>""" % "".join(linhas)


def avaliacoes():
    if not DEPOIMENTOS:
        return ""
    itens = []
    for i, d in enumerate(DEPOIMENTOS):
        itens.append("""
      <figure class="quote%s" data-i="%d"%s>
        <blockquote>%s</blockquote>
        <figcaption><strong>%s</strong> <span>%s no Google</span> <a href="%s" target="_blank" rel="noopener">ver avaliação</a></figcaption>
      </figure>""" % (" is-on" if i == 0 else "", i, "" if i == 0 else ' aria-hidden="true"', escape(d["texto"]),
                     escape(d["nome"]), escape(d["quando"]), escape(d["link"])))
    perfil = ('<a class="link" href="%s" target="_blank" rel="noopener">Todas as avaliações no Google</a>' % escape(GOOGLE_PERFIL)) if GOOGLE_PERFIL else ""
    return """
<section class="sec sec--quotes" id="avaliacoes">
  <div class="wrap quotes">
    <p class="quotes__stars" aria-label="5 estrelas">★★★★★</p>
    <h2 class="sr">Avaliações de clientes no Google</h2>
    <div class="quotes__stage">%s
    </div>
    <div class="quotes__nav">
      <button type="button" class="round" data-dir="-1" aria-label="Avaliação anterior">%s</button>
      <p class="quotes__count"><span class="js-n">1</span> de %d avaliações, todas com 5 estrelas</p>
      <button type="button" class="round" data-dir="1" aria-label="Próxima avaliação">%s</button>
    </div>
    %s
  </div>
</section>""" % ("".join(itens), ic("arrow-left"), len(DEPOIMENTOS), ic("arrow-right"), perfil)


CONVERSA = [
    ("eu", "Oi, Gabriel! Vim pelo site. Minha geladeira parou de gelar, o freezer tá normal.", "Você manda a mensagem"),
    ("ele", "Oi! Consigo passar aí amanhã às 9h, pode ser?", "O horário é combinado"),
    ("eu", "Pode sim, obrigada!", None),
    ("ele", "Achei: é o ventilador do freezer. Te passo o valor antes de trocar a peça.", "Diagnóstico e valor antes do conserto"),
    ("ele", "Pronto, já tá gelando de novo 👍", "Resolvido"),
]


def como_funciona():
    bolhas = []
    for quem, txt, passo in CONVERSA:
        bolhas.append('<li class="msg msg--%s">%s<p>%s</p></li>' % (
            quem, ('<span class="msg__step">%s</span>' % passo) if passo else "", escape(txt)))
    return """
<section class="sec sec--chat" id="como-funciona">
  <div class="wrap chat-grid">
    <div class="chat-grid__txt">
      <h2>Tudo começa numa conversa no WhatsApp</h2>
      <p>Você conta o que está acontecendo, de preferência com uma foto ou um vídeo curto. O Gabriel responde, combina o horário e vai até você. O valor é passado antes do conserto, e você decide.</p>
      <a class="pill pill--wa" href="%s" target="_blank" rel="noopener">Começar a conversa<span class="pill__ico">%s</span></a>
    </div>
    <div class="phone">
      <div class="phone__top"><img src="../assets/img/mark.png" alt="" width="34" height="34"><div><strong>Gabriel Sorrilha</strong><span>Sorrilha Refrigeração</span></div></div>
      <ol class="phone__msgs" aria-label="Exemplo de atendimento">%s</ol>
      <p class="phone__note">Conversa de exemplo</p>
    </div>
  </div>
</section>""" % (WA_GERAL, ic("whatsapp-logo"), "".join(bolhas))


def marcas():
    itens = "".join("<li>%s</li>" % escape(m) for m in MARCAS_TODAS)
    return """
<section class="brands" aria-label="Marcas atendidas">
  <p class="brands__t">Atendemos todas as marcas, como</p>
  <div class="mq"><ul class="mq__g">%s</ul><ul class="mq__g" aria-hidden="true">%s</ul></div>
</section>""" % (itens, itens)


def duvidas():
    itens = "".join('<details><summary>%s%s</summary><p>%s</p></details>' % (escape(p), ic("caret-down"), escape(r))
                    for p, r in INICIO["faq"])
    return """
<section class="sec" id="duvidas">
  <div class="wrap faq">
    <h2>Dúvidas comuns</h2>
    <div class="faq__list">%s</div>
  </div>
</section>""" % itens


def contato():
    opcoes = "".join("<option>%s</option>" % escape(o) for o in OPCOES_FORM)
    return """
<section class="sec sec--contact" id="contato">
  <div class="wrap contact">
    <div class="contact__txt">
      <h2>Conte o que aconteceu</h2>
      <p>Preencha e toque em enviar. O WhatsApp abre com a mensagem pronta, e nada fica guardado no site.</p>
      <ul class="contact__ch">
        <li><a href="tel:%s">%s<span><small>Telefone</small>%s</span></a></li>
        <li><a href="%s" target="_blank" rel="noopener">%s<span><small>Instagram</small>%s</span></a></li>
        <li><p>%s<span><small>Atendimento</small>%s - %s</span></p></li>
      </ul>
    </div>
    <form class="form js-form" novalidate>
      <label>Seu nome<input data-campo="Nome" name="nome" autocomplete="name" placeholder="Como podemos te chamar"></label>
      <label>Bairro<input data-campo="Bairro" name="bairro" placeholder="Ex.: Centro"></label>
      <label class="form__full">Aparelho ou serviço<select data-campo="Serviço" name="servico">%s</select></label>
      <label class="form__full">O que está acontecendo?<textarea data-campo="Problema" name="problema" rows="4" required placeholder="Ex.: a geladeira parou de gelar ontem, o freezer continua normal."></textarea></label>
      <p class="form__err" hidden>Escreva o que está acontecendo para o Gabriel entender o problema.</p>
      <button class="pill pill--wa form__full" type="submit">Enviar pelo WhatsApp<span class="pill__ico">%s</span></button>
    </form>
  </div>
</section>""" % (EMPRESA["telefone_link"], ic("phone"), EMPRESA["telefone_exibicao"],
                  EMPRESA["instagram"], ic("instagram-logo"), EMPRESA["instagram_usuario"],
                  ic("map-pin"), EMPRESA["cidade"], EMPRESA["uf"], opcoes, ic("paper-plane-tilt"))


def rodape():
    links = "".join('<li><a href="../%s/">%s</a></li>' % (s["slug"], escape(s["nome"])) for s in SERVICOS)
    return """
<footer class="foot">
  <div class="wrap foot__grid">
    <div><img src="../assets/img/logo-negativo.png" alt="Sorrilha Refrigeração" width="190" height="47"><p>Refrigeração e assistência técnica em %s - %s. Assistência independente, não autorizada de fabricante.</p></div>
    <div><h3>Serviços</h3><ul>%s</ul></div>
    <div><h3>Contato</h3><ul><li><a href="%s" target="_blank" rel="noopener">WhatsApp %s</a></li><li><a href="%s" target="_blank" rel="noopener">%s</a></li><li><a href="../politica-de-privacidade/">Política de Privacidade</a></li><li><a href="../termos-de-uso/">Termos de Uso</a></li></ul></div>
  </div>
  <p class="wrap foot__end">© 2026 %s</p>
</footer>""" % (
        EMPRESA["cidade"], EMPRESA["uf"], links, WA_GERAL, EMPRESA["telefone_exibicao"],
        EMPRESA["instagram"], EMPRESA["instagram_usuario"], EMPRESA["nome"])


def pagina():
    return """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modelo 2 | Sorrilha Refrigeração</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0f3550">
<link rel="icon" href="../assets/img/favicon.png">
<link rel="preload" href="fonts/shoulders.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/icons/icons.css">
<link rel="stylesheet" href="m2.css">
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
%s
<main id="conteudo">%s%s%s%s%s%s%s</main>
%s
<script>window.SORRILHA_WA = "%s";</script>
<script src="m2.js" defer></script>
</body>
</html>
""" % (escape(INICIO["description"]), cabecalho(), inicio(), servicos(), avaliacoes(), como_funciona(),
       marcas(), duvidas(), contato(), rodape(), EMPRESA["whatsapp"])


if __name__ == "__main__":
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(pagina())
    print("ok:", SAIDA)
