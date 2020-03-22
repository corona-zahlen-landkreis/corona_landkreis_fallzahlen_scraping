import os
import re
from tqdm import tqdm

for name in tqdm(os.listdir('./')):
    if re.match(r"get-.*\.py", name) is None or os.path.isdir('./' + name):
        continue
    os.system("python3 " + name)
