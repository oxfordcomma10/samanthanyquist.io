from google.cloud import storage
import argparse
import os

def main(kwargs):
    '''Goes through user inputed directory (and its subdirectories) and uploads to Google Cloud Storage 
    parameter: kwargs - dictonary of bucket id and directory path that contains the files to go into Google Cloud Storage
    return: None'''
    bucket = kwargs['bucket']
    dir = kwargs['directory']
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if (filename.endswith(".csv")) or (filename.endswith(".txt")):
                full_filename = os.path.join(root,filename)
                blob = bucket.blob(full_filename)
                if not blob.exists():
                    blob.upload_from_filename(full_filename)
    print("Completed uploading files to Google Cloud Storage")
                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Put files into Google Cloud Storage")
    parser.add_argument('-b', '--bucket', required=True, help="Bucket Id")
    parser.add_argument('-r', '--directory', required=True, help="Directory with files")
    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    main(kwargs)