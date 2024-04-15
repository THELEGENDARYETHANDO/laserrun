import os

print("Rules: type rock, paper or scissors (NO CAPTIAL LETTERS)")



player_1 = input("P1 choice")


os.system('cls')

print("Rules: type rock, paper or scissors (NO CAPTIAL LETTERS)")

print("WE LIVE WE LOVE WE LIE DOOO DOO DO DOO DOO DOO DOO")
player_2 = input("P2 choice")

if player_1 == "rock" and player_2 == "scissors":
    print("player 1 wins")
elif player_1 == "rock" and player_2 == "paper":
    print("player 2 wins")
elif player_1 == "paper" and player_2 == "scissors":
    print("player 2 wins")
elif player_1 == "paper" and player_2 == "rock":
    print("player 1 wins")
elif player_1 == "scissors" and player_2 == "paper":
    print("player 1 wins")
elif player_1 == "scissors" and player_2 == "rock":
    print("player 2 wins")
else:
    print("tie bozo")