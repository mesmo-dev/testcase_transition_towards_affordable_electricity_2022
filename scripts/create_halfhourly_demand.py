import csv

demand_half = []
i = 0
last_demand = -1

with open('../hourly_demand_sg_2020.csv', newline='') as csvfile:
    r=csv.reader(csvfile)
    for row in r:
        if last_demand >= 0:
            demand_half.append((last_demand + float(row[0]))/2)

        last_demand = float(row[0])
        demand_half.append(last_demand)

csvfile.close()

for i in range(0, len(demand_half)):
    print("%d,%f" % (i + 1, demand_half[i]))
