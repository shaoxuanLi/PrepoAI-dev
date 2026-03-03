# obtain the raw data, pass it to the Overall_interface.py, and preprocess it through preprocess_pipeline.py
# then in this file 

from Loaders.Overall_Interface import getLoader
from Preprocess.preprocess_pipeline import PreprocessPipeline


def getSource(): # this is the interface to how you want to process the data
    #through frontend user type in
    source = "local" #example
    return source

def getKwargs(): # this is the interface for the keys/urls needed in order to access the data
    #through frontend user type in
    kwargs = {"file_path": "path/to/local/file.txt"} #example
    return kwargs


def run_pipeline():
    source = getSource()
    kwargs = getKwargs()

    loader = getLoader(source, **kwargs)
    raw_data = loader.load()

    preprocessor = PreprocessPipeline()
    processed_data = preprocessor.process(raw_data)
    
    return processed_data 
