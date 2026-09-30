# -*- coding: utf-8 -*-
"""
Textos legais do site: Política de Privacidade (LGPD) e Termos de Uso.

Escritos para o que o site faz HOJE:
- não usa cookies, estatísticas (Google Analytics etc.) nem pixel de anúncios;
- não carrega nada de terceiros (fonte e ícones ficam no próprio site);
- o formulário não envia dados para servidor nenhum: só abre o WhatsApp com a mensagem pronta;
- hospedagem no GitHub Pages, que registra o IP de quem acessa por segurança.

Se algo disso mudar (ex.: instalar Google Analytics, formulário com e-mail, chat), ATUALIZE a política.
"""

ATUALIZADO_EM = "30 de setembro de 2026"


def _identificacao(E):
    doc = (", %s" % E["documento"]) if E.get("documento") else ""
    return "%s, nome comercial de %s%s, com atendimento em %s - %s" % (
        E["nome"], E["responsavel"], doc, E["cidade"], E["uf"])


def privacidade(E, R=None):
    """Lista de (título, [parágrafos ou ("lista", [itens])]).
    R = dicionário RASTREAMENTO do conteudo.py. Se tiver algum código preenchido,
    os trechos sobre cookies, medição e compartilhamento mudam para refletir isso."""
    ident = _identificacao(E)
    R = R or {}
    google = bool((R.get("ga4") or "").strip() or (R.get("google_ads") or "").strip())
    meta = bool((R.get("meta_pixel") or "").strip())
    rastreio = google or meta
    ferramentas = []
    if (R.get("ga4") or "").strip():
        ferramentas.append("Google Analytics, para contar visitas e ver quais páginas são mais vistas")
    if (R.get("google_ads") or "").strip():
        ferramentas.append("Google Ads, para saber quais anúncios do Google trouxeram contatos")
    if meta:
        ferramentas.append("Pixel da Meta, para saber quais anúncios do Instagram e do Facebook trouxeram contatos")

    if rastreio:
        resumo_cookie = ("Só usamos cookies de medição se você aceitar no aviso que aparece na primeira visita. "
                         "Sem aceite, nenhum cookie de medição é gravado.")
        sec_cookies = ("Cookies", [
            "Cookies são pequenos arquivos que o navegador guarda. Este site usa cookies apenas se você clicar em "
            "\"Aceitar\" no aviso de cookies, para:",
            ("lista", ferramentas),
            "Essas ferramentas registram dados como páginas visitadas, tipo de aparelho, cidade aproximada e cliques nos botões de "
            "contato. Não identificam você pelo nome. Se você recusar, o Google pode receber apenas sinais técnicos sem cookies, "
            "sem identificação, e o Pixel da Meta não é carregado.",
            "Você pode mudar sua escolha a qualquer momento no link \"Preferências de cookies\", no rodapé, ou apagando os "
            "cookies no seu navegador. A escolha fica guardada no seu próprio navegador.",
            "Base legal: consentimento (art. 7º, inciso I, da LGPD).",
        ])
        extra_compart = [c for c in [
            "Google, se você aceitar os cookies (Google Analytics e Google Ads);" if google else None,
            "Meta, se você aceitar os cookies (Pixel da Meta);" if meta else None,
        ] if c]
    else:
        resumo_cookie = "Este site não usa cookies nem ferramentas de estatística ou de anúncios."
        sec_cookies = ("Cookies", [
            "Este site não usa cookies, nem próprios nem de terceiros. Por isso não há aviso de cookies para aceitar.",
        ])
        extra_compart = []

    return [
        ("Quem somos", [
            "Esta política explica como o site da %s trata informações pessoais. "
            "O responsável pelo tratamento (controlador, nos termos da Lei Geral de Proteção de Dados, Lei nº 13.709/2018) é %s." % (E["nome"], ident),
            "Para qualquer assunto sobre seus dados, fale com a gente pelo WhatsApp %s." % E["telefone_exibicao"],
        ]),
        ("Resumo", [
            ("lista", [
                resumo_cookie,
                "O formulário de orçamento não guarda nada: ele apenas abre o WhatsApp com a sua mensagem pronta, e você decide se envia.",
                "Os dados que você manda pelo WhatsApp são usados só para responder, agendar e fazer o serviço.",
                ("Não vendemos seus dados. Os dados de medição só vão para o Google e a Meta se você aceitar os cookies."
                 if rastreio else "Não vendemos nem compartilhamos seus dados para marketing."),
            ]),
        ]),
        ("Quais dados tratamos e para quê", [
            "Navegação no site. Ao acessar o site, a empresa que hospeda as páginas (GitHub, do grupo Microsoft) registra "
            "automaticamente dados técnicos, como o endereço IP, por motivos de segurança. Nós não temos acesso a esses registros "
            "nem os usamos para identificar visitantes.",
            "Formulário de orçamento. Os campos nome, bairro, tipo de serviço e descrição do problema não são enviados ao site. "
            "Ao tocar em \"Enviar pelo WhatsApp\", o seu aparelho abre o WhatsApp com esses dados escritos na mensagem. "
            "Eles só chegam até nós se você confirmar o envio.",
            "Conversa pelo WhatsApp e ligações. Recebemos o que você informar: nome, telefone, endereço para a visita, fotos ou vídeos "
            "do aparelho e a descrição do problema. Usamos essas informações para responder, fazer o orçamento, agendar e realizar o "
            "serviço, e para dar suporte ou garantia depois.",
        ]),
        ("Base legal", [
            "Tratamos seus dados para tomar as providências que você pediu antes de contratar (orçamento e agendamento) e para "
            "executar o serviço contratado (art. 7º, inciso V, da LGPD). Quando for preciso guardar algum dado por obrigação legal "
            "ou para nos defender em eventual reclamação, usamos as bases do art. 7º, incisos II e VI.",
        ]),
        ("Com quem os dados são compartilhados", [
            "Não vendemos, alugamos nem cedemos seus dados. Eles passam apenas pelos serviços necessários para o atendimento:",
            ("lista", [
                "WhatsApp (Meta), por onde a conversa acontece, sujeito à política de privacidade do próprio WhatsApp;",
                "GitHub, que hospeda este site;",
            ] + extra_compart + [
                "autoridades públicas, somente quando houver obrigação legal ou ordem judicial.",
            ]),
            "Alguns desses serviços podem armazenar dados fora do Brasil, conforme as regras de transferência internacional da LGPD.",
        ]),
        ("Por quanto tempo guardamos", [
            "Mantemos as conversas e os dados do atendimento pelo tempo necessário para prestar o serviço e cobrir o período de "
            "garantia e de eventuais reclamações previstos no Código de Defesa do Consumidor. Depois disso, as informações podem ser "
            "apagadas a qualquer momento, inclusive a seu pedido, salvo quando a lei exigir que sejam guardadas.",
        ]),
        ("Seus direitos", [
            "Pela LGPD (art. 18), você pode, a qualquer momento e sem custo:",
            ("lista", [
                "confirmar se tratamos dados seus e ter acesso a eles;",
                "corrigir dados incompletos, errados ou desatualizados;",
                "pedir a exclusão dos dados que não precisamos mais guardar;",
                "saber com quem os dados foram compartilhados;",
                "revogar um consentimento que tenha dado.",
            ]),
            "Para exercer esses direitos, mande uma mensagem pelo WhatsApp %s. Respondemos no menor prazo possível. "
            "Se não ficar satisfeito, você também pode reclamar à Autoridade Nacional de Proteção de Dados (ANPD), pelo site gov.br/anpd." % E["telefone_exibicao"],
        ]),
        sec_cookies,
        ("Segurança", [
            "O site é servido com conexão criptografada (HTTPS). Os dados recebidos pelo WhatsApp ficam no aparelho usado no "
            "atendimento, protegido por senha, e só são acessados por quem presta o serviço.",
        ]),
        ("Links para outros sites", [
            "O site tem links para o WhatsApp, o Instagram e as avaliações no Google. Ao abri-los, você passa a usar serviços de "
            "outras empresas, com políticas de privacidade próprias.",
        ]),
        ("Crianças e adolescentes", [
            "Nossos serviços são contratados por adultos. Não coletamos intencionalmente dados de menores de 18 anos.",
        ]),
        ("Alterações", [
            "Podemos atualizar esta política quando o site ou a forma de atendimento mudarem. A data da última atualização fica no topo "
            "desta página.",
        ]),
    ]


