from Overall_Pipeline import run_pipeline
import psycopg2

class PostgresStorage:
    def __init__(self, host="localhost", database="your_db", user="your_user", password="your_password"):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        self._create_tables()  # create tables on init

    def _create_tables(self):
        """Creates tables if they don't exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50),
                role VARCHAR(20),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                description TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                project_id INT REFERENCES projects(id),
                labeller_id INT REFERENCES users(id),
                status VARCHAR(20),
                assigned_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self.conn.commit()

    def add_user(self, username: str, role: str):
        """Insert a new user"""
        self.cursor.execute(
            "INSERT INTO users (username, role) VALUES (%s, %s) RETURNING id",
            (username, role)
        )
        self.conn.commit()
        return self.cursor.fetchone()[0]  # returns new user's id

    def add_project(self, name: str, description: str):
        """Insert a new project"""
        self.cursor.execute(
            "INSERT INTO projects (name, description) VALUES (%s, %s) RETURNING id",
            (name, description)
        )
        self.conn.commit()
        return self.cursor.fetchone()[0]  # returns new project's id

    def add_task(self, project_id: int, labeller_id: int, status: str = "pending"):
        """Insert a new task"""
        self.cursor.execute(
            "INSERT INTO tasks (project_id, labeller_id, status) VALUES (%s, %s, %s) RETURNING id",
            (project_id, labeller_id, status)
        )
        self.conn.commit()
        return self.cursor.fetchone()[0]  # returns new task's id

    def close(self):
        """Close connection"""
        self.cursor.close()
        self.conn.close()


# Usage example
if __name__ == "__main__":
    db = PostgresStorage()

    user_id    = db.add_user("alice", "labeller")
    project_id = db.add_project("Sentiment Analysis", "Label tweets as positive/negative")
    task_id    = db.add_task(project_id, user_id, status="pending")

    print(f"Created user {user_id}, project {project_id}, task {task_id}")
    db.close()