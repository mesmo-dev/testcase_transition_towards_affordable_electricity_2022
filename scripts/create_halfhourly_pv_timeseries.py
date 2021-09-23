import csv

pv_half = []
i = 0

with open('../pv_july2013.csv', newline='') as csvfile:
    r=csv.reader(csvfile)
    for row in r:
        if i % 30 == 0:
            irrad = float(row[3])

            if irrad < 0.0:
                irrad = 0.0

            pv_half.append(irrad/1000.0)

        i = i + 1

csvfile.close()

for i in range(0, len(pv_half)):
    print("%d,%f" % (i + 1, pv_half[i]))
