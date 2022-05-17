# this is for Problem-Solving question number 1

def numAdder(list,target):
    for i in range(len(list)):
        if list[i]+list[i+1] == target:
            return [i,i+1]

print(numAdder(  [3, 2, 4],6))