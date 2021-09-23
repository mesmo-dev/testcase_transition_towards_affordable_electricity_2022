import csv

pv_power = {}

with open('../Data_Geylang/electric_grid_ders.csv', newline='') as csvfile:
    r=csv.reader(csvfile)
    for row in r:
        der_name = row[1]
        node_name = row[4] 
        active_power_nom = row[9]

        if der_name.startswith("pv_"):
            node_nr = int(node_name.replace("secondary", ""))
            if node_nr not in pv_power:
                pv_power[node_nr] = float(active_power_nom)
            else:
                pv_power[node_nr] += float(active_power_nom)

pv_power = dict(sorted(pv_power.items()))
#print(pv_power)

for i in range(1, 392):
    if i in pv_power:
        print("%d,%f" % (i, pv_power[i]/1e6))
    else:
        print("%d,%f" % (i, 0))

csvfile.close()
