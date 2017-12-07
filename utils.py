import math
import random

def manhattan_distance(x_1, x_2):
  # Calculates the Manhattan distance between two points in n-dim space.
  ret = 0
  for t in zip(x_1, x_2):
    ret += abs(t[0] - t[1])
  return ret

def lowest_positive(d):
  # Returns the lowest key from d whose value is positive
  # Returns math.inf if no key has a positive value
  for x in sorted(d):
    if d[x] > 0:
      return x
  return math.inf

def maybe(p=0.5):
  # Random event which occurs with probability p
  return random.random() < p

def save_grid_as_csv(filename, grid):
  with open(filename, 'w') as f:
    for row in reversed(grid):
      str_row = []
      for x in row:
        if x is None:
          str_row.append('')
        else:
          str_row.append(str(x))
      f.write(','.join(str_row))
      f.write('\n')

