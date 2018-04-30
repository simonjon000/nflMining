import getTeams
import csv

# [elo, age, games played, weight, height, years played in pro football]
weight_vector = [0, 0, 0, 0, 0, 0]
learning_rate = 1
team_dict = {}
max = [0, 0, 0, 0, 0, 0]
min = [100000, 100000, 100000, 10000, 100000, 100000]

# Goal here is to use the weight vector to get a value for the inputs
# Get two values and the one with the higher value is the winner
# If incorrect winner is chosen, then we want to find the difference between the two sets of inputs
# The actual winner's inputs which are greater than the loser's inputs should increase the corresponding weight
# The inputs which are lower should decrease the corresponding weights

def MakeDict():
    with open('avg.csv', 'r') as f:
        filereader = csv.reader(f)
        for row in filereader:
            # team_dict[name] = [{year: [age, games played, weight, height, years played in pro football]}]
            # team_dict[name][year] = [age, games played, weight, height, years played in pro football]
            inches = (int(row[5][0]) * 12) + float(row[5][2:])
            if row[1] not in team_dict:
                team_dict[row[1]] = {int(row[0]): [float(row[2]), float(row[3]), float(row[4]), inches, float(row[6])]}
            else:
                team_dict[row[1]][int(row[0])] = [float(row[2]), float(row[3]), float(row[4]), inches, float(row[6])]
    return

def UpdateVector(winner_stats, loser_stats):
    # Normalizing data
    w = [(winner_stats[0] - 1200)/550, (winner_stats[1] - 24.6)/3, (winner_stats[2])/16,
         (winner_stats[3] - 236.2)/12.3, (winner_stats[4] - 72.9)/1.6, (winner_stats[5]) - 2/3]
    l = [(loser_stats[0] - 1200)/550, (loser_stats[1] - 24.6)/3, (loser_stats[2])/16,
         (loser_stats[3] - 236.2)/12.3, (loser_stats[4] - 72.9)/1.6, (loser_stats[5]) - 2/3]

    for x in range(0, 6):
        stat = w[x] - l[x]
        weight_vector[x] += stat * learning_rate
    return

def GetValue(team_stats):
    value = 0
    for x in range(0, 6):
        value += team_stats[x] * weight_vector[x]
    return value


def Train():
    global learning_rate
    getTeams.TeamDict()
    MakeDict()
    training_error = 0
    training_set = 0

    # match = [Year, T1 name, T1 elo, T1 score, T2 name, T2 elo, T2 score]
    # 1970 -> 2009 is for training. 2010 -> 2017 is for testing
    #for match in getTeams.match[4551:13873]:
    for match in getTeams.match[15475:]:
        training_set += 1
        # t_stats = [elo, age, games played, weight, height, years played in pro football]
        t1_stats = [match[2]] + team_dict[match[1]][match[0]]
        t2_stats = [match[5]] + team_dict[match[4]][match[0]]

        v1 = GetValue(t1_stats)
        v2 = GetValue(t2_stats)

        # print(match[1] + " vs " + match[4] + " v1 %.2f " %v1 + " v2 %.2f"  %v2)
        # print("Actual score: %d to %d" %(match[3], match[6]))

        # If the victor is team 2 but output was team 1, update weights
        if v1 >= v2 and match[3] < match[6]:
            UpdateVector(t2_stats, t1_stats)
            training_error += 1
        # If the victor is team 1 but output was team 2, update weights
        elif v1 <= v2 and match[3] > match[6]:
            UpdateVector(t1_stats, t2_stats)
            training_error += 1

    #print("Max: ", max)
    #print("Min: ", min)
    print("Training error: %.2f" %(training_error/training_set))
    print("Final weight vector: [%.2f, %.2f, %.2f, %.2f, %.2f, %.2f]" %(weight_vector[0], weight_vector[1],
                                                                        weight_vector[2], weight_vector[3],
                                                                        weight_vector[4], weight_vector[5]))
    return

Train()