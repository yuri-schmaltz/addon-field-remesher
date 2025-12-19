# Métricas e Benchmarking

O sistema de métricas do Field Remesher permite rastrear performance e diagnosticar problemas.

## Uso Automático

Todas as operações de remesh registram métricas automaticamente no console do Blender:

```
[Field Remesher Metrics]
  operation: remesh
  timestamp: 1734642000.123
  input_vertices: 1024
  input_faces: 2000
  mesh_name: Cube
  backend: QUADRIFLOW
  remesh_time_ms: 523.45
  transfer_time_ms: 12.34
  output_vertices: 1500
  output_faces: 3000
  output_name: Cube_REMESH
  total_time_ms: 550.12
  status: success
```

## Métricas Coletadas

- **tempo_total_ms**: Tempo total da operação (ms)
- **remesh_time_ms**: Tempo da etapa de remesh (ms)
- **transfer_time_ms**: Tempo de transferência de atributos (ms)
- **input_vertices/faces**: Tamanho do mesh de entrada
- **output_vertices/faces**: Tamanho do mesh de saída
- **backend**: Backend utilizado (QUADRIFLOW, INSTANT)
- **status**: success, error, cancelled
- **error_message**: Mensagem de erro (se aplicável)

## Modo Modal

O operador roda em modo modal por padrão:
- **ESC**: Cancela a operação em andamento
- **Header**: Mostra progresso ("Executando remesh...")
- **Console**: Imprime métricas após conclusão

## Salvando Métricas em CSV

Para salvar métricas em arquivo CSV (útil para benchmarking):

1. Edite `ops/remesh.py`
2. No método `modal()`, adicione após `self._metrics.log_to_console()`:
   ```python
   self._metrics.save_to_csv()  # Salva em ~/field_remesher_metrics.csv
   ```

## Benchmarking

Para comparar performance entre backends ou configurações:

1. Ative salvamento de CSV
2. Execute remesh em múltiplos objetos
3. Analise o arquivo `~/field_remesher_metrics.csv`

Métricas úteis:
- **total_time_ms**: Performance geral
- **remesh_time_ms**: Core do algoritmo
- **transfer_time_ms**: Overhead de transferência
- **output_faces/input_faces**: Fator de densidade

## Troubleshooting

Se operações estão lentas:
- Verifique `remesh_time_ms` vs `transfer_time_ms`
- Desabilite transferência de atributos quando não necessário
- Compare QUADRIFLOW vs INSTANT (quando disponível)
- Reduza `target_faces` ou use `RATIO` mode
