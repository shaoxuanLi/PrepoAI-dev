# loading from other databases
# can be able to process and load in all type of databases, including SQL, NoSQL, etc
from Base_model_Loader import BaseDataLoader
from sqlalchemy import create_engine, text

class DBLoader(BaseDataLoader):

    def __init__(self, db_url, query):
        self.engine = create_engine(db_url)
        self.query = query

    def load(self):
        with self.engine.connect() as conn:
            result = conn.execute(text(self.query))
            return [dict(row) for row in result]