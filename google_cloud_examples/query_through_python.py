from google.cloud import bigquery
import argparse

def main(kwargs):
    '''Performs a query
    parameter: kwargs - dictionary containing query statement to be used
    return: None'''
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        kwargs['query'])
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    print(rows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Perform query on BigQuery")
    parser.add_argument('-q', '--query', required=True, help="Full query statement")
    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    main(kwargs)