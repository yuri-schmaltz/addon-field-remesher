# Guia de Contribuição — Field Remesher

Obrigado por considerar contribuir! Este documento fornece diretrizes para manter a qualidade do código e fluxo de trabalho consistentes.

## 📋 Sumário
- [Começando](#começando)
- [Configuração de Desenvolvimento](#configuração-de-desenvolvimento)
- [Fluxo de Trabalho](#fluxo-de-trabalho)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Convenções de Commit](#convenções-de-commit)
- [Pull Requests](#pull-requests)
- [Dúvidas?](#dúvidas)

## 🚀 Começando

### Pré-requisitos
- Blender 3.6 LTS ou 4.x instalado
- Python 3.11+ (para scripts auxiliares)
- Git
- Familiaridade com Blender Python API (`bpy`)

### Fork & Clone
```bash
# 1. Fork no GitHub: github.com/yuri-schmaltz/addon-field-remesher
# 2. Clone seu fork
git clone https://github.com/SEU_USUARIO/addon-field-remesher.git
cd addon-field-remesher/field-remesher

# 3. Configure upstream
git remote add upstream https://github.com/yuri-schmaltz/addon-field-remesher.git
```

## 💻 Configuração de Desenvolvimento

### 1. Validar Sintaxe
Execute o smoke test para garantir que não há erros básicos:
```bash
python scripts/smoke_test.py
```
✅ Todos os arquivos devem passar sem erros.

### 2. Empacotar Add-on
```bash
python scripts/package_addon.py
```
Resultado: `dist/field_remesher_addon.zip`

### 3. Instalar no Blender (Modo Dev)
**Opção A: Link simbólico (recomendado)**
```bash
# Windows (PowerShell Admin)
New-Item -ItemType SymbolicLink -Path "C:\Users\USUARIO\AppData\Roaming\Blender Foundation\Blender\4.x\scripts\addons\field_remesher" -Target "C:\path\to\addon-field-remesher\field-remesher\addon\field_remesher"

# Linux/macOS
ln -s /path/to/addon-field-remesher/field-remesher/addon/field_remesher ~/.config/blender/4.x/scripts/addons/
```

**Opção B: ZIP manual**
1. Instale o ZIP gerado via `Edit > Preferences > Add-ons > Install...`
2. Recarregue a cada mudança: Desative → Ative o add-on

### 4. Debug no Blender
```python
# No Blender Text Editor ou Console Python:
import sys
sys.path.append(r"C:\path\to\addon-field-remesher\field-remesher\addon")
import field_remesher
import importlib
importlib.reload(field_remesher)
```

## 🔄 Fluxo de Trabalho

### Criar Branch de Feature
```bash
git checkout -b feature/minha-feature
# ou
git checkout -b fix/corrigir-bug
```

### Fazer Mudanças
1. **Edite código** em `field-remesher/addon/field_remesher/`
2. **Teste no Blender**
3. **Valide sintaxe**: `python scripts/smoke_test.py`
4. **Empacote** (se necessário): `python scripts/package_addon.py`

### Commits Frequentes
```bash
git add .
git commit -m "feat(ui): adicionar preset 'Game-Ready'"
```

### Sincronizar com Upstream
```bash
git fetch upstream
git rebase upstream/main
```

## 📏 Padrões de Código

### Estilo Python
- **PEP 8** como base (indentação 4 espaços)
- Nomes de classes: `CamelCase`
- Funções/variáveis: `snake_case`
- Constantes: `UPPER_CASE`

### Blender Add-on Específico
- **Operadores**: `FIELDREMESHER_OT_nome_op`
- **Painéis**: `FIELDREMESHER_PT_nome_painel`
- **PropertyGroups**: `FieldRemesherSettings`

### Imports
- **Absolutos** para módulos do add-on: `from field_remesher.backend import ...`
- **Relativos** apenas dentro de subpacotes: `from .util import ...`
- **Ordem**: `bpy` > biblioteca padrão > terceiros > locais

### Exemplo
```python
import bpy
from bpy.types import Operator
from typing import Set

from field_remesher.util.context import get_view3d_override

class FIELDREMESHER_OT_remesh(Operator):
    bl_idname = "fieldremesher.remesh"
    bl_label = "Remesher"
    bl_description = "Executa remesh com quad flow limpo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context) -> Set[str]:
        # Implementação...
        return {'FINISHED'}
```

## 🧪 Testes

### 1. Smoke Test (Obrigatório)
Valida sintaxe Python de todos os arquivos:
```bash
python scripts/smoke_test.py
```

### 2. Teste Manual no Blender
- Abra `View3D > Sidebar (N) > Field Remesher`
- Teste casos:
  - ✅ Remesh com preset "Organic"
  - ✅ Remesh com "Keep Original" ON
  - ✅ Transferência de atributos (UVs, vColors)
  - ✅ Cancelar operação modal (ESC)
  - ✅ Objeto sem faces (mensagem de erro)

### 3. Testes de Compatibilidade
- Blender 3.6 LTS (versão mínima)
- Blender 4.x (versão atual)

## 📝 Convenções de Commit

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<escopo>): <mensagem curta>

[corpo opcional]

[rodapé opcional]
```

### Tipos
- `feat`: Nova feature
- `fix`: Correção de bug
- `docs`: Documentação
- `refactor`: Refatoração (sem mudança funcional)
- `test`: Testes
- `chore`: Manutenção (build, CI, etc.)
- `perf`: Melhoria de performance

### Exemplos
```bash
git commit -m "feat(ui): adicionar preset 'Hard-Surface'"
git commit -m "fix(backend): corrigir ImportError no quadriflow_backend"
git commit -m "docs(readme): atualizar instruções de instalação"
git commit -m "chore(ci): adicionar smoke test na CI"
```

### Breaking Changes
```bash
git commit -m "feat(api)!: mudar assinatura de remesh_with_instant

BREAKING CHANGE: Parâmetro 'guides' agora é obrigatório."
```

## 🔀 Pull Requests

### Antes de Submeter
- [ ] ✅ Smoke test passa: `python scripts/smoke_test.py`
- [ ] ✅ Add-on carrega no Blender sem erros
- [ ] ✅ Funcionalidade testada manualmente
- [ ] ✅ Commits seguem convenção
- [ ] ✅ Sem código comentado ou `TODO` desnecessários

### Criar PR
1. **Push** para seu fork: `git push origin feature/minha-feature`
2. Abra PR em: `https://github.com/yuri-schmaltz/addon-field-remesher/pulls`
3. **Preencha template**:
   - Descrição clara da mudança
   - Screenshots (se UI)
   - Testes realizados
   - Issue relacionada (se houver)

### Revisão
- CI deve passar (smoke test + empacotamento)
- Responda comentários construtivamente
- Force push (`git push --force`) após rebase é OK

## 🔧 Scripts Auxiliares

### Bump de Versão
```bash
# Incrementar patch (0.1.2 → 0.1.3)
python scripts/bump_version.py patch

# Incrementar minor (0.1.3 → 0.2.0)
python scripts/bump_version.py minor

# Dry run (preview)
python scripts/bump_version.py patch --dry-run
```
Atualiza: `__init__.py`, `blender_manifest.toml`, `CHANGELOG.md`

### Empacotamento Estrito
```bash
# Modo strict (valida imports e versões)
python scripts/package_addon.py --strict
```

## ❓ Dúvidas?

- 📖 Leia [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) para problemas comuns
- 📁 Veja [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) para entender a arquitetura
- 🐛 Abra uma Issue: [github.com/yuri-schmaltz/addon-field-remesher/issues](https://github.com/yuri-schmaltz/addon-field-remesher/issues)
- 💬 Pergunte no PR: taggue @yuri-schmaltz

## 📄 Licença
Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (veja [LICENSE](LICENSE)).

