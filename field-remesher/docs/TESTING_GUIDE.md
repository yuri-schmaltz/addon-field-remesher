# Guia de Teste Rápido

## Preparação

1. Empacotar add-on atualizado:
```powershell
python field-remesher/scripts/package_addon.py
```

2. Instalar no Blender:
   - Edit → Preferences → Add-ons → Install...
   - Selecionar `field-remesher/dist/field_remesher_addon.zip`
   - Ativar "Field Remesher (Instant-like)"

3. Abrir Console do Sistema (para ver métricas):
   - Window → Toggle System Console

## Testes de Funcionalidade

### Teste 1: Operação Modal com Progresso ✓
```
1. Cena padrão do Blender (Cubo)
2. Selecionar cubo
3. Sidebar (N) → Field Remesher
4. Clicar "Remesh (Field Remesher)"
5. Observar header superior: "Executando remesh..."
6. Aguardar conclusão
7. Verificar console: [Field Remesher Metrics]
```

**Resultado esperado**:
- Header mostra progresso
- Console imprime métricas completas
- Novo objeto `Cube_REMESH` criado
- Original oculto

### Teste 2: Cancelamento com ESC ✓
```
1. Adicionar mesh densa: Add → Mesh → UV Sphere (subdivisions: 6)
2. Selecionar esfera
3. Target Faces: 50000 (alto para garantir tempo de execução)
4. Clicar "Remesh (Field Remesher)"
5. IMEDIATAMENTE pressionar ESC
6. Verificar mensagem: "Operação cancelada pelo usuário."
```

**Resultado esperado**:
- Operação cancela
- Sem objetos órfãos
- Console mostra `status: cancelled`

### Teste 3: Rollback em Falha ✓
```
1. Selecionar cubo
2. Fechar TODAS as janelas 3D View (deixar apenas preferências/outliner)
3. Tentar executar remesh
4. Verificar erro: "Contexto View3D não encontrado. Abra uma janela View3D..."
5. Verificar que cubo original está visível
6. Verificar que não há Cube_REMESH órfão
```

**Resultado esperado**:
- Mensagem acionável
- Estado restaurado
- Sem duplicados

### Teste 4: Otimização de Atributos ✓
```
# Caso A: Mesh sem UVs
1. Add → Mesh → Cube (padrão, sem UVs criados manualmente)
2. Remesh
3. Verificar console: transfer_time_ms deve ser ~0 ou muito baixo

# Caso B: Mesh com UVs
1. Add → Mesh → UV Sphere
2. Remesh (sphere tem UVs por padrão)
3. Verificar console: transfer_time_ms > 0
```

**Resultado esperado**:
- Sem UVs: transferência pulada ou muito rápida
- Com UVs: transferência executada

### Teste 5: Métricas Detalhadas ✓
```
1. Remesh um objeto qualquer
2. Verificar console para métricas:
   - operation: remesh
   - timestamp: <unix time>
   - input_vertices: <número>
   - input_faces: <número>
   - mesh_name: <nome>
   - backend: QUADRIFLOW
   - remesh_time_ms: <tempo>
   - transfer_time_ms: <tempo>
   - output_vertices: <número>
   - output_faces: <número>
   - output_name: <nome>_REMESH
   - total_time_ms: <tempo>
   - status: success
```

## Benchmark Comparativo

### Setup
```python
# No Blender Text Editor, criar script:
import bpy
import time

# Lista de meshes para testar
test_objects = [
    ("Cube", 8, 6),           # Simples
    ("Sphere_3", 482, 480),   # Médio (UV Sphere, subdiv=3)
    ("Sphere_5", 7682, 7680), # Denso (UV Sphere, subdiv=5)
]

results = []

for name, expected_v, expected_f in test_objects:
    # Criar objeto
    if "Cube" in name:
        bpy.ops.mesh.primitive_cube_add()
    else:
        subdiv = int(name.split("_")[1])
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16)
        obj = bpy.context.active_object
        # Subdividir se necessário (manual ou modifier)
    
    # Executar remesh
    start = time.time()
    bpy.ops.fieldremesher.remesh('INVOKE_DEFAULT')
    # Aguardar conclusão (na prática, verificar console)
    
    print(f"{name}: Ver métricas no console")

# Comparar remesh_time_ms entre objetos
```

### Análise
- **Pequenos (<1k faces)**: < 100ms
- **Médios (1k-10k faces)**: 100-500ms
- **Grandes (>10k faces)**: > 500ms

## Problemas Comuns e Soluções

### Problema: "Selecione um objeto Mesh"
**Solução**: Selecionar um objeto do tipo MESH no viewport

### Problema: "Contexto View3D não encontrado"
**Solução**: Abrir uma janela 3D View (Layout padrão)

### Problema: Operação não cancela com ESC
**Solução**: 
- Verificar que modal está ativo (header mostra mensagem)
- Em meshes muito pequenas, operação termina antes de ESC

### Problema: Métricas não aparecem no console
**Solução**: 
- Windows: Window → Toggle System Console
- Linux/Mac: Executar Blender via terminal

## Validação de Código

```powershell
# Verificar sintaxe Python
python -m py_compile field-remesher/addon/field_remesher/ops/remesh.py
python -m py_compile field-remesher/addon/field_remesher/util/metrics.py
python -m py_compile field-remesher/addon/field_remesher/util/transfer.py
python -m py_compile field-remesher/addon/field_remesher/backend/quadriflow_backend.py
```

**Resultado esperado**: Sem erros

## Checklist Final

- [ ] Add-on empacota sem erros
- [ ] Add-on instala no Blender
- [ ] Painel aparece no Sidebar (N)
- [ ] Remesh básico funciona (cubo padrão)
- [ ] Header mostra progresso
- [ ] ESC cancela operação
- [ ] Métricas aparecem no console
- [ ] Rollback funciona em falhas
- [ ] Mensagens são acionáveis (pt-BR)
- [ ] Sem erros no console do Blender

## Relatório de Teste

Após executar todos os testes, preencher:

```
Data: ___/___/___
Blender Version: ___
SO: Windows / Linux / macOS

✓ = Pass, ✗ = Fail, ~ = Partial

[ ] Teste 1: Modal com progresso
[ ] Teste 2: Cancelamento ESC
[ ] Teste 3: Rollback em falha
[ ] Teste 4: Otimização de atributos
[ ] Teste 5: Métricas detalhadas

Notas:
_______________________________________
_______________________________________
_______________________________________
```
