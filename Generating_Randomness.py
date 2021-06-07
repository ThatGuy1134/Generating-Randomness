import random

def char_checker(string, test):
    if string == "enough" and test:
        return string
    for char in string:
        if char != '0' and char != '1':
            string = string.replace(char, "")
    return string


def analyzer(string, return_t):
    tuple_list = ["000", "001", "010", "011",
                  "100", "101", "110", "111"]
    values = []  # this is the tallies of 0s & 1s for each triad
    t = []  # this is a list of all the triads in the input
    zeros = 0
    ones = 0
    for num in range(0, len(string)):
        temp = string[num:num + 3:1]
        if len(temp) == 3:
            t.append(temp)
    t.pop()
    if return_t:
        return t

    follow_list = list(string[3::1])  # these are the numbers that follow the triads

    #print("\nt: {0}".format(t))
    #print("follow_list: {0}".format(follow_list))

    # this part looks for an instance of a triad in t, then counts the
    # corresponding following 0 or 1
    for tup in tuple_list:
        while t.count(tup) > 0:
            i = t.index(tup)
            if follow_list[i] == "0":
                zeros += 1
            else:
                ones += 1
            t.pop(i)
            follow_list.pop(i)

        values.append(str(zeros) + "," + str(ones))
        zeros, ones = 0, 0

    count_dict = dict(zip(tuple_list, values))
    return count_dict


def display_count(the_count):
    for key in the_count:
        print("{0}: {1}".format(key, the_count[key]))


def likely_to_follow(the_count):
    totals = [0, 0]  # this shows the total number of zeros, ones
    
    # this goes through the original dict, finds the number that
    # is most likely to follow a triad, and rewrites the dict with that
    for key in the_count:
        temp_stat = the_count[key].split(",")
        if int(temp_stat[0]) > int(temp_stat[1]):
            the_count[key] = 0
        elif int(temp_stat[0]) < int(temp_stat[1]):
            the_count[key] = 1
        else:
            the_count[key] = random.randint(0,1)

        totals[0] += int(temp_stat[0])
        totals[1] += int(temp_stat[1])

    #print("\nHere are the numbers that are most likely to follow each triad:")
    #for key in the_count:
    #    print("{0}: {1}".format(key, the_count[key]))

    #print("\nThe total number of following zeros was: {0}.".format(totals[0]))
    #print("The total number of following ones was: {0}.".format(totals[1]))

    return the_count, totals


def predicted_str(test_str, totals, the_count):
    # this gets the new test string, the total 0s & 1s, and the new count
    # that just has the most likely to follow
    length = len(test_str)
    num_list = []
    
    # this part constructs the first triad by starting with the most used
    # number, followed by two random numbers
    if totals[0] > totals[1]:
        num_list.append("0")
    elif totals[0] < totals[1]:
        num_list.append("0")
    else:
        num_list.append(str(random.randint(0,1)))

    num_list.append(str(random.randint(0,1)))
    num_list.append(str(random.randint(0,1)))

    # now we get all the triads from the test_str in order
    triads = analyzer(test_str, True)

    for tri in triads:
        num_list.append(str(the_count[tri]))

    #print("\n\nThis is the list: {0}".format(num_list))

    return "".join(num_list)


def how_correct(test_str, prediction, money):
    t_len = len(test_str)
    matches = 0

    for i in range(3, t_len):
        if test_str[i] == prediction[i]:
            matches += 1

    correct = (matches / (t_len - 3)) * 100

    money = money - matches
    money = money + ((t_len - 3) - matches)

    return matches, correct, money


#***** MAIN *****
string_len = 0
ran_string = ""

print("Please give AI some data to learn...")
print("The current data length is 0, 100 symbols left")

while string_len < 100:
    print("Print a random string containing 0 or 1:")
    temp_string = input()
    temp_string = char_checker(temp_string, False)
    ran_string = ran_string + temp_string
    string_len = len(ran_string)
    if string_len < 100:
        print("Current data length is {0}, {1} symbols left". 
              format(string_len, (100 - string_len)))

print("\nFinal data string:")
print(ran_string)

tuple_count = analyzer(ran_string, False)
#display_count(tuple_count)

follow_dict, total_list = likely_to_follow(tuple_count)

# starting the game
print("\nYou have $1000. Every time the system successfully predicts you next press, you lose $1.")
print('Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')

your_money = 1000
test_str = ""

while test_str != "enough":
    while len(test_str) < 3:
        print("\nPrint a random string containing 0 or 1:")
        test_str = input()
        test_str = char_checker(test_str, True)

    if test_str != "enough":
        prediction = predicted_str(test_str, total_list, follow_dict)
        print("prediction:")
        print(prediction)
        correct, percent, your_money = how_correct(test_str, prediction, your_money)
        print("\nComputer guessed right {0}, out of {1} symbols ({2:5.2f}) %"
              .format(correct, (len(test_str) - 3), percent))
        print("Your capital is now ${0:4.0f}".format(your_money))
        test_str = ""

# ending the game
print("Game over!")
