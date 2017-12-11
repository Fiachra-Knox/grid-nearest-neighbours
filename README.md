# grid-nearest-neighbours
This project contains functions for generating and querying integer grids.
Each point of the grid is either empty or contains a single event.
Each event may have tickets available;
if not, the event is considered to be sold out.

A front-end is provided as *frontend.py*.
This program generates randomly an integer grid.
Once the grid is generated, the program requests coordinates from the user.
The program prints a list of the nearest events to the requested coordinates.
Events which are sold out are disregarded,
and ties are broken by lowest ticket price.
If there are not enough events on the grid,
the program simply lists all events
in order of distance to the given coordinates.
Any number of queries can be made; type 'exit' to exit.

frontend.py can be run directly from the command-line
with Python 3.6 or later installed (python frontend.py).
By default it generates the grid [-10, 10] \* [-10, 10],
and even if a larger grid is specified
it will not generate more than 10000 events.
The grid and event data are saved to *temp_grid.csv* and *temp_events.csv*,
which can be examined afterwards if desired.
In response to each query the program will return 5 events.
The default behaviour can be changed using the following arguments:

* **--minx, --maxx, --miny, --maxy**:
Set the minimum and maximum coordinates of the grid along the x- and y-axes.
* **--num_events**: Set the maximum number of events to be generated.
This only impacts the running of the program
if it is much less than the number of grid squares.
If a negative number is given,
there will be no limit on the number of events generated.
* **--seed**: Set the seed for the random number generator.
Using the same seed and other parameters will ensure the same behaviour,
which can be useful for testing.
* **--grid, --events**: Set the filenames for the grid and events files.
The extension *.csv* is automatically appended.
* **--return_length**:
Set the number of events to print in response to each query.

The functionality of the project can also be imported for use in Python.
The generate module contains functions for generating grids and events.
The world module contains the World class,
which represents an integer grid containing events,
in a way that allows for efficiently finding
the nearest events to a grid point.
The utils module provides utility functions for working with
integer grids, dictionaries, random program flow and csv files.

The grid generator runs in seconds up to grid size of 10^7.
The event generator can generate up to 10^4 events in seconds.
On grids with balanced dimensions individual queries run quickly,
but if one dimension is very large and the number of events is small,
each query can take over a second to run.