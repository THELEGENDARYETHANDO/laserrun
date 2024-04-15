num_1 = input("num 1")
num_2 = input("num 2")
num_3 = input("num 3")

arry = [int(num_1), int(num_2), int(num_3)]

highest_number = 0

for i in arry:
    if i >= highest_number:
        highest_number = i

print(highest_number)
