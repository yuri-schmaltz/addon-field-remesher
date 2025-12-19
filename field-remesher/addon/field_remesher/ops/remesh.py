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
        if s.keep_original:
            src.hide_set(True)

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
            self.report({"ERROR"}, f"Falha no remesh: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Remesh concluído: {dst.name}")
        return {"FINISHED"}
