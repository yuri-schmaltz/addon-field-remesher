import bpy


def transfer_attributes(src_obj, dst_obj, do_uv=True, do_vcol=True):
    """Transfere atributos via Data Transfer modifier e aplica.

    Observação:
    - Em diferentes versões do Blender, nomes de tipos/enumsets podem variar.
    - A estratégia aqui é ser pragmática: tentar UV e Color Attributes quando possível
      e degradar sem quebrar o fluxo.
    """
    if src_obj == dst_obj:
        return
    if src_obj.type != "MESH" or dst_obj.type != "MESH":
        return

    # Checagens prévias: apenas aplicar quando existirem dados relevantes
    has_uv = False
    has_vcol = False
    try:
        # Blender 3.x+
        has_uv = hasattr(src_obj.data, "uv_layers") and len(src_obj.data.uv_layers) > 0
    except Exception:
        has_uv = False
    try:
        # Compatibilidade: vertex_colors (antigo) ou color_attributes (novo)
        if hasattr(src_obj.data, "color_attributes"):
            has_vcol = len(src_obj.data.color_attributes) > 0
        elif hasattr(src_obj.data, "vertex_colors"):
            has_vcol = len(src_obj.data.vertex_colors) > 0
    except Exception:
        has_vcol = False

    actual_do_uv = do_uv and has_uv
    actual_do_vcol = do_vcol and has_vcol

    if not actual_do_uv and not actual_do_vcol:
        # Nada a transferir
        return

    mod = dst_obj.modifiers.new(name="FR_DataTransfer", type="DATA_TRANSFER")
    mod.object = src_obj
    mod.use_object_transform = False

    # Mapeamento robusto (pode variar por versão)
    try:
        mod.loop_mapping = "POLYINTERP_NEAREST"
    except Exception:
        pass

    mod.use_loop_data = True

    desired = set()
    if actual_do_uv:
        desired.add("UV")
    if actual_do_vcol:
        # Em algumas versões: VCOL / COLOR
        desired.add("VCOL")

    try:
        mod.data_types_loops = desired
    except Exception:
        # fallback: tenta apenas UV se falhar
        try:
            if do_uv:
                mod.data_types_loops = {"UV"}
        except Exception:
            pass

    # Aplica modifier
    ctx = bpy.context
    old_active = ctx.view_layer.objects.active
    try:
        ctx.view_layer.objects.active = dst_obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    finally:
        ctx.view_layer.objects.active = old_active
