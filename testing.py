import training
import getTeams

def Test():
    test_error = 0
    test_set = 0

    # 1970 -> 2009 is for training. 2010 -> 2017 is for testing
    for match in getTeams.match[13873:]:
        test_set += 1

        # t_stats = [elo, age, games played, weight, height, years played in pro football]
        t1_stats = [match[2]] + training.team_dict[match[1]][match[0]]
        t2_stats = [match[5]] + training.team_dict[match[4]][match[0]]

        v1 = training.GetValue(t1_stats)
        v2 = training.GetValue(t2_stats)

        # If the victor is team 2 but output was team 1, update weights
        if (v1 >= v2 and match[3] < match[6]) or (v1 < v2 and match[3] > match[6]):
            test_error += 1

    print("Testing error: " + (test_error/test_set))