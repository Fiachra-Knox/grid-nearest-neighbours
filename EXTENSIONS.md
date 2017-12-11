# Assumptions

We assume that users do not require information on events which are sold out
(i.e., have zero tickets available).

# Extensions

To support multiple events at the same location, there are at least two options.
The simpler approach is to use an empty list to represent an empty grid point
(instead of None, which is currently used),
and for each non-empty grid point, store a list of all events at that point.
A more involved approach would be to avoid storing data on empty points at all,
by using a sparse format
(i.e., instead of storing the events at each point,
store the coordinates of each event).
The second option could also speed up world generation; see below.

Assuming the total number of events is limited,
the program runs well at least up to grid sizes of 1000 \* 1000.
Beyond that, the dominant factor in the running time of the program
is the running time of the grid generation algorithm
(unless the number of queries required is enormous).
Therefore, the first change to make to deal with larger grid sizes
would be to switch to sparse grid generation and storage as described above.

Once this change is made, I would expect that the running time of each query
would become dominant.
The algorithm for finding nearest events iterates through distances d,
at each step collecting events at distance d,
until it finds the requested number of events.
Therefore, the running time is superlinear
in the distance to the nearest event.

We can improve this by creating, as a preprocessing step,
a 'zoomed-out' view of the grid where the events
from (say) 10 \* 10 subregions are collected into a single grid point.
Running our current algorithm on the zoomed-out grid will give us an estimate
for the distance on the original grid.
Specifically if the distance to the nearest event in the zoomed-out grid is d,
then the distance in the original grid lies in the range [10(d-2), 10(d+2)].
(Note that the nearest events in the zoomed-out grid may be different
from those in the original;
however, the distances to them will still be bounded.)
Now we can use these bounds to speed up the current nearest event algorithm
on the original grid,
since we only need to iterate over the obtained interval.

Naturally, this approach can be repeated to speed up the algorithm
on the zoomed-out grid as well.
So we will end up with a hierarchy of grids,
and use each one to bound the distance on the next finest grid.
With these improvements, I would expect the running time of the algorithm
to be at worst polylogarithmic in the grid size.