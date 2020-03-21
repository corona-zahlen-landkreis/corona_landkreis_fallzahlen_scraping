import os.path


def add_to_database(landkreis, status, cases):
#  print("{} hat {} Fälle, Stand {}".format(landkreis, cases, status))
  data_file = "data/"+landkreis+".csv"

  if not os.path.isfile(data_file):
    f = open(data_file, "w")
    f.write("Status,Cases\n")
    f.close()

  with open(data_file, "r+") as file:
    for line in file:
      if status in line:
        break
    else:
      print("NEU: {} hat {} Fälle, Stand {}".format(landkreis, cases, status))
      file.write(status+ ","+str(cases)+"\n")
