import csv
yteam = {}
team = []
with open('nfl_elo.csv', 'r') as nflstat:
    filereader = csv.reader(nflstat)
    s=""
    t=1
    for row in filereader:
        if t==1:
            t=0
            continue
        if s != row[1]:
            yteam[s] = set(team)
            s=row[1]
            tempteam = []
            #print(yteam)
        team.append(row[4].lower())
        team.append(row[5].lower())
for key in yteam:
    print(">"+key+"<")
