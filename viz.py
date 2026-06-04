from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .db import PlantLog


def create_health_chart(logs: list[PlantLog], output_path: str = "tmp/health_chart.png") -> str:
    if not logs:
        raise ValueError("No logs available for chart")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    ordered_logs = list(reversed(logs))
    x_values = list(range(1, len(ordered_logs) + 1))
    y_values = [log.health_score for log in ordered_logs]

    plt.figure(figsize=(8, 4.5))
    plt.plot(x_values, y_values, marker="o")
    plt.title("Plant health progress")
    plt.xlabel("Observation")
    plt.ylabel("Health score")
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
    return output_path
