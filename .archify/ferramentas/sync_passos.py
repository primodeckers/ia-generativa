#!/usr/bin/env python3
"""Sincroniza o <slug>.passos.json de um workflow com a página <slug>-passo-a-passo.html.

Uso: sync_passos.py PASTA_DO_WORKFLOW [--titulo "Novo título da página"]
Substitui o bloco walk-data da página pelo conteúdo atual do JSON. Com --titulo, troca também o título
da página (aba, cabeçalho e rótulos de acessibilidade) pelo texto novo.
"""
import json, re, sys, html, os

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    folder = args[0]
    titulo = args[args.index('--titulo') + 1] if '--titulo' in args else None
    slug = os.path.basename(os.path.normpath(folder))
    pj = os.path.join(folder, slug + '.passos.json')
    hp = os.path.join(folder, slug + '-passo-a-passo.html')
    data = json.load(open(pj, encoding='utf-8'))
    h = open(hp, encoding='utf-8').read()
    m = re.search(r'(<script id="walk-data" type="application/json">)(.*?)(</script>)', h, re.S)
    assert m, 'walk-data não encontrado'
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    h = h[:m.start(2)] + blob + h[m.end(2):]
    if titulo:
        t = re.search(r'<title>(.*?)</title>', h, re.S)
        old = html.unescape(t.group(1)).strip()
        if old.endswith(' Diagram'):
            old = old[:-len(' Diagram')]
        n = h.count(old) + h.count(html.escape(old, quote=False)) + h.count(html.escape(old))
        for a, b in ((old, titulo), (html.escape(old, quote=False), html.escape(titulo, quote=False)), (html.escape(old), html.escape(titulo))):
            h = h.replace(a, b)
        print('título trocado:', repr(old), '->', repr(titulo), f'({n} ocorrências)')
    open(hp, 'w', encoding='utf-8').write(h)
    print('ok', hp)

main()
