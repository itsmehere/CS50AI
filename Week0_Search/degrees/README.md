# Six Degrees of Kevin Bacon

According to the [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon) game, anyone in the Hollywood film industry is connected to Kevin Bacon within 6 steps. Each step is considered a movie where both actors starred in.

This problem uses the [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) algorithm to figure out the shortest path between any two actors by choosing a sequence of movies that connects them. 

For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

As a search problem: 
 - The states are people.
 - The actions are movies(take us from one actor to another).
 - Our initial state is the starting actor(Jennifer Lawrence in the above example).
 - The Goal state is the actor we want to get to(Tom Hanks in the above example).

By using breadth-first search, we can reliably find the shortest path from one actor to another.

## Usage

``` python
python degrees.py large # To use the large dataset
```
or
``` python
python degrees.py small # To use the small dataset
```

