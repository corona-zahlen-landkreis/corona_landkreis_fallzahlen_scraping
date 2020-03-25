import os.path
import logging
import csv
import datetime
from  email.utils import parsedate

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
  if not os.path.isfile(data_file):
    with open(data_file, "w",newline='\n') as csvfile:
      csvwriter = csv.DictWriter(csvfile, dialect='unix', fieldnames=column_names,lineterminator='\n')
      csvwriter.writeheader()
      csvfile.close()

  with open(data_file, mode='r+',newline="") as csvfile:
    csvreader = csv.DictReader(csvfile, dialect='unix', fieldnames=column_names)
    line_count = 0
    status_is_in = False
    cases_is_in = False
    existing_line = None
    for line in csvreader:
      line_count = line_count + 1
      #print(line)
      if(status == line['Status']):
        status_is_in = True
        if(str(cases) == line['Cases']):
          # updating lines with missing URL (ugly -- inline update?)
          cases_is_in = line['Source URL'] is not None
          existing_line = line
        elif existing_line is None:
          # we just want the first collision?
          existing_line = line
    
    if status_is_in:
      #logger.debug("nothing new")
      
      if not cases_is_in:
        # there is already a line with the same status
        # verify/report value mismatch? (offer merge later, usually just overwrite with correct newer values?)
        print("status: {}, cases:{}".format(existing_line['Status'], existing_line['Cases'], existing_line['Source URL'], existing_line['Download timestamp']))
        if int(existing_line['Cases']) != cases:
            logger.error("{}:{}: Collision with existing value {}={}, but new value is {}={}".format(data_file, line_count, existing_line['Status'], existing_line['Cases'], status, cases))
            
        if parentId == None:
          print("NEU: {}({}) hat {} Fälle, Stand {}".format(name, uniqueId, cases, status))
        else:
          print("NEU: {}({} teil von {}) hat {} Fälle, Stand {}".format(name, uniqueId, parentId, cases, status))
        csvwriter = csv.DictWriter(csvfile, dialect='unix', fieldnames=column_names,lineterminator='\n')
        csvwriter.writerow({'Status': status, 'Cases': cases, 'Source URL': url, 'Download timestamp': downloadTimeStamp})
        #file.write(status+ ","+str(cases)+','+str(url)+','+str(downloadTimeStamp)+"\n")
    else:
      if parentId == None:
        print("NEU: {}({}) hat {} Fälle, Stand {}".format(name, uniqueId, cases, status))
      else:
        print("NEU: {}({} teil von {}) hat {} Fälle, Stand {}".format(name, uniqueId, parentId, cases, status))
      #TODO URL escape , in url and downloadTime
      csvwriter = csv.DictWriter(csvfile, dialect='unix', fieldnames=column_names,lineterminator='\n')
      csvwriter.writerow({'Status': status, 'Cases': cases, 'Source URL': url, 'Download timestamp': downloadTimeStamp})
      #file.write(status+ ","+str(cases)+','+str(url)+','+str(downloadTimeStamp)+"\n")
