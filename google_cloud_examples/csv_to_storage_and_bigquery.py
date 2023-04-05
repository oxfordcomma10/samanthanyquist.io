from google.cloud import bigquery
from google.cloud import storage
import csv_to_storage
import process_record
import argparse


schemas = [
    [
    bigquery.SchemaField("serial", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("sim_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("model", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("date", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("filename", "STRING", mode="NULLABLE"),
    ]
]

def main(kwargs):
    '''Takes directory of CSV/TXT files and inserts into Google Cloud Storage and BigQuery
    parameter: kwargs - dictonary of user inputed project id, bucket id, dataset id, and the directory location of the csv/txt files 
    return: None'''
    project = kwargs['project']
    bucket = kwargs['bucket']
    dataset = kwargs['dataset']
    
    #Takes CSV files and puts it into Google Cloud Storage
    csv_to_storage.main(kwargs)
    
    #Access Google Cloud Storage Client
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket) 
    
    Units = []
    
    for blob in blobs:
        #Normalize files to uniform structures
        blob_name = blob.name

        #Create Table
        bq_client = bigquery.Client(project = project)
        
        table_id = f"{project}.{dataset}.Units"
        table = bigquery.Table(table_id, schema=schemas[0])
        table = bq_client.create_table(table)
    
        #Query BigQuery to see if file has already been uploaded
        bq_client = bigquery.Client(project = project)
        query = f"SELECT count(*) AS amount FROM {project}.{dataset}.Units WHERE filename='{blob_name}'"
        query_job = bq_client.query(query)
        result = query_job.result()
        count = 0
        for row in result:
            if row.amount > 0:
                count = row.amount
        if count > 0:
            continue
        
        #Process lines from GCS to be places into BigQuery
        units = []
        if blob_name:
            units = process_record(blob)
        else:
            print("Unknown file", blob_name)
            continue
        Units += units
    
    #Access Google BigQuery 
    bq_client = bigquery.Client(project = project)
    storage_client = storage.Client(project = project)   

    #Insert Units rows into BigQuery using the schemas list
    table_id = f"{project}.{dataset}.Units"
    for i in range(Units):
        bq_client.insert_rows(table_id, Units[i], selected_fields = schemas[0])
        
    print(f"Inserted files into {project}.{dataset}.Units")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Consume Google Cloud Storage and write records to BigQuery")
    parser.add_argument('-p', '--project', required=True, help="Project Id")
    parser.add_argument('-b', '--bucket', required=True, help="Bucket Id")
    parser.add_argument('-d', '--dataset', required=True, help="Dataset Id")
    parser.add_argument('-r', '--directory', required=True, help="Directory with files")
    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    main(kwargs)

