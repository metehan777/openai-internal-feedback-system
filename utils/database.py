import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class Database:
    def __init__(self):
        try:
            print("Attempting database connection...")
            # Store connection params for reuse
            self.db_params = {
                'host': os.environ['PGHOST'],
                'database': os.environ['PGDATABASE'],
                'user': os.environ['PGUSER'],
                'password': os.environ['PGPASSWORD'],
                'port': os.environ['PGPORT']
            }
            # Test connection
            self._get_connection()
            print("Database connection successful")
            self._drop_tables()
            print("Tables dropped successfully")
            self._create_tables()
            print("Tables created successfully")
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            raise e

    def _get_connection(self):
        return psycopg2.connect(**self.db_params)

    def _drop_tables(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Drop existing sequence if exists
                cur.execute("DROP SEQUENCE IF EXISTS feedback_id_seq CASCADE")
                # Drop table if exists
                cur.execute("DROP TABLE IF EXISTS feedback CASCADE")
                conn.commit()

    def _create_tables(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Create feedback table with additional AI analysis columns
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        priority INTEGER NOT NULL,
                        ai_priority INTEGER,
                        safety_category TEXT,
                        reasoning TEXT,
                        key_concerns TEXT[],
                        tags TEXT[],
                        safety_flag BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        upvotes INTEGER DEFAULT 0
                    )
                """)
                conn.commit()

    def add_feedback(self, title, description, priority, tags, ai_analysis=None):
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                print(f"Adding feedback with title: {title}")
                if ai_analysis:
                    cur.execute(
                        """
                        INSERT INTO feedback (
                            title, description, priority, tags, ai_priority,
                            safety_category, reasoning, key_concerns, safety_flag
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            title, description, priority, tags,
                            ai_analysis.get('priority_score'),
                            ai_analysis.get('safety_category'),
                            ai_analysis.get('reasoning'),
                            ai_analysis.get('key_concerns', []),
                            ai_analysis.get('is_safety_concern', False)
                        )
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO feedback (title, description, priority, tags)
                        VALUES (%s, %s, %s, %s) RETURNING id
                        """,
                        (title, description, priority, tags)
                    )
                result = cur.fetchone()
                conn.commit()
                print("Feedback added successfully")
                return result[0] if result else None
        except Exception as e:
            print(f"Error adding feedback: {str(e)}")
            raise e
        finally:
            if conn:
                conn.close()

    def get_all_feedback(self):
        try:
            conn = self._get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM feedback ORDER BY created_at DESC")
                return cur.fetchall()
        finally:
            if conn:
                conn.close()

    def upvote_feedback(self, feedback_id):
        try:
            conn = self._get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE feedback SET upvotes = upvotes + 1 WHERE id = %s",
                    (feedback_id,)
                )
                conn.commit()
        finally:
            if conn:
                conn.close()
