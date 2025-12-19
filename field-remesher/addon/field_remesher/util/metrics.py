"""Sistema de métricas simples para benchmark e troubleshooting."""

import time
import json
import os
from pathlib import Path


class MetricsLogger:
    """Logger de métricas para operações de remesh."""

    def __init__(self):
        self.start_time = None
        self.metrics = {}

    def start(self, operation_name="remesh"):
        """Inicia contagem de tempo."""
        self.start_time = time.perf_counter()
        self.metrics = {
            "operation": operation_name,
            "timestamp": time.time(),
            "status": "running",
        }

    def record(self, key, value):
        """Registra uma métrica."""
        self.metrics[key] = value

    def finish(self, status="success"):
        """Finaliza métricas."""
        if self.start_time:
            elapsed = time.perf_counter() - self.start_time
            self.metrics["tempo_total_ms"] = round(elapsed * 1000, 2)
        self.metrics["status"] = status
        return self.metrics

    def log_to_console(self):
        """Imprime métricas no console."""
        print("[Field Remesher Metrics]")
        for k, v in self.metrics.items():
            print(f"  {k}: {v}")

    def save_to_csv(self, filepath=None):
        """Salva métricas em CSV (append)."""
        if filepath is None:
            # Padrão: $HOME/field_remesher_metrics.csv
            filepath = Path.home() / "field_remesher_metrics.csv"
        else:
            filepath = Path(filepath)

        file_exists = filepath.exists()

        try:
            with open(filepath, "a", encoding="utf-8") as f:
                if not file_exists:
                    # Cabeçalho
                    headers = list(self.metrics.keys())
                    f.write(",".join(headers) + "\n")
                # Linha de dados
                values = [str(self.metrics.get(k, "")) for k in self.metrics.keys()]
                f.write(",".join(values) + "\n")
        except Exception as e:
            print(f"[Field Remesher] Erro ao salvar métricas: {e}")


def get_mesh_stats(obj):
    """Retorna estatísticas do mesh."""
    if not obj or obj.type != "MESH":
        return {"vertices": 0, "faces": 0, "edges": 0}
    mesh = obj.data
    return {
        "vertices": len(mesh.vertices),
        "faces": len(mesh.polygons),
        "edges": len(mesh.edges),
    }
