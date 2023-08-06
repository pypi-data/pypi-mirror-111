import math
import cmath
class X1X:
  """ The maths presented in this package was devised by Prof. Edson E. S. Sampaio from UFBa
in his spare time.I just implemented as a Python Library, as a means to help encrypt/decrypt files.
For (X^n) + (X^(-n)) = 'a', method 'eval' returns 'a'(n must be integer and >1).
Sidenote:all the solutions for the equation above are x=-0,5 +- i/2*Sqrt(3)

For (X^n) + (X^(-n)) = 'a' (n must be integer and >1), method 'eval_n_inverse'
returns a tuple with 4 lists inside as follows ('a1', 'a2', 'x01','x02'), being:
(x01)^n + (x01)^(-n) = a1 and (x02)^n + (x02)^(-n) = a2."""  
  def __init__(self,n):
    self.n = n
  def eval(self):
    if not isinstance(self.n, int) or(self.n == 0):
      raise ValueError(" n must be integer")
      return None
    if self.n%3 == 0:
      canlyniad = 2
    elif self.n%3== 1 or self.n%3==2:
      canlyniad = -1
    else:
      canlyniad = None
    return canlyniad
  def eval_n_inverse(self):
    if not isinstance(self.n, int) or(self.n == 0):  
      raise ValueError("n must be integer")
      return None
    y = int(1/(self.n))
    x01_complex = []
    x02_complex = []
    canyliad1 = []
    canyliad2 = []
    for l in range(self.n):

      x1 = cmath.exp(2j * math.pi *(l + 1/3)*y)
      x01_complex.append(x1)
      x2 = cmath.exp(2j * math.pi *(l + 2/3)*y)
      x02_complex.append(x2)    

      c1 = math.cos(self.n*2*math.pi*(l + 1/3))
      canyliad1.append(c1)
      c2 = math.cos(self.n*2*math.pi*(l + 2/3))
      canyliad2.append(c2)
    return (canyliad1,canyliad2,x01_complex,x02_complex)



if __name__ == "__main__":
  print("x^n + 1/x^n = 'result' of class X1X for x=-0,5 +- i/2*Sqrt(3)- by Edson E. S. Sampaio at Oct 16 2020")
  xix = X1X(n=3)
  result = xix.eval()
  print(result)
  xix = X1X(n=2)
  result = xix.eval_n_inverse()
  print(result)