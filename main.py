import datetime

try:
    char_list = eval(open("charlist", "r").read())
except FileNotFoundError:
    char_list = []
    name = 0
    i = 0
    print("(input -1 if you dont have an nth character)")
    while name != "-1":
        name = input(f"Please input character number {i}'s name: ")
        char_list.append(name)
        i += 1

    open("charlist", "w").write(str(char_list))

while True:
    date = datetime.date.today()
    char = input("Please input character resampled on: ")

    if char.isdigit():
        if 0 <= int(char) <= 10:
            char_file = open(char_list[int(char) - 1], "a")
        else:
            continue
    else:
        if char in char_list:
            char_file = open(char, "a")
        else:
            continue

    if input("Did you sample a skill (y/n)? ") == "y":
        print("(T1 W = Oak logs), (T2 B = Butterfly)")
        mat = input("Please input the material tier followed by type: ").split()
        amount = input("Please input amount sampled: ")

        char_file.write(f"[{date.day + date.month * 30 + date.year * 365}, 'Resource',  ({mat[0]}, {mat[-1]}), {amount}]")

    elif input("Did you sample a mob drop (y/n)? ") == "y":
        print("(W1 1 = Spore Caps), (W3 4 = Ram Wool)")
        mat = input("Please input the world number followed by tier: ").split()
        amount = input("Please input amount sampled: ")

        char_file.write(
            f"[{date.day + date.month * 30 + date.year * 365}, 'Resource',  ({mat[0]}, {mat[-1]}), {amount}]")

    char_file.write("\n")
    char_file.close()
