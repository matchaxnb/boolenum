# boolenum

Proposal for a boolean enumeration (bisection method, aka binary search) 
sample implementation in Python. I tried to genericize what we usually do when
writing such tools which are often tailor-made.

## When to use it?

When you face a blind SQL injection problem and you want to PoC a data dump.

## How to use it?

Derive the BoolenumMessageBuilder class to send messages to your targets that 
will return different results according to the truth-status of the statement you
test (SQL injection code is your own business and I will provide no help here, 
build your own skills up).

Guess the length of data you want to dump, then character after character, get
the value.

## Suggestions

Do not dump column after column but rather use a CONCAT of the values of
interest to you (so you can run the dump unattended). 

The less verbose, the better. It usually takes between 8 and 10 tests to 
bisect to a byte value so do not guess noise characters.

These operations are parallelizable, you can have many workers guessing a
character each.

## How to test?

I wrote a tester, not using SQL injections but rather a class encapsulating
a random string and giving out indications on the value of each character.

Run python3 devinette.py and see it work.
