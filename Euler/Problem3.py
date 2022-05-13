number1 = 600851475143

i1 = 2
while i1 < number1:
	if number1 % i1 == 0:
		number1 = number1/i1
		i1 = 1
	i1 += 1
print(i1)
x = 0