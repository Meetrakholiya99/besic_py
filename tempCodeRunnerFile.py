# Program to find the HCF of two numbers (TCS)

a = int(input("Enter first number: "))  # Fixed incorrect input handling
b = int(input("Enter second number: "))

smaller = min(a, b)  # Find the smaller number

for i in range(smaller, 0, -1):  # Iterate from smaller to 1
    if a % i == 0 and b % i == 0:
        hcf = i  # Assign correct HCF value
        break  # Exit loop once HCF is found

print(f"The HCF of {a} and {b} is {hcf}")  # Print result
