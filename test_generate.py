import unittest
import random
from zlib import adler32

from generate import generate_grid, generate_events
from utils import save_grid_as_csv, save_events_as_csv

class TestGenerators(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.size = (21, 21)
    num_events = self.size[0]*self.size[1]
    random.seed('Look at all the pretty lights')
    self.event_nos = random.sample(range(10**9), k=num_events)

  def test_generate_grid(self):
    random.seed('New York, New York')
    grid = generate_grid(self.size, self.event_nos)
    save_grid_as_csv('temp.csv', grid)
    with open('temp.csv', 'rb') as f:
      self.assertEqual(adler32(f.read()), 2748486490)

  def test_generate_events(self):
    random.seed('You won\'t find them cheaper anywhere else!')
    events = generate_events(self.event_nos)
    save_events_as_csv('temp.csv', events)
    with open('temp.csv', 'rb') as f:
      self.assertEqual(adler32(f.read()), 4168537308)