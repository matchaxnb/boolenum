#!/usr/bin/env python3


"""
abstraction of a boolean enumeration problem. such problems are meant to get a
single character's value in a blind system such as a blind SQLi injection.

* wanted_data_coordinates is a tuple defining the /coordinates/ of data we want 
(bound to implementation of the connector). For example a SQL boolean enumerator
will want to define it as (table_fully_qualified_path, row, column, character)

* connector enables sending the boolean enumeration queries to the data source.
It is a target-specific class with facilities to send truth tests to the target.
It exposes a send_message method that returns a response state. The caller (for
example a tester) can then analyze the response state and deduce if an assertion
is true or false (time-based attacks, presence or absence of a string…)
"""
class BooleanEnumerationProblem:
  def __init__(self, wanted_data_coordinates):
    self.coordinates = wanted_data_coordinates

"""
Truth tester prototype. It takes a connector's output and can tell whether its
assertion is true or false.
Needs a different implementation for each target.
"""
class BooleanEnumerationTruthTester:
  def test_truth(self, response_status):
    if response_status['answer_time'] > 10 or 'Connected' in response_status['body']:
      return True
    return False

"""
Example message builder
"""
class BooltesterMessageBuilder:
  def build_gte(self, coordinates, value):
    pass

  def build_lt(self, coordinates, value):
    pass

  def build_lte(self, coordinates, value):
    pass

  def build_gt(self, coordinates, value):
    pass

  def build_eq(self, coordinates, value):
    pass

"""
prototype of a boolean enumeration tester. It is fed with problems and it gives
results. It is generic and needs not be extended usually.

It uses in this implementation a greater-than / less-than-or-equal testing. If
you cannot get these truths then implement it with lt / ge testing.

We are testing values in the range 0-255 because these are the possible values
for a byte. However in cases where another continuous finite number of integer
values are possible this would need to be adjusted accordingly.

We use the efficient bisection (binary search) algorithm to guess the value.
"""
class BooleanEnumerationTester:
  def __init__(self, connector, truthtester, messagebuilder):
    self.connector = connector
    self.truthtester = truthtester
    self.messagebuilder = messagebuilder

  def solve_problem(self, problem):
    coordinates = problem.coordinates
    # we search for a byte value
    min_value = 0
    max_value = 255
    to_test = max_value - (max_value - min_value) // 2
    while min_value != max_value:
      test = self.messagebuilder.build_gt(coordinates,to_test)
      resp = self.connector.send_message(test)
      if self.truthtester.test_truth(resp):
        min_value = to_test + 1
      else:
        max_value = to_test
      to_test = max_value - (max_value - min_value) // 2
      if (max_value - min_value == 1):
        test = self.messagebuilder.build_le(coordinates, min_value)
        resp = self.connector.send_message(test)
        if self.truthtester.test_truth(resp):
          max_value = min_value
        else:
          min_value = max_value 
      print("End of round. mV: %s MV: %s" % (min_value, max_value))
    print("End of search, mV: %s MV: %s" % (min_value, max_value))
    return min_value
