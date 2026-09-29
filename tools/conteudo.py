# -*- coding: utf-8 -*-
"""
Conteúdo do site da Sorrilha Refrigeração.

Tudo o que aparece escrito no site está aqui. Para mudar um texto, edite
este arquivo e rode:  python3 tools/build.py
"""

# ---------------------------------------------------------------------------
# DADOS DA EMPRESA
# ---------------------------------------------------------------------------
EMPRESA = {
    "nome": "Sorrilha Refrigeração",
    "responsavel": "Gabriel Sorrilha",
    "cidade": "Sertãozinho",
    "uf": "SP",
    "whatsapp": "5575999062183",          # 55 + DDD + número, só dígitos
    "telefone_exibicao": "(75) 99906-2183",
    "telefone_link": "+5575999062183",
    "instagram": "https://www.instagram.com/sorrilha_refrigeracao/",
    "instagram_usuario": "@sorrilha_refrigeracao",
}

# Endereço onde o site fica publicado (sem barra no final).
# Quando tiver domínio próprio, troque aqui, ex.: "https://sorrilharefrigeracao.com.br"
SITE_URL = "https://helderbento98.github.io/SORRILHA-REFRIGERA-O"

# ---------------------------------------------------------------------------
# DEPOIMENTOS DO GOOGLE
# Cole aqui as avaliações reais do perfil do Google, exatamente como estão.
# Enquanto a lista estiver vazia, a seção de depoimentos não aparece no site.
# Exemplo:
#   {"nome": "Maria S.", "estrelas": 5, "texto": "Atendimento rápido...", "quando": "há 2 semanas"},
# ---------------------------------------------------------------------------
DEPOIMENTOS = [
    # Avaliações reais do perfil no Google (5 estrelas), texto como o cliente escreveu.
    # Nome exibido: primeiro nome + inicial do sobrenome. "link" abre a avaliação no Google.
    {"nome": "Tainá L.", "estrelas": 5, "quando": "há 3 meses",
     "texto": "Muito bom profissional, atendimento excelente.",
     "link": "https://www.google.com/maps/contrib/117794246307687388836/reviews?hl=pt-BR"},
    {"nome": "Andra B.", "estrelas": 5, "quando": "há 3 meses",
     "texto": "Prestam um ótimo atendimento, são honestos com os clientes, e isso é um grande diferencial, podem confiar!",
     "link": "https://www.google.com/maps/contrib/114087981476000836882/reviews?hl=pt-BR"},
    {"nome": "Quezia F.", "estrelas": 5, "quando": "há 2 meses",
     "texto": "Excelente profissional e ótimo atendimento.",
     "link": "https://www.google.com/maps/contrib/115886534326477653508/reviews?hl=pt-BR"},
    {"nome": "Manuel H.", "estrelas": 5, "quando": "há 3 meses",
     "texto": "Muito bom. Fez o concerto da máquina de lavar ficou top. Muito prestativo, recomendo.",
     "link": "https://www.google.com/maps/contrib/110952830723655940270/reviews?hl=pt-BR"},
]

# Link para o perfil no Google (aparece junto dos depoimentos). Deixe "" se não tiver.
GOOGLE_PERFIL = ""

# Nota média e total de avaliações que aparecem no perfil do Google (ex.: "4,9" e 37).
# Deixe "" e 0 para esconder a nota.
GOOGLE_NOTA = ""
GOOGLE_TOTAL = 0

# ---------------------------------------------------------------------------
# MARCAS ATENDIDAS (nomes em texto)
# ---------------------------------------------------------------------------
MARCAS_AR = ["Samsung", "LG", "Midea", "Springer", "Gree", "Elgin", "Daikin",
             "Fujitsu", "Carrier", "Consul", "Philco", "Agratto", "Electrolux", "TCL"]
MARCAS_REFRIG = ["Brastemp", "Consul", "Electrolux", "Samsung", "LG", "Panasonic",
                 "Midea", "Esmaltec", "Metalfrio", "Gelopar", "Fricon", "Philco"]
