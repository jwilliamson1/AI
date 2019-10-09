def cube(x):
  return x * x * x

def fact(n):
 if n < 1:
   raise Exception("Input must be positive: " + str(n))
 if n == 1:
  return 1
 else:
  return n * fact(n - 1)

print(cube(3))

print(fact(3))