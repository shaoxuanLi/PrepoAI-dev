from Cloud_Data_Loader import S3Loader
from Local_Data_Loader import LocalFileLoader
from DB_Data_Loader import DBLoader

def getLoader(source_type, **kwargs):
    
    if source_type == "local":
        return LocalFileLoader(**kwargs)

    elif source_type == "s3":
        return S3Loader(**kwargs)

    elif source_type == "db":
        return DBLoader(**kwargs)
    
    else:
        raise ValueError("Unknown source type")