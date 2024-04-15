score = int(input("What score did you get"))

if score >= 101:
    print ("that input was invalid")
elif score >= 85:
    print("Congrats, you got an A")
elif score >= 70:
    print("Congrats, you got a B")
elif score >= 50:
    print ("Well done, you got a C")
elif score >= 25:
    print ("damn bro, you got a D")
elif score >= 0:
    print ("bruh, you got an F")
else:
    print ("that input was invalid")