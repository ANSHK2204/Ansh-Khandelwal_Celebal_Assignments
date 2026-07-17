"""
Drive Wise - Query Logger
SQLite-based logging for user queries, response times, and system metrics.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from app.config import LOG_DB_PATH


class QueryLogger:
    """Manages SQLite logging for Drive Wise query monitoring."""

    def __init__(self, db_path: str = LOG_DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Create a new database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize the logging database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                query TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                response_time_ms REAL NOT NULL,
                chunks_retrieved INTEGER DEFAULT 0,
                status TEXT DEFAULT 'success',
                sources_used TEXT DEFAULT '[]',
                answer_preview TEXT DEFAULT '',
                error_message TEXT DEFAULT ''
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_log_id INTEGER NOT NULL,
                context_relevance REAL DEFAULT 0.0,
                answer_groundedness REAL DEFAULT 0.0,
                answer_completeness REAL DEFAULT 0.0,
                FOREIGN KEY (query_log_id) REFERENCES query_logs(id)
            )
        """)
        conn.commit()
        conn.close()

    def log_query(
        self,
        query: str,
        brand: str,
        model: str,
        response_time_ms: float,
        chunks_retrieved: int = 0,
        status: str = "success",
        sources_used: List[str] = None,
        answer_preview: str = "",
        error_message: str = "",
        evaluation: Dict[str, float] = None
    ) -> int:
        """
        Log a query and its response details.
        Returns the log entry ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        sources_json = json.dumps(sources_used or [])

        cursor.execute("""
            INSERT INTO query_logs 
            (timestamp, query, brand, model, response_time_ms, 
             chunks_retrieved, status, sources_used, answer_preview, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp, query, brand, model, response_time_ms,
            chunks_retrieved, status, sources_json,
            answer_preview[:500], error_message
        ))

        log_id = cursor.lastrowid

        # Log evaluation metrics if provided
        if evaluation:
            cursor.execute("""
                INSERT INTO evaluation_logs 
                (query_log_id, context_relevance, answer_groundedness, answer_completeness)
                VALUES (?, ?, ?, ?)
            """, (
                log_id,
                evaluation.get("context_relevance", 0.0),
                evaluation.get("answer_groundedness", 0.0),
                evaluation.get("answer_completeness", 0.0)
            ))

        conn.commit()
        conn.close()
        return log_id

    def get_logs(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Retrieve recent query logs."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM query_logs 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        """, (limit, offset))

        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs

    def get_stats(self) -> Dict:
        """Get aggregate statistics for monitoring."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Total queries
        cursor.execute("SELECT COUNT(*) as total FROM query_logs")
        total = cursor.fetchone()["total"]

        # Average response time
        cursor.execute("SELECT AVG(response_time_ms) as avg_time FROM query_logs")
        avg_time = cursor.fetchone()["avg_time"] or 0.0

        # Success rate
        cursor.execute(
            "SELECT COUNT(*) as success FROM query_logs WHERE status = 'success'"
        )
        success = cursor.fetchone()["success"]
        success_rate = (success / total * 100) if total > 0 else 100.0

        # Failed queries
        cursor.execute(
            "SELECT COUNT(*) as failed FROM query_logs WHERE status = 'error'"
        )
        failed = cursor.fetchone()["failed"]

        # Average evaluation scores
        cursor.execute("""
            SELECT 
                AVG(context_relevance) as avg_context,
                AVG(answer_groundedness) as avg_grounded,
                AVG(answer_completeness) as avg_complete
            FROM evaluation_logs
        """)
        eval_row = cursor.fetchone()

        conn.close()

        return {
            "total_queries": total,
            "avg_response_time_ms": round(avg_time, 2),
            "success_rate": round(success_rate, 2),
            "failed_queries": failed,
            "avg_context_relevance": round(eval_row["avg_context"] or 0.0, 3),
            "avg_answer_groundedness": round(eval_row["avg_grounded"] or 0.0, 3),
            "avg_answer_completeness": round(eval_row["avg_complete"] or 0.0, 3)
        }
