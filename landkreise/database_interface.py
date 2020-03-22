import os.path


def add_to_database(uniqueId, status, cases, name="", parentId=None):
  if parentId == None:
    data_file = "data/"+uniqueId+".csv"
  else:
    data_dir = "data/"+parentId
    data_file = data_dir+"/"+uniqueId+".csv"
    os.makedirs(data_dir, exist_ok=True)

  if not os.path.isfile(data_file):
    f = open(data_file, "w")
    f.write("Status,Cases\n")
    f.close()

  with open(data_file, "r+") as file:
    line_count = 0
    for line in file:
      line_count = line_count + 1
      if status in line:
        # verify/report value mismatch? (offer merge later, usually just overwrite with correct newer values?)
        [line_status, line_cases] = line.split(",")
        if int(line_cases) != cases:
            print("ERROR in {}:{}: Collision with existing value {}={}, but new value is {}={}".format(data_file, line_count, line_status, line_cases, status, cases))
        else:
            # Value matches existing entry
            break
      else:
        if parentId == None:
          print("NEU: {}({}) hat {} Fälle, Stand {}".format(name, uniqueId, cases, status))
        else:
          print("NEU: {}({} teil von {}) hat {} Fälle, Stand {}".format(name, uniqueId, parentId, cases, status))
        file.write(status+ ","+str(cases)+"\n")
