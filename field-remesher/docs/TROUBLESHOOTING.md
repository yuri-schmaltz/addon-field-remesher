# Troubleshooting - Field Remesher

Guia de resolução de problemas comuns do Field Remesher.

## 🚨 Problemas Comuns

### Add-on não aparece no Blender

**Sintomas:** Após instalar o ZIP, o add-on não está listado em Preferências → Add-ons.

**Soluções:**
1. **Verifique a versão do Blender:** O add-on requer Blender 3.6 LTS ou superior.
2. **Procure por "Field Remesher":** Use a barra de busca em Add-ons.
3. **Verifique erros no Console:**
   - Abra `Window → Toggle System Console` (Windows) ou inicie o Blender via terminal
   - Procure por `ImportError` ou `SyntaxError` relacionados a `field_remesher`
4. **Reinstale o add-on:**
   - Remova o add-on existente (se listado)
   - Feche e reabra o Blender
   - Instale novamente o ZIP

### Painel não visível na Sidebar

**Sintomas:** Add-on ativado, mas painel "Field Remesher" não aparece na Sidebar (N).

**Soluções:**
1. **Abra a Sidebar:** Pressione `N` na View3D ou clique no ícone `>` no canto superior direito.
2. **Procure a aba "Field Remesher":** Role as abas até encontrar.
3. **Verifique o modo:** Certifique-se de estar em Object Mode com um objeto mesh selecionado.

### Operação de Remesh falha ou trava

**Sintomas:** Ao clicar em "Remesher", nada acontece ou o Blender trava.

**Soluções:**
1. **Verifique a densidade:** Valores muito altos (>100k faces) podem travar. Comece com 1k-10k.
2. **Mesh válida:** Certifique-se de que o objeto tem geometria (vértices e faces).
3. **Modo Object:** O remesh só funciona em Object Mode.
4. **Console de erros:** Verifique mensagens de erro no Console do sistema.
5. **Cancelamento:** Se travar, pressione `ESC` (se o modal estiver ativo) ou reinicie o Blender.

### Mensagem "Erro de contexto" no Quadriflow

**Sintomas:** `Erro: contexto View3D indisponível para Quadriflow`

**Soluções:**
1. **Abra uma janela 3D View:** O Quadriflow requer uma View3D ativa.
2. **Tente novamente:** A primeira tentativa pode falhar; tente executar novamente.
3. **Fallback automático:** O add-on tenta executar sem override em fallback.

### Atributos não transferidos (UVs, cores)

**Sintomas:** Após o remesh, o objeto perde UVs ou cores de vértices.

**Soluções:**
1. **Ative "Transferir Atributos":** Certifique-se de que a opção está marcada nas configurações.
2. **Verifique se o original possui atributos:** Se o original não tem UVs, não há o que transferir.
3. **Data Transfer Modifier:** Inspecione o modifier aplicado e ajuste configurações manualmente se necessário.

### Rollback não funciona

**Sintomas:** Após erro, o objeto duplicado órfão permanece na cena.

**Soluções:**
1. **Limpeza manual:** Selecione e delete o objeto `<nome>_REMESH`.
2. **Reporte o bug:** Se o rollback falhar consistentemente, abra uma issue com passos para reproduzir.

### Preset não muda configurações

**Sintomas:** Selecionar um preset não atualiza os parâmetros visíveis.

**Soluções:**
1. **Verifique a versão do add-on:** Presets foram adicionados na v0.1.1+.
2. **Reabra o painel:** Feche e reabra a Sidebar (`N`).
3. **Modo Custom:** Se o preset for "Custom", os valores não mudam automaticamente.

### Engine nativo (Instant) não disponível

**Sintomas:** Backend "INSTANT" não aparece nas preferências ou está desabilitado.

**Soluções:**
1. **Funcionalidade futura:** O engine nativo ainda não está implementado (v0.1.x).
2. **Use Quadriflow:** Selecione backend "AUTO" ou "QUADRIFLOW" enquanto o nativo não está disponível.
3. **Acompanhe o Roadmap:** Veja `ROADMAP.md` para status do engine nativo.

## 🐛 Reportando Novos Problemas

Se o seu problema não está listado acima, por favor reporte uma issue no GitHub incluindo:

### Informações Essenciais
- **Versão do Blender:** Ex: 4.2.5 LTS
- **Versão do add-on:** Ex: 0.1.2 (veja em Preferências → Add-ons)
- **Sistema operacional:** Windows 11 / Ubuntu 22.04 / macOS 14
- **Passos para reproduzir:**
  1. Abrir Blender
  2. Adicionar cubo padrão
  3. Clicar em "Remesher" com densidade 50k
  4. Observar erro X

### Informações Úteis
- **Logs do Console:** Copie mensagens de erro relevantes
- **Screenshots:** Capture o estado da UI e erros visuais
- **Arquivo .blend:** Se possível, anexe um arquivo mínimo que reproduz o problema

## 📊 Métricas e Diagnóstico

O add-on inclui um sistema de métricas para troubleshooting. Para ativar:

1. **Abra o Console do Sistema:**
   - Windows: `Window → Toggle System Console`
   - Linux/macOS: Inicie o Blender via terminal

2. **Execute o remesh:**
   - As métricas serão impressas automaticamente no console

3. **Analise o output:**
```
=== Field Remesher Metrics ===
Object: Cube_REMESH
Faces: 500 → 1024 (delta: +524)
Vertices: 502 → 1026 (delta: +524)
Backend: QUADRIFLOW
Remesh Time: 0.234s
Transfer Time: 0.089s
Total Time: 0.323s
Status: SUCCESS
```

4. **Compartilhe as métricas:** Ao reportar bugs, inclua este output.

## 🔧 Ferramentas de Diagnóstico

### Smoke Test (Validação de Sintaxe)
Executa validação de sintaxe de todos os módulos Python:

```bash
python field-remesher/scripts/smoke_test.py
```

**Output esperado:** `✅ Todos os X arquivos Python têm sintaxe válida!`

### Empacotamento com Validação
Empacota o add-on com validação estrita de imports:

```bash
python field-remesher/scripts/package_addon.py --strict
```

**Output esperado:** `OK: <path>/field_remesher_addon.zip`

## 💬 Suporte

- **Issues:** https://github.com/yuri-schmaltz/addon-field-remesher/issues
- **Discussions:** https://github.com/yuri-schmaltz/addon-field-remesher/discussions

---

**Ainda com problemas?** Abra uma issue detalhada e ajudaremos a resolver!
