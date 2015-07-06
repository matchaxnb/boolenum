#!/usr/bin/env python
"""
Devinette without the time.sleep because here we mean to compute stats.
"""
import string
import random
from boolenumeration import *

class Devinette:
  def __init__(self, length = 30):
    letters = string.ascii_letters +  string.digits

    self._val = ""
    while (length > 0):
      self._val += random.choice(list(letters))
      length -= 1
  
  def ge(self,position, value):
    return ord(self._val[position]) >= value

  def le(self,position, value):
    return ord(self._val[position]) <= value
  
  def gt(self,position, value):
    return ord(self._val[position]) > value

  def lt(self,position, value):
    return ord(self._val[position]) < value
    
  def length_ge(self,value):
    return len(self._val) >= value

  def length_le(self,value):
    return len(self._val) <= value

  def length_gt(self,value):
    return len(self._val) > value

  def length_lt(self,value):
    return len(self._val) < value

if __name__ == '__main__':
  d = Devinette()
  


"""
devinette guessers, really simple ones.
"""

"""
The truth tester is straightforward. In the real world there will be pattern
matching or testing of response time here.
"""
class DevinetteTruthTester(BooleanEnumerationTruthTester):
  def test_truth(self, response):
    return response

"""
The message builder just returns a tuple representing what we wan
to test
"""

class DevinetteMB(BooltesterMessageBuilder):
  def build_gt(self, coordinates, value):
    return ('gt', coordinates, value)

  def build_lt(self, coordinates, value):
    return ('lt', coordinates, value)

  def build_ge(self, coordinates, value):
    return ('ge', coordinates, value)

  def build_le(self, coordinates, value):
    return ('le', coordinates, value)

"""
This sends the messages we want to get to the Devinette and returns 
the test truth response.
"""
class DevinetteConnector:
  _counter = 0
  def __init__(self, devinette):
    self._d = devinette
  def send_message(self, mesg):
    self._counter += 1
    if (mesg[1] == 'len'):
      if mesg[0] == 'gt':
        return self._d.length_gt(mesg[2])
      elif mesg[0] == 'lt':
        return self._d.length_lt(mesg[2])
      elif mesg[0] == 'ge':
        return self._d.length_ge(mesg[2])
      elif mesg[0] == 'le':
        return self._d.length_le(mesg[2])
    else:
      if mesg[0] == 'gt':
        return self._d.gt(mesg[1], mesg[2])
      elif mesg[0] == 'lt':
        return self._d.lt(mesg[1], mesg[2])
      elif mesg[0] == 'ge':
        return self._d.ge(mesg[1], mesg[2])
      elif mesg[0] == 'le':
        return self._d.le(mesg[1], mesg[2])

"""
No need to implement something specific for this case. 
We use greater-than
testing which is the default and we are testing values in the range 0-255 which
is normal if we want to guess byte values. If we were to guess values in a
greater range we would have to adjust the initial min_value / max_value
"""
class DevinetteBoolTester(BooleanEnumerationTester):
  pass


"""
in this code we compute the mean number of rounds to guess a byte.
It gets close to 8.21
"""
if __name__ == '__main__':
  from numpy import mean
  from pprint import pprint
  iterations = 100
  stats = []
  while iterations > 0:
    iterations -= 1
    tests = range(1, 250)
    tats = []
    for t in tests:
      d = Devinette(t)
  
      bt = DevinetteBoolTester(DevinetteConnector(d), DevinetteTruthTester(), DevinetteMB())
  
      # first guess length
  
      lengthpb = BooleanEnumerationProblem("len")
  
      total_length = bt.solve_problem(lengthpb)
  
      i = 0
      resstr = ""
      while i < total_length:
        problem = BooleanEnumerationProblem(i)
        guess = bt.solve_problem(problem)
        resstr += chr(guess)
        i += 1

      tats.append((t, bt.connector._counter))
    stats.append(tats)
  values = [ [ (t[1]) for t in lst ] for lst in stats ]
  i = 0
  series = {}
  while i < len(values[0]):
    series[i+1] = [ t[i] for t in values ]
    i += 1
  means = [ (val,mean(series[val])) for val in series ]
  pprint(means)
  roundperbyte = [ (val, mean(series[val]) / val) for val in series ]
  pprint(roundperbyte)
