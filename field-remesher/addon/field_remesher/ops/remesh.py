import bpy
import time
from bpy.types import Operator

from ..backend import instant_available, run_quadriflow, run_instant_engine
from ..util.transfer import transfer_attributes
from ..util.metrics import MetricsLogger, get_mesh_stats


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

    _timer = None
    _cancelled = False
    _executing = False
    _metrics = None
    _step = "init"
    _progress_msg = ""

    def invoke(self, context, event):
        """Inicia operação modal."""
        src = context.active_object
        if not src or src.type != "MESH":
            self.report({"ERROR"}, "Selecione um objeto Mesh.")
            return {"CANCELLED"}

        # Inicializa métricas
        self._metrics = MetricsLogger()
        self._metrics.start("remesh")

        # Captura estatísticas do mesh de entrada
        input_stats = get_mesh_stats(src)
        self._metrics.record("input_vertices", input_stats["vertices"])
        self._metrics.record("input_faces", input_stats["faces"])
        self._metrics.record("mesh_name", src.name)

        # Preferências
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences
        backend = prefs.backend
        if backend == "AUTO":
            backend = "INSTANT" if instant_available() else "QUADRIFLOW"
        self._metrics.record("backend", backend)

        # Prepara execução modal
        self._cancelled = False
        self._executing = False
        self._step = "init"
        self._progress_msg = "Iniciando remesh..."

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        """Loop modal com progresso e cancelamento."""
        if event.type == "ESC":
            self._cancelled = True
            self._progress_msg = "Cancelando..."
            context.area.header_text_set(None)
            self.cancel(context)
            self.report({"INFO"}, "Operação cancelada pelo usuário.")
            if self._metrics:
                self._metrics.finish("cancelled")
                self._metrics.log_to_console()
            return {"CANCELLED"}

        if event.type == "TIMER" and not self._executing:
            # Executa o remesh uma única vez
            self._executing = True
            self._progress_msg = "Executando remesh..."
            context.area.header_text_set(self._progress_msg)

            try:
                result = self._do_remesh(context)
                if result == {"FINISHED"}:
                    # Sucesso
                    self._metrics.finish("success")
                    self._metrics.log_to_console()
                    context.area.header_text_set(None)
                    self.cancel(context)
                    return {"FINISHED"}
                else:
                    # Falha
                    self._metrics.finish("error")
                    self._metrics.log_to_console()
                    context.area.header_text_set(None)
                    self.cancel(context)
                    return {"CANCELLED"}
            except Exception as e:
                self.report({"ERROR"}, f"Erro inesperado: {e}")
                self._metrics.finish("error")
                self._metrics.log_to_console()
                context.area.header_text_set(None)
                self.cancel(context)
                return {"CANCELLED"}

        return {"RUNNING_MODAL"}

    def cancel(self, context):
        """Limpa timer ao cancelar."""
        if self._timer:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
            self._timer = None

    def _do_remesh(self, context):
        """Executa o remesh (lógica original do execute)."""
        # Marca etapa e tempo
        t_start = time.perf_counter()
        self._step = "prepare"
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
            self._step = "remeshing"
            t_remesh_start = time.perf_counter()
            
            if backend == "QUADRIFLOW":
                run_quadriflow(context, dst, s)
            else:
                run_instant_engine(dst, s, guides=None)
            
            t_remesh = (time.perf_counter() - t_remesh_start) * 1000
            self._metrics.record("remesh_time_ms", round(t_remesh, 2))

            # Pós: transferência de atributos (padrão robusto)
            self._step = "transfer"
            t_transfer_start = time.perf_counter()
            
            if s.transfer_uv or s.transfer_vcol:
                transfer_attributes(src, dst, do_uv=s.transfer_uv, do_vcol=s.transfer_vcol)
            
            t_transfer = (time.perf_counter() - t_transfer_start) * 1000
            self._metrics.record("transfer_time_ms", round(t_transfer, 2))

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
            self._metrics.record("error_message", str(e))
            return {"CANCELLED"}

        # Métricas finais
        output_stats = get_mesh_stats(dst)
        self._metrics.record("output_vertices", output_stats["vertices"])
        self._metrics.record("output_faces", output_stats["faces"])
        self._metrics.record("output_name", dst.name)

        elapsed = (time.perf_counter() - t_start) * 1000
        self._metrics.record("total_time_ms", round(elapsed, 2))

        self.report({"INFO"}, f"Remesh concluído: {dst.name} ({output_stats['faces']} faces)")
        return {"FINISHED"}

    def execute(self, context):
        """Execução direta (fallback sem modal)."""
        # Redireciona para o método interno
        self._metrics = MetricsLogger()
        self._metrics.start("remesh_direct")
        result = self._do_remesh(context)
        if result == {"FINISHED"}:
            self._metrics.finish("success")
        else:
            self._metrics.finish("error")
        self._metrics.log_to_console()
        return result
