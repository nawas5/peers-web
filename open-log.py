import csv
import pandas as pd

filename = "data/peers.log"
filename_csv = "data/peers-log.csv"

with open(filename_csv, 'w', encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(["time","name","x","y","z"])
    with open(filename, 'r') as file:
        for line in file:
            if line.find("CLE: TAG") > 0:
                a = line.split()
                # проверка на корректность точек
                if a[4] == "1":
                    time = a[0]
                    name = a[3]
                    x = float(a[5])
                    y = float(a[6])
                    z = float(a[7])
                    file_writer.writerow([str(time), str(name), str(x), str(y), str(z)])


df = pd.read_csv(filename_csv, error_bad_lines=False)
df["number"] = 0
mname = df["name"].unique()
for i in range(len(df)):
    for j in range(len(mname)):
        if df["name"][i] == mname[j]:
            df["number"][i] = j+1

df.to_csv("data/log.csv")