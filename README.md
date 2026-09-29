# Sorrilha Refrigeração: site

Site da Sorrilha Refrigeração (Gabriel Sorrilha), Sertãozinho - SP.
HTML e CSS estáticos, com uma página para cada serviço para aparecer nas buscas do Google.

## Páginas
| Endereço | Busca que a página mira |
|---|---|
| `/` | refrigeração em Sertãozinho |
| `/ar-condicionado/` | instalação, limpeza e conserto de ar-condicionado em Sertãozinho |
| `/camara-fria/` | manutenção e instalação de câmara fria em Sertãozinho |
| `/geladeira-e-freezer/` | conserto de geladeira e freezer em Sertãozinho |
| `/maquina-de-lavar/` | conserto de máquina de lavar em Sertãozinho |
| `/fogao/` | conserto de fogão em Sertãozinho |
| `/reparos-em-casa/` | pequenos reparos elétricos e hidráulicos em Sertãozinho |

## Como editar
Todos os textos ficam em `tools/conteudo.py` (telefone, serviços, perguntas, marcas, depoimentos).
Depois de editar, gere as páginas de novo:

```
python3 tools/build.py      # gera todas as páginas, sitemap.xml e robots.txt
python3 tools/icones.py     # só se usar um ícone novo
```

- **Depoimentos do Google:** cole na lista `DEPOIMENTOS` em `tools/conteudo.py`. Com a lista vazia, a seção não aparece.
- **Domínio próprio:** troque `SITE_URL` em `tools/conteudo.py` e gere de novo.
- **Visual:** `assets/css/site.css` (cores no topo do arquivo).

## Publicar
Settings → Pages → Source: *Deploy from a branch* → Branch `main` / `(root)`.

Depois de publicado, cadastre o site no Google Search Console e envie o `sitemap.xml`.
