# SPEC — Field Remesher (Instant-like)

## Objetivo
Fornecer retopologia quad com orientação por campo (field-aligned) dentro do Blender,
com UX consistente e preservação de atributos para uso em produção.

## Backends
1) **QUADRIFLOW (fallback)** — disponível imediatamente (operador nativo do Blender).
2) **INSTANT (engine nativo)** — módulo Python nativo (pybind11) chamando um core C++.

## Funcionalidades (MVP v0.1)
- Operador Remesh (não-destrutivo): duplicar mesh, remesh no duplicado, manter/ocultar original
- UI no N-panel
- Parâmetros principais: densidade (faces/edge/ratio), simetria, preserve boundary/sharp, seed
- Pós-processo: transferir materiais, UV, cores (quando existirem)

## Funcionalidades (v0.2+)
- Batch/fila/cancelamento
- Guides (curvas) persistentes e overlay
- Presets e sugestão automática
- Densidade adaptativa (vertex group / textura) — plena no engine; limitada no fallback

## Engine nativo (contrato)
- `instant_meshes_py.remesh(verts, faces, options, guides=None) -> (out_verts, out_faces, meta)`
- `meta` inclui tempo, estatísticas e warnings
- Entrada preferencial: triangulada; saída: quads ou tri (com metadata)

## Critérios de aceitação gerais
- Não travar UI; sempre retornar erro tratável
- Resultados reprodutíveis quando `deterministic`/`seed` configurados
- Preservação de atributos funcionando (ou degradando com warnings claros)

