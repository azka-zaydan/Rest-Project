# This is for Problem-solving question number 2
def palindrome_checker(num):
    into_string = str(num)
    if into_string[::-1] == into_string:
        return True
    else:
        return False

print(palindrome_checker(10))