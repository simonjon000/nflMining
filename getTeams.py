import csv

yteam = {}
match = []
with open('nfl_elo.csv', 'r') as nflstat:
    filereader = csv.reader(nflstat)
    s = ""
    for row in filereader:
        # if s != row[1]:
        #    yteam[s] = set(team)
        #    s=row[1]
        #    print(yteam)

        # Year, T1 name, T1 elo, T1 score, T2 name, T2 elo, T2 score
        match.append((row[1], row[4].lower(), row[6][:6], row[12], row[5].lower(), row[7][:6], row[13]))

for key in match:
    print("Year:" + key[0] + ", T1:" + key[1], key[2], key[3] + ", T2:" + key[4], key[5], key[6])
