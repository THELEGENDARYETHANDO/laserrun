import random

num = random.randint(1, 50)

for i in range(5):
    guess = int(input("guess"))
    if guess == num:
        print("you won")
    else:
        print("you lose")