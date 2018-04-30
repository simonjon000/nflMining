import getTeams
import csv

weight_vector = [0, 0, 0, 0, 0, 0]
learning_rate = 0.5
team_dict = {}

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

def UpdateVector(winner_stats, loser_stats):
    global weight_vector
    print("Updating vectors")
    for x in range(0, 6):
        if winner_stats[x] > loser_stats[x]:
            weight_vector[x] += learning_rate
        elif winner_stats[x] < loser_stats[x]:
            weight_vector[x] -= learning_rate
    return

def GetValue(team_stats):
    global weight_vector
    value = 0
    for x in range(0, 6):
        value += team_stats[x] * weight_vector[x]
    return value


def Train():
    getTeams.TeamDict()
    MakeDict()
    training_error = 0
    training_set = 0
    # Need to get a complete set of the teams
    # All we need from the match is the elo for each team
    # Get the stats for that team for that year
    # Append those stats with the ELO score for the match
    # Calculate the value, compare, update if needed

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

        print(match[1] + " vs " + match[4] + " v1 %.2f " %v1 + " v2 %.2f"  %v2)
        print("Actual score: %d to %d" %(match[3], match[6]))

        # If the victor is team 2 but output was team 1, update weights
        if v1 >= v2 and match[3] < match[6]:
            UpdateVector(t2_stats, t1_stats)
            training_error += 1
        # If the victor is team 1 but output was team 2, update weights
        elif v1 <= v2 and match[3] > match[6]:
            UpdateVector(t1_stats, t2_stats)
            training_error += 1

    print("Training error: %.2f" %(training_error/training_set))


def main():
    Train()
    print(weight_vector)

main()