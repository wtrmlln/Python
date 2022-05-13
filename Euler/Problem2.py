a = 0
b = 1
temp_result = 0
result = 0

while result < 4000000:
    if temp_result == 0:
        a = b + b
        b = a + b
        temp_result = a + b
    else:
        temp_result = temp_result + b
        b = b + a
        a = temp_result - b
    
    if a % 2 == 0:
        result = result + a
print(result)