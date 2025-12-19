import bpy
from ..util.context import get_view3d_override


def run_quadriflow(context, obj, s):
    # Garantir modo objeto
    if obj.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    # Tenta setar o modo de remesh no mesh data (varia por versão)
    try:
        obj.data.remesh_mode = "QUAD"
    except Exception:
        pass

    override = get_view3d_override(context, obj)
    if override is None:
        # Tenta executar sem override; se falhar, retorna mensagem acionável
        kwargs = dict(
            use_mesh_symmetry=s.use_mesh_symmetry,
            use_preserve_sharp=s.use_preserve_sharp,
            use_preserve_boundary=s.use_preserve_boundary,
            preserve_attributes=s.preserve_attributes,
            smooth_normals=s.smooth_normals,
            mode=s.mode,
            target_ratio=s.target_ratio,
            target_edge_length=s.target_edge_length,
            target_faces=s.target_faces,
            seed=s.seed,
        )
        try:
            bpy.ops.object.quadriflow_remesh(**kwargs)
            return
        except Exception:
            raise RuntimeError(
                "Contexto View3D não encontrado. Abra uma janela View3D (Layout) e tente novamente."
            )

    kwargs = dict(
        use_mesh_symmetry=s.use_mesh_symmetry,
        use_preserve_sharp=s.use_preserve_sharp,
        use_preserve_boundary=s.use_preserve_boundary,
        preserve_attributes=s.preserve_attributes,
        smooth_normals=s.smooth_normals,
        mode=s.mode,
        target_ratio=s.target_ratio,
        target_edge_length=s.target_edge_length,
        target_faces=s.target_faces,
        seed=s.seed,
    )

    with context.temp_override(**override):
        bpy.ops.object.quadriflow_remesh(**kwargs)
