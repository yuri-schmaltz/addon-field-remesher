# Field Remesher (Instant-like) — Blender Add-on

[![CI](https://github.com/yuri-schmaltz/addon-field-remesher/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/yuri-schmaltz/addon-field-remesher/actions/workflows/ci.yml)

Add-on para Blender (3.6 LTS+ e 4.x) que entrega retopologia quad “field-aligned” **estilo Instant Meshes**,
com **fallback imediato** via Quadriflow e um **backend nativo opcional** (engine) para paridade avançada.

## Status
- ✅ Fallback Quadriflow: funcional (MVP)
- 🧩 Engine nativo: estrutura pronta (stub). Requer implementar/compilar bindings e core.
- ✅ Roadmap e backlog (GitHub) incluídos em `ROADMAP.md` e `docs/github_backlog.csv`

## Estrutura do repositório
- `addon/` — código do add-on (instalável no Blender)
- `native/` — esqueleto para bindings (pybind11) + core (submodule / fork do upstream)
- `scripts/` — empacotamento e build do módulo nativo
- `.github/` — templates de issues e workflow básico
- `docs/` — especificação, compatibilidade, backlog importável, etc.

## Instalação

### Download via GitHub Releases
1. Acesse [Releases](https://github.com/yuri-schmaltz/addon-field-remesher/releases)
2. Baixe `field_remesher_addon.zip` da versão desejada
3. No Blender: `Edit > Preferences > Add-ons > Install...`
4. Selecione o ZIP baixado
5. Ative o add-on: **Field Remesher (Instant-like)**
6. Painel: `View3D > Sidebar (N) > Field Remesher`

### Build Local (Desenvolvimento)
```bash
python scripts/package_addon.py
```
Saída: `dist/field_remesher_addon.zip`

## 🚀 Uso Rápido

### Remesh Básico
1. Selecione um objeto mesh na View3D
2. Abra a Sidebar (`N`) → aba "Field Remesher"
3. **Escolha um preset** (opcional):
   - `Organic` - Para modelos orgânicos (caracteres, criaturas)
   - `Hard-Surface` - Objetos mecânicos e arquitetônicos
   - `Game-Ready` - Otimizado para tempo real
   - `High-Detail` - Preservação máxima de detalhes
   - `Custom` - Configuração manual
4. **Ajuste a densidade**:
   - `Faces Mode`: Número alvo de faces (ex: 5000)
   - `Edge Mode`: Comprimento médio de arestas (ex: 0.02)
   - `Ratio Mode`: Proporção de redução (ex: 0.5 = 50%)
5. Clique em **"Remesher"**
6. Aguarde (progresso aparece no header)
7. Pressione `ESC` para cancelar se necessário

### Transferência de Atributos
- **Ative "Transferir Atributos"** para preservar:
  - UVs
  - Cores de vértices
  - Normais

### Opções Avançadas
(Disponível se habilitado em Preferências → Add-ons → Field Remesher)
- **Smooth Normals**: Suavizar normais após remesh
- **Symmetry**: Tentar preservar simetria
- **Keep Original**: Manter mesh original oculta

## 📖 Exemplos de Uso

### Exemplo 1: Retopologia de Escultura
```
Cenário: Escultura high-poly (500k faces) precisa de retopo limpa.

Passos:
1. Selecione a escultura
2. Preset: "High-Detail"
3. Density: 10000 faces
4. Transfer Attributes: ON
5. Remesher → resultado: 10k quads uniformes
```

### Exemplo 2: Otimização para Game
```
Cenário: Asset com 50k tris precisa rodar em mobile (target: 5k tris).

Passos:
1. Selecione o asset
2. Preset: "Game-Ready"
3. Mode: Ratio
4. Density: 0.1 (10% das faces originais)
5. Remesher → resultado: ~5k faces otimizadas
```

### Exemplo 3: Limpeza de Mesh CAD
```
Cenário: Modelo CAD importado com topologia irregular.

Passos:
1. Selecione o modelo
2. Preset: "Hard-Surface"
3. Mode: Edge Length
4. Density: 0.05 (arestas de 5cm)
5. Smooth Normals: ON
6. Remesher → topologia limpa e uniforme
```

## 💻 Desenvolvimento Local

### Requisitos
- Blender 3.6 LTS ou 4.x
- Python 3.11+
- Git

### Setup
```bash
# Clone
git clone https://github.com/yuri-schmaltz/addon-field-remesher.git
cd addon-field-remesher/field-remesher

# Smoke test (validação de sintaxe)
python scripts/smoke_test.py

# Empacote
python scripts/package_addon.py

# Instale o ZIP gerado no Blender
```

### Estrutura
```
field-remesher/
├── addon/field_remesher/        # Código do add-on
│   ├── __init__.py              # Registro e bl_info
│   ├── properties.py            # PropertyGroups
│   ├── preferences.py           # AddonPreferences
│   ├── ui.py                    # Painéis da Sidebar
│   ├── ops/                     # Operadores
│   │   ├── remesh.py            # Op principal (modal)
│   │   └── preset_ops.py        # Ops de presets
│   ├── backend/                 # Implementações de remesh
│   │   ├── quadriflow_backend.py
│   │   └── instant_backend.py   # (stub)
│   └── util/                    # Utilitários
│       ├── context.py           # View3D override
│       ├── transfer.py          # Transferência de attrs
│       └── metrics.py           # Sistema de métricas
├── scripts/                     # Scripts auxiliares
│   ├── package_addon.py         # Empacotamento
│   ├── bump_version.py          # Bump de versão
│   └── smoke_test.py            # Validação de sintaxe
├── native/                      # Engine nativo (futuro)
└── docs/                        # Documentação técnica
```

### Workflow de Desenvolvimento
Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes completos.

## Instalação (fallback)
1. No Blender: `Edit > Preferences > Add-ons > Install...`
2. Selecione o **zip do add-on** gerado por `scripts/package_addon.py` (ou compacte a pasta `addon/`).
3. Ative o add-on: **Field Remesher (Instant-like)**.
4. Painel: `View3D > Sidebar (N) > Field Remesher`.

## Gerar zip instalável do add-on
No terminal (Python 3.x):
```bash
python scripts/package_addon.py
```
Saída: `dist/field_remesher_addon.zip`

## Backend Engine nativo (opcional)
A estrutura está em `native/`. Para ativar o backend INSTANT:
1) implemente o core (ou traga o upstream via submodule/fork),
2) compile o módulo `instant_meshes_py`,
3) copie o binário para `addon/field_remesher/binaries/<platform>/`,
4) selecione backend **AUTO** ou **INSTANT** nas preferências do add-on.

Veja: `native/README.md`.

## Licenças
- Código do add-on: `LICENSE` (GPL-3.0-or-later recomendado para Blender)
- Terceiros: `LICENSES/` (inclua upstream do engine quando adicionar)

