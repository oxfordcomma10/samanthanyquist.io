
# Google Cloud Examples

## Summary

The Google Cloud Examples project demonstrates a program that takes `.csv` or `.txt` files, standarizes the contents in these files, uploads the content to Google Cloud Storage (GCS) and Google BigQuery (BQ), and then allows one to SQL query the BigQuery database, all in Python.  

### Further Information

What is [Google Cloud Storage](https://cloud.google.com/storage)?  
What is [Google BigQuery](https://cloud.google.com/bigquery)?

---

## How to Set Up the Program

### Requirements

The program is best used with a Linux operating system and is written in Python 3.  

#### Packages

    google-api-core==2.0.0
    google-auth==2.0.1
    google-cloud-bigquery==2.24.1
    google-cloud-core==2.0.0
    google-cloud-storage==1.42.0
    pycparser==2.20
    pyparsing==2.4.7

#### Google Cloud Platform Access

Must have an active GCS [bucket](https://cloud.google.com/storage/docs/creating-buckets) and BQ [project](https://cloud.google.com/bigquery/docs/resource-hierarchy) and dataset with proper IAM credentials.  

---

## Uploading Files to Google Cloud Storage

To simply upload files from a local directory to GCS, use `csv_to_storage.py`. The program will walk through each file in the directory and check if it is a `.csv` or `.txt` file and if it has already been uploaded to the GCS bucket. If it has not been uploaded and is either a `.csv` or `.txt` file, then the program will upload the file to the GCS bucket.

To run the program on a Linux command line with output:  

    $ python3 csv_to_storage.py -b [bucket ID] -r [directory]
    Completed uploading files to Google Cloud Storage

---

## Uploading Files to Google BigQuery and Google Cloud Storage

To upload files from a local directory to GCS and BQ, use `csv_to_storage_and_bigquery.py`. The program uses `csv_to_storage.py` to upload the local `.csv` and `.txt` files to a GCS bucket, for more specfic information go to [Uploading Files to Google Cloud Storage](#uploading-files-to-google-cloud-storage). To omit this feature go to [Only Upload to BigQuery](#only-upload-to-bigquery). The other part of the program is uploading the contents of the files to a specified BQ project and dataset. First, a new table called `[project ID].[dataset ID].Units` is created in the project and dataset within BQ. The table schemas are  

    bigquery.SchemaField("serial", "STRING", mode="NULLABLE")
    bigquery.SchemaField("sim_id", "STRING", mode="NULLABLE")
    bigquery.SchemaField("model", "STRING", mode="NULLABLE")
    bigquery.SchemaField("date", "TIMESTAMP", mode="NULLABLE")
    bigquery.SchemaField("filename", "STRING", mode="NULLABLE")

meaning that the newly created table will look similar to

| serial | sim_id | model | date | filename |
| ------ | ------ | ----- | ---- | -------- |

once the `[project ID].[dataset ID].Units` table is created.  

If a table does not need to be created, follow [Uploading to a BigQuery Table That Already Exists](#uploading-to-a-bigquery-table-that-already-exists).  

After table creation, the program pulls all files from the GCS bucket and queries each filename with the BQ table to check if the rows of the file already exist in the table. This is to prevent multiple entries of the same information. If the rows already exist then the next file is checked without adding more into the BQ `[project ID].[dataset ID].Units` table.  

The new rows are then sent through `process_records.py` to normalize the rows to align with the BQ table schemas by adding the date of the file information and the filename. From there the normalized rows are inserted into the `[project ID].[dataset ID].Units` table.

To run the program on a Linux command line with output:

    $ python3 csv_to_storage_and_bigquery.py -p [project ID] -b [bucket ID] -d [dataset ID] -r [directory]
    Completed uploading files to Google Cloud Storage
    Inserted files into [project ID].[dataset ID].Units
 

### Example Input and Output of Uploading Files to Google BigQuery and Google Cloud Storage

From `example_input20230403.csv`

| serial | sim_id | model |
| ----- | ----- | ----- |
| 1234567 | 3001234567 | 300 |
| 1234568 | 3001234568 | 300 |
| 8765432 | 4008765432 | 400 |

BQ `[project ID].[dataset ID].Units` table  

| serial | sim_id | model | date | filename |
| ----- | ----- | ----- | ----- | ----- |
| 1234567 | 3001234567 | 300 | 2023-04-03 | /data/example_input20230403.csv |
| 1234568 | 3001234568 | 300 | 2023-04-03 | /data/example_input20230403.csv |
| 8765432 | 4008765432 | 400 | 2023-04-03 | /data/example_input20230403.csv |

---

## Query BigQuery Table

The script `query_through_python.py` queries through a given BQ table. BQ uses SQL to query through tables.

To run the program on Linux:

    $ python3 query_through_python.py -q "[Full query statement]"

Once the program has finished running the system will print the result of the query.

### Example Query

Using the example `[project ID].[dataset ID].Units` table from [Upload to Google Bigquery Example](#example-input-and-output-of-uploading-files-to-google-bigquery-and-google-cloud-storage)

Command line and result:

    $ python3 query_through_python.py -q "SELECT count(*) FROM [project ID].[dataset ID].Units WHERE model='300'"
    2

---

## Additonal Information and Tips

### Only Upload to BigQuery

The script `csv_to_storage_and_bigquery.py` includes a line to upload a local directory's contents to a specified GCS bucket. To only use the current files in the GCS bucket and upload to the BQ table, remove the following lines:

    csv_to_storage.main(kwargs)

and  

    parser.add_argument('-r', '--directory', required=True, help="Directory with files")

It is recommended that these lines be commented out rather than removed in case there is a future use for the GCS upload feature.

    # csv_to_storage.main(kwargs)

and  

    # parser.add_argument('-r', '--directory', required=True, help="Directory with files")

To run the program on a Linux command line with the output:

    $ python3 csv_to_storage_and_bigquery.py -p [project ID] -b [bucket ID] -d [dataset ID]
    Inserted files into [project ID].[dataset ID].Units

### Uploading to a BigQuery Table That Already Exists

The script `csv_to_storage_and_bigquery.py` includes lines to create a table called *Units* in the specified project and dataset database. If the table already exists and only new content needs to be added, remove the following lines:

    table_id = f"{project}.{dataset}.Units"
    table = bigquery.Table(table_id, schema=schemas[0])
    table = bq_client.create_table(table)

It is recommended that these lines be commented in case there is a future use for the table creation.

    # table_id = f"{project}.{dataset}.Units"
    # table = bigquery.Table(table_id, schema=schemas[0])
    # table = bq_client.create_table(table)

---

## Version

1