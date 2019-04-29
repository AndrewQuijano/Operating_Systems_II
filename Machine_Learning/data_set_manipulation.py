import csv


# For kdd, we skip columns 10 - 22
# In our version, the label is in 0, so don't drop that!
def drop_columns(file, begin=0, end=9, begin_2=23, end_2=42):
    with open(file, "r") as source:
        rdr = csv.reader(source)
        with open("new_" + file, "w") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow(r[begin:end] + r[begin_2:end_2])


def split_csv(file, size=1000000):
    file_part = 1
    lines = []
    with open(file, 'r') as big_file:
        for line in big_file:
            if file_part % size == 0:
                with open(str(file_part) + "_" + str(file), 'w+') as chunk:
                    chunk.writelines(lines)
                lines = []
            else:
                lines.append(line)
            file_part += 1
            file_part = file_part % size


def merge_csv(file):
    file_part = 1
    for j in range(6):
        with open(file + "_" + file_part + ".csv", 'r') as chunk:
            with open(file + ".csv", 'a+') as big_file:
                for line in chunk:
                    big_file.write(line)
        file_part += 1


if __name__ == "__main__":
    # main()
    # kdd_prep()
    # drop_columns("kdd_prep.csv")
    split_csv("kdd_prep.csv")