def termos(E):
    ident = _identificacao(E)
    return [
        ("Sobre o site", [
            "Este site é da %s e serve para apresentar os serviços oferecidos e facilitar o contato. "
            "Ao usar o site, você concorda com estes termos." % ident,
        ]),
        ("O site não é uma loja", [
            "Nenhum serviço é contratado ou pago pelo site. Os botões e o formulário apenas abrem uma conversa no WhatsApp. "
            "O serviço só é combinado depois do contato, com orçamento informado antes de qualquer conserto.",
        ]),
        ("Informações sobre serviços", [
            "As descrições de serviços, problemas comuns e dicas do site são informativas e não substituem a avaliação de um técnico "
            "no local. Prazos e valores dependem do diagnóstico de cada aparelho e são informados no orçamento.",
            "Em caso de cheiro de gás, feche o registro, abra portas e janelas, não acione interruptores e, se o cheiro for forte, "
            "ligue para o Corpo de Bombeiros (193).",
        ]),
        ("Garantia e direitos do consumidor", [
            "Os serviços seguem o Código de Defesa do Consumidor (Lei nº 8.078/1990). Para serviços em aparelhos e instalações, "
            "o prazo legal para reclamar de defeitos aparentes é de 90 dias a partir da conclusão do serviço (art. 26, inciso II). "
            "Condições de garantia de peças e serviços são informadas no orçamento.",
        ]),
        ("Assistência independente e marcas", [
            "A %s é uma assistência técnica independente. Não é assistência autorizada de nenhum fabricante. "
            "As marcas citadas no site pertencem aos seus donos e aparecem apenas para informar os aparelhos que atendemos." % E["nome"],
        ]),
        ("Avaliações de clientes", [
            "As avaliações exibidas foram publicadas por clientes no Google e são reproduzidas como foram escritas, com o nome "
            "abreviado. Cada uma tem um link para a publicação original.",
        ]),
        ("Conteúdo do site", [
            "Os textos, o logotipo e a identidade visual da %s não podem ser copiados para uso comercial sem autorização." % E["nome"],
        ]),
        ("Privacidade", [
            "O tratamento de dados pessoais está descrito na Política de Privacidade.",
        ]),
        ("Alterações e foro", [
            "Estes termos podem ser atualizados a qualquer momento; a data da última versão fica no topo desta página. "
            "Vale a legislação brasileira. Como relação de consumo, você pode resolver qualquer questão no foro do seu domicílio.",
        ]),
    ]
