import random
import math
import json

from utils import manhattan_distance, lowest_positive, maybe
from exceptions import UnrecognizedFormatError

class World:

  # Holds data on the world and the events within it
  # Methods allow listing of events nearby any given coordinate

  def __init__(self, grid_data_source, event_data_source, min_coords=(0, 0)):

    # Takes filenames as data sources
    # Supported file types: csv, txt (treated as csv), json

    self.off = tuple([-x for x in min_coords])

    ext = grid_data_source.split('.')[-1]
    if ext in ['csv', 'txt']:
      event_nos = self.load_grid_from_csv(grid_data_source)
    elif ext == 'json':
      with open(grid_data_source, 'r') as f:
        self.grid = json.load(f)
      event_nos = []
      for row in self.grid:
        for x in row:
          if x is not None:
            event_nos.append(x)
    else:
      raise UnrecognizedFormatError(
        grid_data_source + ' is not in a recognized format.')


    ext = event_data_source.split('.')[-1]
    if ext in ['csv', 'txt']:
      event_nos = self.load_events_from_csv(event_data_source)
    elif ext == 'json':
      with open(event_data_source, 'r') as f:
        self.events = json.load(f)
      self.event_nos = list(self.events.keys())
    else:
      raise UnrecognizedFormatError(
        event_data_source + ' is not in a recognized format.')

  def offset(self, x):
    return (x[0] + self.off[0], x[1] + self.off[1])

  def get(self, x):
    x = self.offset(x)
    return self.grid[x[0]][x[1]]

  def get_lowest_price(self, x):
    if isinstance(x, tuple):
      x = self.get(x)
    if x is None:
      return math.inf
    return lowest_positive(self.events[x])

  def get_nearest_events(self, x, k=None):
    # Returns a sorted list of the k events nearest to x,
    # or all events if k is not specified.
    # Naive and very slow
    x = self.offset(x)
    nearest_events = []
    for j, row in enumerate(self.grid):
      for i, event_no in enumerate(row):
        if event_no is not None:
          price = lowest_positive(self.events[event_no])
          if price < math.inf:
            nearest_events.append((manhattan_distance(x, (i, j)), price, event_no))
    nearest_events.sort()
    if k is None:
      return nearest_events
    else:
      return nearest_events[:k]

  def print_nearest_events(self, x, k=None):
    nearest_events = self.get_nearest_events(x, k)
    print('Closest events to {0}:'.format(x))
    for event in nearest_events:
      print('Event {0:=9} - ${1:=5.2f}, Distance {2}'.format(
        event[2], event[1]/100, event[0]))

  def load_grid_from_csv(self, filename):
    # Returns the event numbers encoutered
    self.grid = []
    event_nos = []
    row_length = None
    with open(filename, 'r') as f:
      for line in f:
        raw_row = line.split(',')
        row = []
        for s in raw_row:
          if s.strip() == '':
            row.append(None)
          else:
            e = int(s)
            row.append(e)
            event_nos.append(e)
        if row_length is None:
          row_length = len(row)
        else:
          assert(row_length == len(row))
        self.grid.append(row)
    self.grid.reverse()
    self.size = (row_length, len(self.grid))
    return event_nos

  def load_events_from_csv(self, filename):
    # Takes a CSV file with event id in the first column,
    # ticket prices and numbers available in the rest.
    # Returns the event numbers generated
    self.events = {}
    with open(filename, 'r') as f:
      for line in f:
        if line.strip() == '':
          break
        raw_row = line.split(',')
        event_no = int(raw_row[0])
        tickets = {}
        for i in range(1, len(raw_row)):
          if raw_row[i].strip() != '':
            pair = raw_row[i].split(':')
            price = float(pair[0].strip().strip('$'))
            price = round(price*100)
            tickets[price] = int(pair[1])
        self.events[event_no] = tickets
    return list(self.events.keys())

