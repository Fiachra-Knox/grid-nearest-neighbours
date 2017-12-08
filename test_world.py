import unittest
import random
from time import process_time

from world import World
from generate import generate_events, generate_grid
from utils import save_grid_as_csv, save_events_as_csv, file_already_exists
from exceptions import UnrecognizedFormatError

class TestWorld(unittest.TestCase):

  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)

    size = (21, 21)
    num_events = size[0]*size[1]
    random.seed('Look at all the pretty lights')
    event_nos = random.sample(range(10**9), k=num_events)
    if not file_already_exists('grid_testcase_2.csv', 2748486490):
      random.seed('New York, New York')
      grid = generate_grid(size, event_nos)
      save_grid_as_csv('grid_testcase_2.csv', grid)
    if not file_already_exists('events_testcase_2.csv', 4168537308):
      random.seed('You won\'t find them cheaper anywhere else!')
      events = generate_events(event_nos)
      save_events_as_csv('events_testcase_2.csv', events)

    n=10**3
    num_events=10**4
    size = (2*n + 1, 2*n + 1)
    random.seed('Now we have a lot of events')
    event_nos = random.sample(range(10**9), k=num_events)
    if not file_already_exists('grid_testcase_3.csv', 2409672020):
      random.seed('Now the world is a lot bigger')
      grid = generate_grid(size, event_nos)
      save_grid_as_csv('grid_testcase_3.csv', grid)
    if not file_already_exists('events_testcase_3.csv', 3963271492):
      random.seed('We have to generate details for all these many events')
      events = generate_events(event_nos)
      save_events_as_csv('events_testcase_3.csv', events)

  def test_errors(self):
    with self.assertRaises(UnrecognizedFormatError):
      w = World(min_coords=(-2, -2),
                grid_data_source='session',
                event_data_source='events_testcase_1.csv')
      w.print_nearest_events((-1, -1), k=5)
    with self.assertRaises(UnrecognizedFormatError):
      w = World(min_coords=(-2, -2),
                grid_data_source='grid_testcase_1.csv',
                event_data_source='session')
      w.print_nearest_events((-1, -1), k=5)

  def test_deterministic_cases(self):
    w = World(min_coords=(-2, -2),
              grid_data_source='grid_testcase_1.csv',
              event_data_source='events_testcase_1.csv')
    self.assertEqual(
      w.get_nearest_events((-1, -1), k=5),
      [(2, 100, 7), (3, 2738, 5), (3, 53589, 6), (4, 1000, 1), (5, 1500, 2)])

  def test_random_cases(self):
    w = World(min_coords=(-10, -10), grid_data_source='grid_testcase_2.csv',
              event_data_source='events_testcase_2.csv')
    self.assertEqual(
      w.get_nearest_events((-1, -1), k=10),
      [(3, 230, 875072028), (5, 679, 590672579), (5, 3732, 94611473),
       (6, 3821, 888911603), (6, 4050, 687618495), (7, 3719, 188918206),
       (7, 5202, 235950439), (9, 665, 974344725), (10, 143, 762308638),
       (10, 668, 602022355)])

  def test_large_cases(self):
    t = process_time()
    w = World(grid_data_source='grid_testcase_3.csv',
              event_data_source='events_testcase_3.csv',
              min_coords=(-1000, -1000))
    t = process_time() - t
    self.assertLess(t, 2)

    t = process_time()
    answer = w.get_nearest_events((-100, 100), k=10)
    t = process_time() - t
    self.assertEqual(answer,
      [(5, 1419, 916234323), (12, 1386, 584561230), (30, 2, 300911460),
       (34, 616, 501582957), (42, 126, 129773648), (43, 2612, 921336850),
       (44, 735, 920746258), (44, 5864, 839723794), (45, 2341, 476481568),
       (47, 1830, 559403626)])
    self.assertLess(t, 0.5)

  def test_speed(self):
    t = process_time()
    w = World(grid_data_source='grid_testcase_3.csv',
              event_data_source='events_testcase_3.csv',
              min_coords=(-1000, -1000))
    t = process_time() - t
    self.assertLess(t, 2)

    t = process_time()
    answer = w.get_nearest_events((-100, 100), k=10)
    t = process_time() - t
    self.assertLess(t, 0.05)