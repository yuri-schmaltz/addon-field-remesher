def get_view3d_override(context, active_obj):
    """Cria override robusto para operadores que exigem contexto de View3D."""
    win = context.window
    scr = win.screen
    for area in scr.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    return {
                        "window": win,
                        "screen": scr,
                        "area": area,
                        "region": region,
                        "scene": context.scene,
                        "view_layer": context.view_layer,
                        "active_object": active_obj,
                        "object": active_obj,
                        "selected_objects": [active_obj],
                        "selected_editable_objects": [active_obj],
                    }
    return None
