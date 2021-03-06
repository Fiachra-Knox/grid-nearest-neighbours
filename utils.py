import math
import random
from zlib import adler32
from collections import defaultdict

def manhattan_distance(x_1, x_2):
  # Calculates the Manhattan distance between two points in n-dim space.
  # Takes integer tuples x_1 and x_2 of the same length.
  distance = 0
  for t in zip(x_1, x_2):
    distance += abs(t[0] - t[1])
  return distance

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

def sparse_grid_diagonals(dense_grid, ascending=False):
  # Turns a grid into a dictionary (with default value []);
  # keys are k such that the diagonal x + y = k is nonempty
  # Values are lists of coordinates and values of non-null entries.
  sparse_diagonals = defaultdict(list)
  if ascending:
    off = len(dense_grid) - 1
    f = lambda i, j: i - j
  else:
    f = lambda i, j: i + j
  for j, row in enumerate(dense_grid):
    for i, x in enumerate(row):
      if x is not None:
        sparse_diagonals[f(i, j)].append((i, j, x))
  if not ascending:
    for key in sparse_diagonals:
      sparse_diagonals[key].reverse()
  return sparse_diagonals

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

def save_events_as_csv(filename, events):
  with open(filename, 'w') as f:
    for e in sorted(events):
      line = [str(e)]
      for price in sorted(events[e]):
        line.append('${0:.2f}:{1}'.format(price/100, events[e][price]))
      f.write(','.join(line))
      f.write('\n')

def file_already_exists(filename, checksum):
  try:
    with open(filename, 'rb') as f:
      return adler32(f.read()) == checksum
  except FileNotFoundError:
    return False
