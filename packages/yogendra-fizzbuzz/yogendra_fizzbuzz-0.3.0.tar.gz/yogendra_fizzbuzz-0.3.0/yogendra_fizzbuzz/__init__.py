__version__ = '0.3.0'

def fizzbuzz(n):
  result = str(n)
  if (n == 0):
    pass
  elif(n % 5 == 0 and n % 3 == 0):
    result = "FizzBuzz"
  elif(n%5 == 0):
    result = "Buzz"
  elif(n%3 == 0):
    result = "Fizz"
  return result
  
def fizzbuzz_to(n):
  return list(map(fizzbuzz, range(1,n+1)))



