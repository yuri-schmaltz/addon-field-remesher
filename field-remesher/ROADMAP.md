# Roadmap (exaustivo) — Field Remesher

Este roadmap está alinhado com milestones de versão e com o backlog importável em `docs/github_backlog.csv`.

## Milestones
- **v0.1 (MVP)**: fallback Quadriflow + UI + preservação básica de atributos
- **v0.2**: batch/fila + guias (dados/UX) + presets
- **v0.3 (Native alpha)**: core nativo + bindings + integração Blender↔engine (sem guias)
- **v0.4 (Native beta)**: guias influenciando o campo + reprojeção avançada (BVH)
- **v1.0 (Produção)**: CI multiplataforma, testes, benchmarks, docs completas, política ABI

---

## v0.1 — MVP (Quadriflow)
### Entregas
- Add-on instalável por zip
- Operador principal de remesh (não-destrutivo)
- Fallback Quadriflow estável (override de contexto, rollback)
- Transferência de materiais, UV e cores (quando existirem)
- Logging e docs básicas

### Aceitação
- Remesh em 10 meshes (organic + hard-surface) sem travar UI
- Transferência não falha quando atributos inexistem
- README Quickstart

---

## v0.2 — Batch + Guias (dados/UX) + Presets
### Entregas
- Batch multi-objeto com fila, status e cancelamento
- Sistema de guias: Curves + JSON em Custom Props + overlay de direção
- Conversão de annotate/grease pencil para guides
- Presets (Organic/Hard-surface/Game-ready/LOD) e sugestão automática

### Aceitação
- Batch em 20 objetos sem corromper contexto
- Guias persistem e exibem overlay
- Presets reprodutíveis

---

## v0.3 — Native Engine (alpha)
### Entregas
- Estrutura `native/` completa: core + pybind11 + build local
- Módulo `instant_meshes_py.remesh()` com contrato mínimo
- Integração Blender↔engine (conversão mesh↔arrays)
- Backend AUTO/INSTANT funcional quando binário está presente

### Aceitação
- Engine roda pelo menos em 1 plataforma no Blender
- Sem crash, erros tratados
- Parâmetros essenciais com efeito (target, boundary, sharp, seed)

---

## v0.4 — Guias na engine + Reprojeção BVH (beta)
### Entregas
- Consumo real de guides pelo engine (constraints no campo)
- UI por guia: peso/rigidez
- Reprojeção BVH barycentric (UV/cores/normals) como opção avançada
- Comparativos/baselines vs Data Transfer

### Aceitação
- Guias mudam o fluxo de quads de forma visível e estável
- Reprojeção melhora casos difíceis (hard-surface, UVs complexos)

---

## v1.0 — Produção
### Entregas
- CI multiplataforma: build do native por versão de Blender
- Testes headless (integração) + fixtures licenciadas
- Benchmarks e métricas
- Documentação completa + troubleshooting
- Política de ABI e matriz de binários publicada

### Aceitação
- Releases reprodutíveis e instaláveis
- Suporte a pipeline (LOD, export, cache opcional)

