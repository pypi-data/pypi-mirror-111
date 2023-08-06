__version__ = '0.1.0'

def fizzbuzz(n):
  result = str(n)
  if (n == 0):
    pass
  if(n % 5 == 0 and n % 3 == 0):
    return "FizzBuzz"
  elif(n%5 == 0):
    return "Buzz"
  elif(n%3 == 0):
    return "Fizz"
  return result
  
def fizzbuzz_to(n):
  return list(map(fizzbuzz, range(n)))



