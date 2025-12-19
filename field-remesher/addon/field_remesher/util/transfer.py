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
    if do_uv:
        desired.add("UV")
    if do_vcol:
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
