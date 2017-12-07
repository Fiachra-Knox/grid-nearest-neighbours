import random
import math
import json

from utils import manhattan_distance, lowest_positive, maybe
from exceptions import UnrecognizedFormatError

class World:

  # Holds data on the world and the events within it
  # Methods allow listing of events nearby any given coordinate

  def __init__(self, min_coords=(0, 0),
               world_data_source=(21, 21),
               event_data_source=500):

    # Can either take a filename as a data source,
    # or randomly generate testing data of given size.
    # Supported file types: csv, txt (treated as csv), json

    self.off = tuple([-x for x in min_coords])
    event_nos = None

    given_world = isinstance(world_data_source, str)
    if given_world:
      ext = world_data_source.split('.')[-1]
      if ext in ['csv', 'txt']:
        event_nos = self.load_world_from_csv(world_data_source)
      elif ext == 'json':
        with open(world_data_source, 'r') as f:
          self.world = json.load(f)
        event_nos = []
        for row in self.world:
          for x in row:
            if x is not None:
              event_nos.append(x)
      else:
        raise UnrecognizedFormatError(
          world_data_source, 'is not in a recognized format.')
    else:
      if hasattr(world_data_source, '__getitem__'):
        self.size = world_data_source
      else:
        raise UnrecognizedFormatError(
          world_data_source, 'is not subscriptable or a filename.')

    given_events = isinstance(event_data_source, str)
    if given_events:
      ext = event_data_source.split('.')[-1]
      if ext in ['csv', 'txt']:
        event_nos = self.load_events_from_csv(event_data_source)
      elif ext == 'json':
        with open(event_data_source, 'r') as f:
          self.events = json.load(f)
        self.event_nos = list(self.events.keys())
      else:
        raise UnrecognizedFormatError(
          event_data_source, 'is not in a recognized format.')

    if event_nos is None:
      event_nos = random.sample(
        range(10**9), k=min(self.size[0]*self.size[1], event_data_source))

    if not given_world:
      self.generate_world(event_nos)
    if not given_events:
      self.generate_tickets(event_nos)

  def offset(self, x):
    return (x[0] + self.off[0], x[1] + self.off[1])

  def get(self, x):
    x = self.offset(x)
    return self.world[x[0]][x[1]]

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
    for j, row in enumerate(self.world):
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

  def load_world_from_csv(self, filename):
    # Returns the event numbers encoutered
    # in case data needs to be generated for them
    self.world = []
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
        self.world.append(row)
    self.world.reverse()
    self.size = (row_length, len(self.world))
    return event_nos

  def load_events_from_csv(self, filename):
    # Takes a CSV file with event id in the first column,
    # ticket prices and numbers available in the rest.
    # Returns the event numbers generated
    # so that they are available for world generation
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

  def generate_world(self, event_nos):
    # Randomly generates world data for testing purposes
    idx = 0
    # If we have very few events, spread them out well.
    p = min(0.1, len(event_nos)/(self.size[0]*self.size[1]))
    self.world = []
    for i in range(self.size[1]):
      row = []
      for j in range(self.size[0]):
        if maybe(p) and idx < len(event_nos):
          row.append(event_nos[idx])
          idx += 1
        else:
          row.append(None)
      self.world.append(row)

  def generate_tickets(self, event_nos):
    # Randomly generates ticket price and availability data for testing
    # Prices are stored in cents, not dollars!
    # So we need to convert them back for the user
    self.events = {}
    for x in event_nos:
      prices = []
      for i in range(random.randint(0, 20)):
        prices.append(random.randint(1, 10**4))
      tickets = {}
      for p in prices:
        if maybe():
          tickets[p] = random.randint(1, 10**5)
        else:
          tickets[p] = 0
      self.events[x] = tickets