MARCAS_LAVAR = ["Brastemp", "Consul", "Electrolux", "LG", "Samsung", "Panasonic", "Midea", "Philco"]
MARCAS_FOGAO = ["Brastemp", "Consul", "Electrolux", "Atlas", "Esmaltec", "Mueller", "Dako", "Continental"]

# Ordem da faixa de marcas da página inicial (sem repetir)
def _unicas(*listas):
    vistas, saida = set(), []
    for lista in listas:
        for m in lista:
            if m not in vistas:
                vistas.add(m); saida.append(m)
    return saida

MARCAS_TODAS = _unicas(MARCAS_AR, MARCAS_REFRIG, MARCAS_LAVAR, MARCAS_FOGAO)

# ---------------------------------------------------------------------------
# PÁGINA INICIAL
# ---------------------------------------------------------------------------
INICIO = {
    "title": "Refrigeração em Sertãozinho - SP | Sorrilha Refrigeração",
    "description": ("Ar-condicionado, câmara fria e conserto de geladeira, freezer, máquina de lavar e fogão "
                    "em Sertãozinho - SP. Atendimento em casa e no comércio."),
    "h1": "Refrigeração e assistência técnica em Sertãozinho",
    "sub": ("Ar-condicionado, câmara fria, geladeira, freezer, máquina de lavar e fogão, "
            "na sua casa ou no seu comércio. E também pequenos reparos e manutenções residenciais."),
    "faq": [
        ("Vocês atendem em qual cidade?",
         "Atendemos em Sertãozinho - SP, em casas, apartamentos e comércios. Se você está em outra cidade da região, "
         "consulte pelo WhatsApp."),
        ("Como faço para pedir um orçamento?",
         "Pelo WhatsApp ou pelo formulário desta página. Conte qual é o aparelho, a marca e o que está acontecendo. "
         "Se puder, mande uma foto ou um vídeo curto: isso ajuda a entender o problema antes da visita."),
        ("Vocês atendem todas as marcas?",
         "Sim. Fazemos assistência técnica independente em aparelhos de todas as marcas. "
         "Não somos assistência autorizada de fabricante."),
        ("Atendem mercados e outros comércios?",
         "Sim. Fazemos instalação, manutenção e conserto de câmaras frias, freezers e expositores comerciais, "
         "além do ar-condicionado do estabelecimento."),
        ("Posso resolver vários serviços na mesma visita?",
         "Pode, e costuma ser mais prático. Mande a lista pelo WhatsApp, por exemplo a limpeza do ar-condicionado e "
         "uma tomada para trocar, e combinamos tudo de uma vez."),
    ],
}

