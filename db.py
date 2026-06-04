from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class PlantLog:
    id: int
    user_id: int
    plant_name: str
    health_score: int
    diagnosis: str
    action: str
    created_at: str


class Database:
    def __init__(self, path: str = "greenbuddy.db") -> None:
        self.path = Path(path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS plants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS plant_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    plant_name TEXT NOT NULL,
                    health_score INTEGER NOT NULL,
                    diagnosis TEXT NOT NULL,
                    action TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS user_state (
                    user_id INTEGER PRIMARY KEY,
                    plant_name TEXT,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def set_current_plant(self, user_id: int, plant_name: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO user_state (user_id, plant_name, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id)
                DO UPDATE SET plant_name = excluded.plant_name, updated_at = excluded.updated_at
                """,
                (user_id, plant_name, self._now()),
            )
            connection.execute(
                """
                INSERT INTO plants (user_id, name, created_at)
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM plants WHERE user_id = ? AND lower(name) = lower(?)
                )
                """,
                (user_id, plant_name, self._now(), user_id, plant_name),
            )
            connection.commit()

    def get_current_plant(self, user_id: int) -> str:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT plant_name FROM user_state WHERE user_id = ?",
                (user_id,),
            ).fetchone()
        if row and row["plant_name"]:
            return str(row["plant_name"])
        return "My plant"

    def add_log(self, user_id: int, plant_name: str, analysis: dict[str, Any]) -> None:
        health_score = int(analysis.get("health_score", 50))
        diagnosis = str(analysis.get("diagnosis", "No diagnosis"))
        action = str(analysis.get("care_action", "Observe the plant and check watering."))

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO plant_logs (user_id, plant_name, health_score, diagnosis, action, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, plant_name, health_score, diagnosis, action, self._now()),
            )
            connection.commit()

    def get_logs(self, user_id: int, limit: int = 20) -> list[PlantLog]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, user_id, plant_name, health_score, diagnosis, action, created_at
                FROM plant_logs
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        return [PlantLog(**dict(row)) for row in rows]
