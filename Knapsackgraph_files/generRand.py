# import random

# shop = ["bananas","Rice","Glasses","Jackets","Boots","Hats","Gloves","Bracelets","Sashes","scarves","Socks","Bandana"]
# randlst = [x for x in range(len(shop))]
# for i in range(5):
#     sel = random.randint(0, len(randlst)-1)
#     item = shop[sel]
#     shop.remove(item)
#     randlst.pop()
#     x = random.uniform(0.1, 20)
#     y = random.randint(10, 1100)

#     print("{},{},{}".format(item,x,y))


import random
print("FIND X GAME. X is between 0 and 100. find x")
x, y = random.randint(0, 100), -1
for i in range(7):
    tryit = int(input("Enter a number: "))
    if tryit < x:
        print("too low")
    elif tryit > x:
        print("too high")
    else:
        print("Congratulations. You won the game by the ", i+1,"th trial.")
        y = i
        break

if y == -1:
    print("you failed. YOU ARE A FAILER.")