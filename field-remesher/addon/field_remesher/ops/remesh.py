import bpy
from bpy.types import Operator

from ..backend import instant_available, run_quadriflow, run_instant_engine
from ..util.transfer import transfer_attributes


def _dup_object(context, src_obj, suffix="_REMESH"):
    new_obj = src_obj.copy()
    new_obj.data = src_obj.data.copy()
    new_obj.name = f"{src_obj.name}{suffix}"
    context.collection.objects.link(new_obj)
    return new_obj


class FIELDREMESHER_OT_remesh(Operator):
    bl_idname = "fieldremesher.remesh"
    bl_label = "Remesh (Field Remesher)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Preferências do add-on
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        s = context.scene.fieldremesher_settings

        src = context.active_object
        if not src or src.type != "MESH":
            self.report({"ERROR"}, "Selecione um objeto Mesh.")
            return {"CANCELLED"}

        # Estado anterior (para rollback em caso de falha)
        old_active = context.view_layer.objects.active
        old_selected_names = [o.name for o in context.selected_objects]
        src_hidden_before = src.hide_get()

        # Decide backend
        backend = prefs.backend
        if backend == "AUTO":
            backend = "INSTANT" if instant_available() else "QUADRIFLOW"

        # Não-destrutivo: duplicar
        dst = _dup_object(context, src)
        for o in context.selected_objects:
            o.select_set(False)
        dst.select_set(True)
        context.view_layer.objects.active = dst

        # Ocultar original (se solicitado)
        did_hide_src = False
        if s.keep_original:
            try:
                src.hide_set(True)
                did_hide_src = True
            except Exception:
                did_hide_src = False

        try:
            if backend == "QUADRIFLOW":
                run_quadriflow(context, dst, s)
            else:
                run_instant_engine(dst, s, guides=None)

            # Pós: transferência de atributos (padrão robusto)
            if s.transfer_uv or s.transfer_vcol:
                transfer_attributes(src, dst, do_uv=s.transfer_uv, do_vcol=s.transfer_vcol)

            if s.smooth_normals:
                try:
                    bpy.ops.object.shade_smooth()
                except Exception:
                    pass

        except Exception as e:
            # Rollback: restaurar visibilidade do original, remover duplicado e restaurar seleção/ativo
            try:
                if did_hide_src and not src_hidden_before:
                    src.hide_set(False)
            except Exception:
                pass

            try:
                # Remover objeto duplicado com segurança
                if dst is not None:
                    # Desvincula e remove o objeto; remove mesh data se possível
                    import bpy
                    if dst.name in bpy.data.objects:
                        bpy.data.objects.remove(bpy.data.objects[dst.name], do_unlink=True)
                    try:
                        if dst.data and dst.data.name in bpy.data.meshes:
                            bpy.data.meshes.remove(bpy.data.meshes[dst.data.name])
                    except Exception:
                        pass
            except Exception:
                pass

            # Restaurar seleção e ativo
            try:
                for o in context.selected_objects:
                    o.select_set(False)
                for name in old_selected_names:
                    obj = bpy.data.objects.get(name)
                    if obj:
                        obj.select_set(True)
                if old_active and old_active.name in bpy.data.objects:
                    context.view_layer.objects.active = bpy.data.objects[old_active.name]
            except Exception:
                pass

            self.report({"ERROR"}, f"Falha no remesh: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Remesh concluído: {dst.name}")
        return {"FINISHED"}
