# Loader file, First including the ability of importing text files
    # including csv, json, word, .. text documents
# Can then be extended to include image and sound processing capabilities.

from Base_model_Loader import BaseDataLoader
import json, csv
from pathlib import Path

class LocalFileLoader(BaseDataLoader):

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        ext = Path(self.filepath).suffix.lower()
        if ext == '.json':
            with open(self.filepath, 'r') as f:
                return json.load(f)
        if ext == '.csv':
            with open(self.filepath, 'r') as f:
                reader = csv.DictReader(f)  
                return list(reader)   
        if ext == ".txt":
            with open(self.filepath, 'r') as f:
                return f.read()

        raise ValueError(f"Unsupported file type: {ext}")
