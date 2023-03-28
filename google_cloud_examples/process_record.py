
def process_record(fname, bucket):
    '''Processes Records 
    parameters: fname - filename to reference in Google Cloud Storage
                bucket - client bucket to access files in Google Cloud Storage
    return: List of tuples'''
    blob = bucket.get_blob(fname)
    downloaded_blob = blob.download_as_string()
    lines = downloaded_blob.splitlines()
    Date = fname[fname.find("date") + len("date") + 1:][:8]
    date = Date[:4] + "-" + Date[4:6] + "-" + Date[6:] + " 00:00:00"
    units = []
    for line in lines:
        line = line.decode("utf-8")
        line = line.split(',')
        tupled = tuple(line)
        if len(tupled) == 3:
            serial,sim_id,model = tupled
            units.append(serial, sim_id, model, date, fname)
        else:
            print(f"Incorrect number of cells in line in {fname}")
    return units
