# Changelog

## v0.1.3 — Dev Tooling & Documentation (Janeiro 2025)

### 🛠️ Developer Experience
- **Smoke Test**: Validação de sintaxe Python sem dependências do Blender
- **CI Integration**: Smoke test executado automaticamente antes do empacotamento
- **Bump Version Script**: Automação de incremento de versão (major/minor/patch)
- **CHANGELOG Validation**: Modo `--strict` valida entrada de versão no CHANGELOG

### 📚 Documentação
- **README**: Expandido com exemplos de uso (retopo, game, CAD)
- **README**: Adicionada seção "Desenvolvimento Local" com setup detalhado
- **CONTRIBUTING.md**: Guia completo de contribuição (200+ linhas)
- **TROUBLESHOOTING.md**: Guia de resolução de problemas comuns

### 🔧 Scripts
- `scripts/smoke_test.py`: Validação de sintaxe com py_compile
- `scripts/bump_version.py`: Atualiza `__init__.py`, `blender_manifest.toml` e `CHANGELOG.md`
- `scripts/package_addon.py`: Validação de CHANGELOG em modo `--strict`


## [0.1.2] — Fix ImportError (Janeiro 2025)

### 🐛 Correções
- **ImportError no Blender 5.x**: Corrigido import relativo em `ui.py` (`.backend` em vez de `..backend`)

## v0.1.1 — Quick Wins + Modal + Métricas (Dezembro 2025)

### 🎯 Melhorias de UX
- **Operador Modal**: `invoke()` com loop modal para progresso e cancelamento
- **Cancelamento**: Pressione `ESC` para interromper operações longas
- **Mensagens Acionáveis**: Erros contextuais orientam o usuário
- **Progresso Visual**: Header mostra "Executando remesh..."

### 🛡️ Confiabilidade
- **Rollback Robusto**: Estado restaurado completamente em caso de falha
- **Limpeza Automática**: Remove duplicados órfãos em erros
- **Fallback View3D**: Tenta executar sem override quando possível

### ⚡ Performance
- **Otimização de Transferência**: Checa atributos antes de aplicar
- **Redução de Overhead**: ~10-30% em meshes sem UVs/cores
- **Timing Detalhado**: Métricas por etapa (remesh, transfer)

### 📊 Observabilidade
- **Sistema de Métricas**: Logger automático em todas operações
- **Output no Console**: Timing, vértices/faces, backend, status
- **Troubleshooting**: Mensagens de erro detalhadas
- **CSV Export**: Suporte opcional para benchmarking

### 📚 Documentação
- Adicionado `docs/METRICS.md` - Sistema de métricas
- Adicionado `docs/IMPROVEMENTS_SUMMARY.md` - Resumo técnico
- Adicionado `docs/TESTING_GUIDE.md` - Guia de validação
- Atualizado README com funcionalidades

### 🔧 Arquivos Modificados
- `ops/remesh.py` - Modal + Métricas + Rollback
- `util/transfer.py` - Pré-checagens de atributos
- `util/metrics.py` - Sistema de métricas [NOVO]
- `backend/quadriflow_backend.py` - Fallback + mensagens

### ✅ Compatibilidade
- Blender 3.6 LTS e 4.x
- Windows/Linux/macOS
- Backward compatible

## Unreleased
- Initial scaffold.

