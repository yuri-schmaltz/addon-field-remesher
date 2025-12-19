# Compatibilidade

## Blender
- Suportado: Blender **3.6 LTS** e **4.x**
- Operador fallback: `bpy.ops.object.quadriflow_remesh` (disponível nas versões citadas)

## Sistemas operacionais
- Windows / Linux / macOS (fallback)
- Backend nativo: requer build por plataforma e por versão do Python embutido no Blender.

## Observações ABI
- Binários do módulo nativo devem ser compilados contra o Python do Blender (mesma versão/ABI).
- Política recomendada: artefatos por versão de Blender (ex.: 3.6, 4.0, 4.1...).

