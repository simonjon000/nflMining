import csv
match = []

def TeamDict():
    global match
    firstline = True
    with open('nfl_elo.csv', 'r') as nflstat:
        filereader = csv.reader(nflstat)
        for row in filereader:
            if firstline:
                    firstline = False
                    continue
            # match = [Year, T1 name, T1 elo, T1 score, T2 name, T2 elo, T2 score]
            match += [[int(row[1]), row[4].lower(), int(row[6][:4]), int(row[12]), row[5].lower(), int(row[7][:4]), int(row[13])]]
        nflstat.close()

def main():
    TeamDict()
    for v in match[0]:
        print(v)

main()