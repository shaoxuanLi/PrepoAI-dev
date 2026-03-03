from pymongo import MongoClient   # pip install pymongo
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Overall_Pipeline import run_pipeline

class MongoDBStorage:
    def __init__(self, host="localhost", port=27017, db_name="labelling_platform"):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def store_processed_data(self):
        """Run pipeline and store processed data as JSON documents"""
        collection = self.db["raw_data"]

        processed_data = run_pipeline()

        # if processed_data is a list, insert all at once
        if isinstance(processed_data, list):
            documents = [
                {
                    "content": item,
                    "status": "pending",        # waiting to be labelled
                    "created_at": datetime.now()
                }
                for item in processed_data
            ]
            result = collection.insert_many(documents)
            print(f"Inserted {len(result.inserted_ids)} documents into raw_data")
            return result.inserted_ids

        # if processed_data is a single dict
        elif isinstance(processed_data, dict):
            document = {
                "content": processed_data,
                "status": "pending",
                "created_at": datetime.now()
            }
            result = collection.insert_one(document)
            print(f"Inserted document with id: {result.inserted_id}")
            return result.inserted_id

    def store_label_result(self, task_id: int, labeller_id: int, labels: list):
        """Store complex JSON labelling results after labeller finishes"""
        collection = self.db["labelled_results"]

        document = {
            "task_id":     task_id,
            "labeller_id": labeller_id,
            "labels":      labels,      # complex JSON label structure
            "labelled_at": datetime.now()
        }
        # example of labels:
        # [
        #   {"text": "I love this", "label": "positive", "span": [0, 11]},
        #   {"text": "I hate this", "label": "negative", "span": [0, 11]}
        # ]

        result = collection.insert_one(document)
        print(f"Stored label result with id: {result.inserted_id}")
        return result.inserted_id

    def get_pending_data(self):
        """Fetch all raw data that has not been labelled yet"""
        collection = self.db["raw_data"]
        pending = list(collection.find({"status": "pending"}))
        print(f"Found {len(pending)} pending documents")
        return pending

    def update_status(self, document_id, status: str):
        """Update the status of a raw data document"""
        collection = self.db["raw_data"]
        collection.update_one(
            {"_id": document_id},
            {"$set": {"status": status}}   # "pending" → "in_progress" → "done"
        )
        print(f"Updated document {document_id} status to: {status}")

    def close(self):
        self.client.close()


# Usage example
if __name__ == "__main__":
    mongo = MongoDBStorage(
        host="localhost",
        port=27017,
        db_name="labelling_platform"
    )

    # 1. run pipeline and store processed data
    mongo.store_processed_data()

    # 2. fetch pending data for labellers
    pending = mongo.get_pending_data()

    # 3. simulate labeller labelling first document
    if pending:
        doc = pending[0]
        mongo.update_status(doc["_id"], "in_progress")

        # 4. store the label result
        mongo.store_label_result(
            task_id=1,
            labeller_id=1,
            labels=[
                {"text": "I love this", "label": "positive", "span": [0, 11]},
                {"text": "I hate this", "label": "negative", "span": [0, 11]}
            ]
        )

        mongo.update_status(doc["_id"], "done")

    mongo.close()