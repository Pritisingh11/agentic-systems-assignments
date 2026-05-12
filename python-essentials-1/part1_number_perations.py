num1 = input()
num2 = input()

#Addition
print("Sum:", int(num1) + int(num2))

#Division with error handling
try: 
    result = int(num1) / int(num2)
    print("Division:", result) 
except ZeroDivisionError: 
    print("Cannot divide by zero")