# ---------------------------------------------------------------------------
# PÁGINAS DE SERVIÇO
# Cada página mira uma busca do Google: "<serviço> em Sertãozinho".
# ---------------------------------------------------------------------------
SERVICOS = [
    {
        "slug": "ar-condicionado",
        "nome": "Ar-condicionado",
        "icone": "snowflake",
        "resumo": "Instalação, limpeza, higienização e conserto de ar-condicionado split.",
        "title": "Instalação de Ar-Condicionado em Sertãozinho | Sorrilha",
        "description": ("Instalação, limpeza, higienização e conserto de ar-condicionado split em Sertãozinho - SP. "
                        "Casas e comércios, todas as marcas. Orçamento pelo WhatsApp."),
        "h1": "Instalação e manutenção de ar-condicionado em Sertãozinho",
        "intro": ("Instalamos, limpamos e consertamos ar-condicionado split em casas, escritórios e comércios de "
                  "Sertãozinho. Você descreve o problema pelo WhatsApp e o técnico vai até o local para avaliar e resolver."),
        "faz": ["Instalação de ar-condicionado split", "Limpeza e higienização completa",
                "Manutenção preventiva", "Conserto e assistência técnica"],
        "problemas": ["Pingando água dentro do ambiente", "Não gela ou demora para gelar", "Cheiro ruim ao ligar",
                      "Barulho ou vibração diferente", "Desliga sozinho ou pisca luzes no painel",
                      "Gelo na tubulação ou na evaporadora"],
        "blocos": [
            ("Por que a instalação bem feita faz diferença",
             "Boa parte dos defeitos de ar-condicionado começa na instalação: dreno sem caimento, tubulação mal isolada "
             "ou aparelho ligado num circuito sem a proteção adequada. Por isso a instalação começa pela escolha do ponto "
             "das unidades interna e externa, do trajeto da tubulação e do dreno e pela conferência da parte elétrica. "
             "Assim o aparelho gela como deve, consome menos energia e dura mais."),
            ("Limpeza e higienização: quando fazer",
             "Com o uso, o filtro e a serpentina acumulam poeira, fungos e bactérias. O resultado aparece como cheiro ruim, "
             "menos frio e conta de luz mais alta. Em casa, o recomendado é uma higienização completa pelo menos uma vez "
             "por ano, ou a cada seis meses se o aparelho fica ligado todos os dias. A limpeza do filtro você mesmo pode "
             "fazer a cada 15 a 30 dias."),
        ],
        "marcas": MARCAS_AR,
        "faq": [
            ("De quanto em quanto tempo devo limpar o ar-condicionado?",
             "Para uso residencial, uma higienização completa por ano é o mínimo. Se o aparelho fica ligado todos os dias "
             "ou o ambiente tem muita poeira, o ideal é a cada seis meses. O filtro pode ser lavado por você a cada 15 a 30 dias."),
            ("Meu ar-condicionado está pingando água. O que pode ser?",
             "As causas mais comuns são dreno entupido, mangueira do dreno dobrada ou sem caimento e filtro muito sujo, "
             "que faz a serpentina congelar e depois gotejar. Desligue o aparelho e peça uma avaliação: a água pode "
             "estragar a parede e atingir a parte elétrica."),
            ("Quanto custa a instalação do ar-condicionado?",
             "Depende da capacidade do aparelho (BTUs), da distância entre as unidades interna e externa e do tipo de parede. "
             "Mande pelo WhatsApp o modelo do aparelho e fotos do local para receber uma estimativa."),
            ("Vocês instalam aparelho de qualquer marca?",
             "Sim. Instalamos e fazemos manutenção em ar-condicionado split de todas as marcas."),
        ],
        "wa": "Olá, Gabriel! Vim pelo site e preciso de serviço em ar-condicionado.",
        "keywords": "instalação de ar-condicionado Sertãozinho, limpeza de ar-condicionado, higienização de ar-condicionado, conserto de ar-condicionado",
    },
    {
        "slug": "camara-fria",
        "nome": "Câmara fria",
        "icone": "fridge",
        "resumo": "Instalação, manutenção e conserto de câmara fria para mercados e comércios.",
        "title": "Manutenção de Câmara Fria em Sertãozinho | Sorrilha",
        "description": ("Instalação, manutenção preventiva e conserto de câmara fria para mercados, açougues, padarias "
                        "e restaurantes em Sertãozinho - SP. Chame no WhatsApp."),
        "h1": "Câmara fria para mercados e comércios em Sertãozinho",
        "intro": ("Instalação, limpeza, manutenção e conserto de câmaras frias, freezers e expositores para quem trabalha "
                  "com alimentos. Câmara parada é mercadoria em risco: quanto antes o chamado, menor o prejuízo."),
        "faz": ["Instalação de câmara fria", "Manutenção preventiva", "Conserto e assistência técnica",
                "Limpeza do evaporador e do condensador", "Freezers e expositores comerciais"],
        "problemas": ["Não chega à temperatura programada", "Gelo acumulando no evaporador",
                      "Compressor ligando e desligando toda hora", "Porta sem vedação ou borracha danificada",
                      "Painel com alarme ou apagado", "Barulho alto na unidade externa"],
        "blocos": [
            ("Manutenção preventiva evita perda de mercadoria",
             "A maioria das paradas de câmara fria dá sinais antes de acontecer: gelo acumulando no evaporador, temperatura "
             "oscilando, compressor trabalhando mais que o normal. Com visitas periódicas, esses sinais são corrigidos antes "
             "de virar prejuízo. A frequência ideal depende do tamanho da câmara e do uso, e é combinada com você."),
            ("Para quem atendemos",
             "Mercados, açougues, padarias, restaurantes, lanchonetes e distribuidoras que dependem de refrigeração para "
             "conservar produtos. Também cuidamos do ar-condicionado do salão e do escritório, para você resolver tudo "
             "com um só contato."),
        ],
        "marcas": ["Gelopar", "Fricon", "Metalfrio", "Eletrofrio", "Consul", "Elgin", "Danfoss", "Embraco"],
        "faq": [
            ("Quais sinais mostram que a câmara fria precisa de manutenção?",
             "Gelo acumulando no evaporador, temperatura que não se mantém, compressor ligando e desligando com frequência, "
             "porta que não veda bem e barulho diferente na unidade externa. Qualquer um desses sinais merece avaliação."),
            ("O que fazer se a câmara fria parar de gelar?",
             "Mantenha a porta fechada o máximo possível para conservar o frio, confira se o disjuntor não desarmou e chame "
             "pelo WhatsApp informando a temperatura que aparece no painel."),
            ("É possível combinar manutenção periódica?",
             "Sim. A frequência das visitas é definida de acordo com o tamanho da câmara e com o uso no seu comércio."),
            ("Atendem câmara fria de qualquer marca?",
             "Sim. Atendemos câmaras frias, freezers e expositores comerciais de todas as marcas."),
        ],
        "wa": "Olá, Gabriel! Vim pelo site. Tenho um comércio e preciso de atendimento em câmara fria.",
        "keywords": "câmara fria Sertãozinho, manutenção de câmara fria, conserto de câmara fria, instalação de câmara fria",
    },
    {
        "slug": "geladeira-e-freezer",
        "nome": "Geladeira e freezer",
        "icone": "thermometer-cold",
        "resumo": "Conserto de geladeira e freezer que não gela, forma gelo ou faz barulho.",
        "title": "Conserto de Geladeira e Freezer em Sertãozinho | Sorrilha",
        "description": ("Conserto de geladeira e freezer em Sertãozinho - SP: não gela, forma gelo, faz barulho ou desliga "
                        "sozinho. Atendimento em domicílio, todas as marcas."),
        "h1": "Conserto de geladeira e freezer em Sertãozinho",
        "intro": ("Geladeira que parou de gelar, freezer formando gelo demais ou aparelho fazendo barulho. O atendimento é "
                  "feito na sua casa ou no seu comércio, com diagnóstico antes do conserto."),
        "faz": ["Geladeiras de uma e duas portas", "Geladeiras frost free", "Freezers horizontais e verticais",
                "Freezers e expositores comerciais"],
        "problemas": ["Geladeira não gela", "Freezer gela, mas a geladeira não", "Gelo acumulando demais",
                      "Barulho alto ou estalos", "Água embaixo das gavetas", "Desliga sozinha ou não liga"],
        "blocos": [
            ("Consertar ou trocar?",
             "Na maioria dos casos, o conserto sai bem mais barato que um aparelho novo. Depois do diagnóstico você recebe "
             "o valor do serviço e decide se compensa. O objetivo é você decidir com informação, sem surpresa."),
            ("Cuidados que evitam defeito",
             "Deixe espaço atrás e nas laterais para o ar circular, não coloque comida quente dentro da geladeira e confira "
             "de tempos em tempos se a borracha da porta está vedando. Em geladeiras sem frost free, faça o degelo quando "
             "a camada de gelo passar de meio centímetro."),
        ],
        "marcas": MARCAS_REFRIG,
        "faq": [
            ("Minha geladeira não gela, mas o freezer está normal. O que pode ser?",
             "Em geladeiras frost free, o problema costuma estar na circulação de ar entre o freezer e a geladeira: "
             "ventilador parado, gelo bloqueando a passagem ou falha no sistema de degelo. O diagnóstico no local confirma a causa."),
            ("É normal a geladeira fazer barulho?",
             "Um zumbido baixo do motor e estalos leves quando a temperatura muda são normais. Barulho alto, batidas ou "
             "chiado contínuo indicam problema e merecem avaliação."),
            ("Vocês atendem freezer de comércio?",
             "Sim. Atendemos freezers horizontais e verticais, residenciais e comerciais, e expositores."),
        ],
        "wa": "Olá, Gabriel! Vim pelo site e preciso de conserto em geladeira/freezer.",
        "keywords": "conserto de geladeira Sertãozinho, conserto de freezer, geladeira não gela, assistência técnica geladeira",
    },
    {
        "slug": "maquina-de-lavar",
        "nome": "Máquina de lavar",
        "icone": "wash",
        "resumo": "Conserto e limpeza completa de máquina de lavar roupas.",
        "title": "Conserto de Máquina de Lavar em Sertãozinho | Sorrilha",
        "description": ("Conserto e limpeza de máquina de lavar em Sertãozinho - SP: não centrifuga, vaza água, não liga "
                        "ou faz barulho. Atendimento em domicílio, todas as marcas."),
        "h1": "Conserto e limpeza de máquina de lavar em Sertãozinho",
        "intro": ("Assistência técnica para máquinas de lavar roupas e limpeza completa do cesto, onde se acumulam "
                  "resto de sabão, amaciante e sujeira que causam mau cheiro."),
        "faz": ["Conserto e assistência técnica", "Limpeza completa da máquina", "Diagnóstico no local"],
        "problemas": ["Não centrifuga", "Não enche ou não solta a água", "Vazando água", "Barulho forte ou máquina andando",
                      "Não liga ou para no meio do ciclo", "Roupa saindo com cheiro ou manchada"],
        "blocos": [
            ("Por que limpar a máquina de lavar",
             "Sabão, amaciante e fiapos se acumulam entre o cesto e o tanque, numa parte que não dá para ver. Isso causa "
             "mau cheiro, manchas na roupa e pode prejudicar peças da máquina. A limpeza completa remove essa sujeira e "
             "melhora a lavagem."),
        ],
        "marcas": MARCAS_LAVAR,
        "faq": [
            ("Minha máquina não centrifuga. O que pode ser?",
             "Pode ser roupa desbalanceada no cesto, dreno entupido que impede a água de sair, correia gasta ou defeito "
             "na placa ou no motor. Redistribua a roupa e rode só a centrifugação. Se não resolver, peça uma avaliação."),
            ("De quanto em quanto tempo devo limpar a máquina?",
             "Para o uso normal de uma família, uma limpeza completa por ano costuma bastar. Se a roupa começar a sair com "
             "cheiro ou manchas, é sinal de que está na hora."),
            ("A máquina está vazando. Posso continuar usando?",
             "Melhor não. Água perto da parte elétrica é arriscada e o vazamento pode piorar. Feche a torneira da máquina "
             "e peça uma avaliação."),
        ],
        "wa": "Olá, Gabriel! Vim pelo site e preciso de conserto/limpeza de máquina de lavar.",
        "keywords": "conserto de máquina de lavar Sertãozinho, máquina não centrifuga, limpeza de máquina de lavar",
    },
    {
        "slug": "fogao",
        "nome": "Fogão",
        "icone": "oven",
        "resumo": "Conserto de boca que não acende, chama amarela, acendimento e forno.",
        "title": "Conserto de Fogão em Sertãozinho | Sorrilha Refrigeração",
        "description": ("Conserto de fogão em Sertãozinho - SP: boca que não acende, chama amarela, acendimento automático "
                        "e forno. Atendimento em domicílio, todas as marcas."),
        "h1": "Conserto de fogão em Sertãozinho",
        "intro": ("Boca que não acende, chama fraca ou amarelada, acendimento automático falhando ou forno que não "
                  "esquenta direito. A assistência é feita na sua casa."),
        "faz": ["Conserto do acendimento automático", "Regulagem de chama", "Limpeza de queimadores e injetores",
                "Conserto de forno"],
        "problemas": ["Boca não acende", "Chama amarela ou fraca", "Acendimento automático não funciona",
                      "Forno não esquenta ou apaga", "Botão duro ou solto", "Panela ficando preta"],
        "blocos": [
            ("Sentiu cheiro de gás?",
             "Feche o registro do botijão ou do gás encanado, abra portas e janelas e não acenda luzes, fósforos nem "
             "aparelhos elétricos no local. Com o ambiente ventilado, chame o técnico. Se o cheiro for forte, ligue para "
             "o Corpo de Bombeiros no 193."),
        ],
        "marcas": MARCAS_FOGAO,
        "faq": [
            ("Por que a chama do fogão fica amarela?",
             "Chama amarela geralmente indica queima incompleta: queimador sujo ou entupido, peças encaixadas fora do lugar "
             "ou entrada de ar desregulada. Além de escurecer as panelas, desperdiça gás. Limpeza e regulagem resolvem na "
             "maioria dos casos."),
            ("O acendimento automático parou. Tem conserto?",
             "Tem. O defeito costuma estar na vela, no fio ou no módulo de ignição, peças fáceis de encontrar para as "
             "marcas mais comuns."),
        ],
        "wa": "Olá, Gabriel! Vim pelo site e preciso de conserto de fogão.",
        "keywords": "conserto de fogão Sertãozinho, fogão não acende, chama amarela, assistência técnica fogão",
    },
    {
        "slug": "reparos-em-casa",
        "nome": "Reparos em casa",
        "icone": "wrench",
        "resumo": "Tomadas, interruptores, lustres, encanamento e vazamentos.",
        "title": "Pequenos Reparos em Casa em Sertãozinho | Sorrilha",
        "description": ("Instalação de tomadas, interruptores, lustres e luminárias, conserto de encanamento e vazamentos em "
                        "Sertãozinho - SP. Vários reparos na mesma visita."),
        "h1": "Pequenos reparos em casa em Sertãozinho",
        "intro": ("Aquele serviço pequeno que fica esperando na lista: tomada que não funciona, lustre para instalar, "
                  "torneira pingando ou cano vazando. O mesmo técnico que cuida do seu ar-condicionado resolve."),
        "faz": ["Instalação e troca de tomadas", "Instalação e troca de interruptores", "Instalação de lustres e luminárias",
                "Conserto de encanamento", "Vazamentos em pias, torneiras e conexões"],
        "problemas": ["Tomada sem energia ou esquentando", "Interruptor com mau contato", "Lustre ou luminária para instalar",
                      "Torneira pingando", "Vazamento embaixo da pia", "Cano ou conexão vazando"],
        "blocos": [
            ("Um profissional para vários serviços",
             "Em vez de procurar um técnico para a tomada, outro para o vazamento e outro para o ar-condicionado, você "
             "resolve tudo numa visita. Mande a lista pelo WhatsApp, com fotos se puder, e combine o melhor horário."),
        ],
        "marcas": [],
        "faq": [
            ("Que tipo de serviço elétrico vocês fazem?",
             "Pequenos serviços do dia a dia: instalação e troca de tomadas e interruptores e instalação de lustres e "
             "luminárias. Para obras maiores, como troca de fiação ou do quadro de disjuntores, consulte pelo WhatsApp."),
            ("Dá para fazer vários reparos na mesma visita?",
             "Sim, e costuma ser mais prático. Envie a lista pelo WhatsApp e combine tudo de uma vez."),
        ],
        "wa": "Olá, Gabriel! Vim pelo site e preciso de um reparo em casa.",
        "keywords": "marido de aluguel Sertãozinho, instalação de tomada, instalação de lustre, conserto de vazamento",
    },
]

# Opções do campo "Tipo de serviço" do formulário
OPCOES_FORM = ["Ar-condicionado", "Câmara fria", "Geladeira ou freezer", "Máquina de lavar", "Fogão",
               "Tomada, lustre ou parte elétrica", "Encanamento ou vazamento", "Outro"]
# Qual opção fica marcada em cada página de serviço
OPCAO_POR_SERVICO = {
    "ar-condicionado": "Ar-condicionado", "camara-fria": "Câmara fria", "geladeira-e-freezer": "Geladeira ou freezer",
    "maquina-de-lavar": "Máquina de lavar", "fogao": "Fogão", "reparos-em-casa": "Tomada, lustre ou parte elétrica",
}
