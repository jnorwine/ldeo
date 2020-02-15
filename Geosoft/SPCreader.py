import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os
from tqdm import tqdm

### CONFIG ################################################################

input = "G:\\jnorwine\\polygrid1\\spc"
output = "G:\\jnorwine\\polygrid1\\spc\\processed\\"

###########################################################################

def spc_to_csv(input, output):

    openfile = open(input, "r")
    linelist = openfile.readlines()
    openfile.close()

    average = re.search(r"Ln\(E\) \=.+(\d+\.\d+)e\+(\d*)", linelist[2])
    columns = re.findall(r"\s+(\S+)", linelist[4])

    data = linelist[7:]
    for i in range(len(data)):
        data[i] = data[i].split()

    df = pd.DataFrame(data)
    df.columns = columns

    save_path = os.path.join(output, "csv\\")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    name = re.search(r"\\([^\\]+)\.SPC", input).group(1) + ".csv"
    save_path = os.path.join(save_path, name)

    df.to_csv(save_path, index=False)



#file_list = next(os.walk(input))[2]
new_input = input
file_list = next(os.walk(new_input))[2]

for i in range(len(file_list)):
    file_list[i] = os.path.join(input, file_list[i])

for path in tqdm(file_list, ascii=True):
    spc_to_csv(path, output)
