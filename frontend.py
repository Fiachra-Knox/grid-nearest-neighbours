import random
import argparse

from generate import generate_grid, generate_events
from utils import save_grid_as_csv, save_events_as_csv
from world import World

# Grid and event parameters
min_coords = (-10, -10)
size = (21, 21)
num_events = size[0]*size[1]

# Filenames (extension must always be .csv or .txt)
grid_filename = 'temp_grid.csv'
events_filename = 'temp_events.csv'

# Number of events to print in response to each user query
k = 5

# Common list of event numbers is generated seperately
event_nos = random.sample(range(10**9), k=num_events)

# Create grid and events files to feed to World
grid = generate_grid(size, event_nos)
save_grid_as_csv(grid_filename, grid)
del grid
events = generate_events(event_nos)
save_events_as_csv(events_filename, events)
del events

# Create world and answer user queries
w = World(grid_filename, events_filename, min_coords=min_coords)
while True:
  inp = input('Please Input Coordinates: ')
  print('')
  if inp in ['exit', 'quit', 'logout']:
    break
  inp = inp.split(',')
  if len(inp) != 2:
    print('Error: Expected 2 coordinates, received %d.' % len(inp))
    print('Please Input Exactly Two Coordinates.\n')
    continue
  try:
    x = [int(s) for s in inp]
  except ValueError:
    print('Error: Coordinates must be integers.')
    print('Please Input Integer Coordinates.\n')
    continue
  for i in range(2):
    if x[i] < min_coords[i] or x[i] >= min_coords[i] + size[i]:
      print('Warning: Coordinate %d is out of bounds.' % x[i])
  print('')
  w.print_nearest_events(x, k=k)
  print('')