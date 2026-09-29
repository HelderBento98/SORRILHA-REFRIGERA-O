# -*- coding: utf-8 -*-
"""
Gera assets/icons/ com só os ícones Phosphor (MIT) usados no site.
Rode depois do build:  python3 tools/icones.py
Precisa de: npm, pip install fonttools brotli
"""
import os, re, subprocess, tempfile, glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
usados = [l.strip() for l in open(os.path.join(RAIZ, "tools", "icones-usados.txt")) if l.strip()]

tmp = tempfile.mkdtemp()
subprocess.run(["npm", "pack", "@phosphor-icons/web@2.1.2", "--silent"], cwd=tmp, check=True, stdout=subprocess.DEVNULL)
subprocess.run("tar xzf *.tgz", shell=True, cwd=tmp, check=True)
base = os.path.join(tmp, "package", "src", "regular")
css = open(os.path.join(base, "style.css")).read()

regras, codigos = [], []
for nome in usados:
    m = re.search(r'\.ph\.ph-' + re.escape(nome) + r':before\s*\{\s*content:\s*"\\([0-9a-f]+)"', css)
    if not m:
        print("ícone não encontrado:", nome); continue
    codigos.append(m.group(1))
    regras.append('.ph.ph-%s:before{content:"\\%s"}' % (nome, m.group(1)))

saida = os.path.join(RAIZ, "assets", "icons")
subprocess.run(["pyftsubset", os.path.join(base, "Phosphor.ttf"), "--unicodes=" + ",".join("U+" + c for c in codigos),
                "--flavor=woff2", "--output-file=" + os.path.join(saida, "phosphor-subset.woff2")], check=True)
cab = ('/* Phosphor Icons (MIT) - subconjunto so com os icones usados no site. Gerado por tools/icones.py */\n'
       '@font-face{font-family:"Phosphor";src:url("phosphor-subset.woff2") format("woff2");font-weight:normal;font-style:normal;font-display:block}\n'
       '.ph{font-family:"Phosphor"!important;speak:never;font-style:normal;font-weight:normal;font-variant:normal;'
       'text-transform:none;line-height:1;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;display:inline-block}\n')
open(os.path.join(saida, "icons.css"), "w").write(cab + "\n".join(regras) + "\n")
print("%d ícones no subconjunto" % len(codigos))
