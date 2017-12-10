import random
import argparse

from generate import generate_grid, generate_events
from utils import save_grid_as_csv, save_events_as_csv
from world import World

parser = argparse.ArgumentParser(
  description='creates a random world and finds nearest events')
parser.add_argument(
  '-s', '--seed', type=str, default='none',
  help='use SEED as a seed for the random number generator')
parser.add_argument(
  '-n', '--num_events', type=int, default=-1,
  help='limit number of events to a maximum of NUM_EVENTS')
parser.add_argument(
  '-mx', '--minx', type=int, default=-10,
  help='use MINX as the least x-coordinate of the world (default -10)')
parser.add_argument(
  '-my', '--miny', type=int, default=-10,
  help='use MINY as the least y-coordinate of the world (default -10)')
parser.add_argument(
  '-Mx', '--maxx', type=int, default=10,
  help='use MAXX as the greatest x-coordinate of the world (default 10)')
parser.add_argument(
  '-My', '--maxy', type=int, default=10,
  help='use MAXY as the greatest y-coordinate of the world (default 10)')
parser.add_argument(
  '-r', '--return_length', type=int, default=5,
  help='return up to RETURN_LENGTH responses to each query (default 5)')
parser.add_argument(
  '-g', '--grid', type=str, default='temp_grid',
  help='write grid data to GRID.csv (default temp_grid.csv)')
parser.add_argument(
  '-e', '--events', type=str, default='temp_events',
  help='write event data to EVENTS.csv (default temp_events.csv)')
args = parser.parse_args()

# Grid and event parameters
min_coords = (args.minx, args.miny)
size = (args.maxx - args.minx + 1, args.maxy - args.miny + 1)
for i in range(2):
  if size[i] <= 0:
    print('Warning: Grid has invalid size; using default instead.')
    size[i] = 21
if args.num_events < 0:
  num_events = size[0]*size[1]
else:
  num_events = min(args.num_events, size[0]*size[1])

# Accept a seed if given, for testing purposes
if args.seed != 'none':
  random.seed(args.seed)

# Common list of event numbers for grid and events
event_nos = random.sample(range(10**9), k=num_events)

# Filenames (extension must always be .csv or .txt)
for forb in '#%&{}\\<>*?/ $!\'\":@\n\t':
  if forb in args.grid:
    print('Warning: Grid filename has invalid characters. Using default.')
    grid_filename = 'temp_grid.csv'
    break
else:
  if len(args.grid) > 27:
    print('Warning: Grid filename is too long and will be truncated.')
    grid_filename = args.grid[:27] + '.csv'
  else:
    grid_filename = args.grid + '.csv'

for forb in '#%&{}\\<>*?/ $!\'\":@\n\t':
  if forb in args.events:
    print('Warning: Events filename has invalid characters. Using default.')
    events_filename = 'temp_events.csv'
    break
else:
  if len(args.events) > 27:
    print('Warning: Events filename is too long and will be truncated.')
    events_filename = args.events[:27] + '.csv'
  else:
    events_filename = args.events + '.csv'

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
  inp = input('\nPlease Input Coordinates: ')
  print('')
  if inp in ['exit', 'quit', 'logout']:
    break
  inp = inp.split(',')
  if len(inp) != 2:
    print('Error: Expected 2 coordinates, received %d.' % len(inp))
    print('Please Input Exactly Two Coordinates.')
    continue
  try:
    x = [int(s) for s in inp]
  except ValueError:
    print('Error: Coordinates must be integers.')
    print('Please Input Integer Coordinates.')
    continue
  for i in range(2):
    if x[i] < min_coords[i] or x[i] >= min_coords[i] + size[i]:
      print('Warning: Coordinate %d is out of bounds.\n' % x[i])
  w.print_nearest_events(x, k=args.return_length)