import os.path
import logging
import csv
import datetime
from  email.utils import parsedate
from tempfile import mkstemp
from shutil import move, copymode
from os import remove


logger = logging.getLogger(__name__)

def add_to_database(uniqueId, status, cases, name="", parentId=None, url=None, downloadTime=None):
  if parentId == None:
    data_file = "data/"+uniqueId+".csv"
  else:
    data_dir = "data/"+parentId
    data_file = data_dir+"/"+uniqueId+".csv"
    os.makedirs(data_dir, exist_ok=True)

  try:
    downloadTimeStamp = datetime.datetime(*parsedate(downloadTime)[:6])
    downloadTimeStamp = downloadTimeStamp.replace(tzinfo=datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()
  except ValueError:
    downloadTimeStamp = downloadTime

  column_names = [ "Status","Cases","Source URL","Download timestamp" ]
  #Create temp file
  #new_file = tempfile.mkstemp()
  new_file = data_file + ".tmp"
  with open(new_file, "w",newline='\n') as csv_outfile:
    csvwriter = csv.DictWriter(csv_outfile, dialect='unix', fieldnames=column_names,lineterminator='\n')
    csvwriter.writeheader()

    with open(data_file, mode='r+',newline="") as csvfile:
      csvreader = csv.DictReader(csvfile, dialect='unix', fieldnames=column_names)
      line_count = 0
      status_is_in = False
      exact_duplicate = False
      existing_line = None
      duplicate_lines = []
      matching_lines = []
      for line in csvreader:
        line_count = line_count + 1
        #print(line)
        if (status == line['Status'] and (line['Source URL'] is None or line['Source URL'] == url)):
          status_is_in = True
          if(str(cases) == line['Cases']):
            # updating lines with missing URL (ugly -- inline update?)
            exact_duplicate = exact_duplicate or line['Source URL'] == url
            duplicate_lines.append(line)
          else:
            # If we import values from country, state, district and community level
            # keeping duplicates helps to identify reporting delays
            # keep date-matches for analysis of variance (TODO: add option to remove or combine date duplicates?)
            matching_lines.append(line)
            csvwriter.writerow(line)
        else:
          csvwriter.writerow(line)
    
      if status_is_in and exact_duplicate:
        if len(duplicate_lines) > 1:
          print("Replacing/found %s exact duplicates (date,url,cases): %r" % (len(duplicate_lines), duplicate_lines))
      else:
        # Always add one entry of the duplicates
        if parentId == None:
          print("NEU: {}({}) hat {} Fälle, Stand {}".format(name, uniqueId, cases, status))
        else:
          print("NEU: {}({} teil von {}) hat {} Fälle, Stand {}".format(name, uniqueId, parentId, cases, status))
      # Report if there are lines with the same status/date but different case number
      # verify/report value mismatch? (offer merge later, usually just overwrite with correct newer values?)
      for existing_line in matching_lines:
        print("status: {}, cases:{}".format(existing_line['Status'], existing_line['Cases'], existing_line['Source URL'], existing_line['Download timestamp']))
        #if int(existing_line['Cases']) != cases: #redundant check
        logger.error("{}:{}: Keeping existing colliding value {}={} ({}), but new value is {}={}".format(data_file, line_count, existing_line['Status'], existing_line['Cases'], status, cases))
      csvwriter.writerow({'Status': status, 'Cases': cases, 'Source URL': url, 'Download timestamp': downloadTimeStamp})
        #file.write(status+ ","+str(cases)+','+str(url)+','+str(downloadTimeStamp)+"\n")
      csvfile.close()
  #Replace existing file
  if os.replace is None:
    # Not atomic replace, but better than nothing in older python
    #Copy the file permissions from the old file to the new file
    shutil.copymode(data_file, new_file)
    #Remove original file
    os.remove(data_file)
    shutil.move(new_file, data_file)
  else:
    #Replace existing file (requires python 3.3)
    # TODO verify it keeps file-ownership and permissions
    os.replace(new_file, data_file)
