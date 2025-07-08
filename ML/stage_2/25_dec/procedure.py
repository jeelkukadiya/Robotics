Total_Silo=5

def take_input():
    for i in range(Total_Silo):
        x = list(map(str, input(f"Enter balls in Silo {i+1} : ").split(',')))
        final_list.append(x)
    return final_list


state = [["","",""],["","","O"],["","","X"],["","O","O"],["","X","O"],["","O","X"],["","X","X"],["O","O","O"],["X","O","O"],["O","X","O"],["X","X","O"],["O","O","X"],["X","O","X"],["O","X","X"],["X","X","X"]]


final_list=[]
verify_list=[]
index_list=[]
next_state=[]

"""
# taking various silo state as input
for i in range(Total_Silo):
    x = list(map(str, input(f"Enter balls in Silo {i+1} : ").split(',')))
    final_list.append(x)
"""

final_list = take_input()

print(f"Ball Arrangement in Silo : ", final_list)

# verifying wheather all the input given are possible or not
j=0
for i in range(Total_Silo):
    for sublist in state:
        if sublist == final_list[i]:
            verify_list.append(sublist)
            j=j+1
            # Generating the index_list
            index=state.index(sublist)
            index_list.append(index)
print("All valid State of input are : ",verify_list)

if j==Total_Silo:
    print("All Input State of Silo are valid")     
else:
    print("There is an invalid State in input")

# Generating cal_list for Calculation purpose
cal_list=list(map(lambda x: x + 1, index_list))

print(cal_list)

# Taking input from user to generate next state of the silos
ball=input("Enter the type of ball you want to insert : ")
Silo_number=int(input("Enter the silo number in which you want to enter the ball :  "))

# Generating the next stage index number of Silo
number=cal_list[Silo_number-1]
if 8<=number<=15:
    print("The silo is already full")
elif number>=15 or number<=0:
    print("An error occured")
elif ball=='x' or ball=='X':
    number=((2*number)+1)
else:
    number=2*number
cal_list[Silo_number-1]=number
index_list=list(map(lambda y: y - 1, cal_list))      

for i in range(Total_Silo):
    next_state.append(state[index_list[i]])

print("Next state is : ", next_state)