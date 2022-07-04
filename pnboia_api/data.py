import pandas as pd

from google.cloud import storage
from datamodelapi.params import *
from datamodelapi.bd import *

# iGIJHmD89mJ7xk6G

def get_data_from_gcp(filename, start_date, end_date, nrows=10000, optimize=False, **kwargs):
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_FOLDER}/{filename}"
    print(path)
    df = pd.read_csv(path, nrows=nrows)
    return df[(df['date'] > start_date) & (df['date'] < end_date)]

def get_data_from_raw(filename, start_date='2000-01-01', end_date='2030-01-01', nrows=1000000000, optimize=False, **kwargs):
    """method to get the training data (or a portion of it) from google cloud bucket"""

    path = f"{LOCAL_PATH[0:-5]}{filename}.csv"

    df = pd.read_csv(path, nrows=nrows)
    df = df[['id', 'title', 'publication', 'author', 'date', 'year',
       'month', 'content']]

    return df[(df['date'] > start_date) & (df['date'] < end_date)]


# gcloud run deploy apipython \
# --image=gcr.io/le-wagon-data-582/apipython \
# --set-env-vars=GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
# --set-cloudsql-instances=le-wagon-data-582:us-central1:datamodel \
# --platform=managed \
# --region=us-central1 \
# --project=le-wagon-data-582
