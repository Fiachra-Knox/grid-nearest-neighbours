import random

from utils import maybe

def generate_grid(size, event_nos):
  # Randomly generates world data for testing purposes
  idx = 0
  # If we have very few events, spread them out well.
  p = min(0.1, len(event_nos)/(2*size[0]*size[1]))
  ret = []
  for i in range(size[1]):
    row = []
    for j in range(size[0]):
      if maybe(p) and idx < len(event_nos):
        row.append(event_nos[idx])
        idx += 1
      else:
        row.append(None)
    ret.append(row)
  return ret

def generate_events(event_nos):
  # Randomly generates ticket price and availability data for testing
  # Prices are stored in cents, not dollars!
  # So we need to convert them back for the user
  events = {}
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
    events[x] = tickets
  return events