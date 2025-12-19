# addon-field-remesher

[![CI](https://github.com/yuri-schmaltz/addon-field-remesher/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yuri-schmaltz/addon-field-remesher/actions/workflows/ci.yml)

Repositório monorepo do add-on Field Remesher para Blender. Veja a documentação detalhada em `field-remesher/README.md`.

## Publicação
- Releases automáticos por tag `v*` publicam o ZIP instalável: veja `.github/workflows/release.yml`.
- Publicação no Blender Extensions (opcional): ver seção abaixo.

## Publicação no Blender Extensions (Opcional)
Este repositório inclui um workflow opcional para preparar o pacote para o Blender Extensions. Pré-requisitos típicos:
- Manifesto do add-on para Extensions (ex.: `blender_manifest.toml` ou equivalente quando aplicável).
- Compatibilidade com políticas do catálogo (nomes, descrições, licença, etc.).

Como usar (quando o manifesto estiver adicionado):
1. Vá em Actions > "Publish (Blender Extensions) — Dry Run".
2. Clique em "Run workflow" para gerar o ZIP preparado e validar estrutura.
3. Siga o processo de submissão do Blender Extensions com o artefato gerado.

Observação: neste momento, o workflow realiza apenas o empacotamento/validação e gera artefato; a submissão é manual.