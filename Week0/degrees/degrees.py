import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    start = Node(source, None, None) # Create a Node for the starting person
    goal = Node(target, None, None) # Create a Node for the ending person
    frontier = QueueFrontier() # Create frontier to store Nodes
    frontier.add(start) 
    exploredNodes = set() # Create a set to keep track of Nodes we have already visited(optimization)
    shortestPath = [] # Lastly, a list that tells us how we got from start -> goal
    
    while frontier is not None:
        # Remove the first Node & get a list of all it's children(neighbors)
        currentNode = frontier.remove()
        listOfNeighbors = neighbors_for_person(currentNode.state)
        
        # Loop through the neighbors one by one
        for neighbor in listOfNeighbors:
            if neighbor not in exploredNodes:
                # Create a new Node for the neighbor that includes their state, parent, and action
                # given to us by listOfNeighbors
                neighborsNode = Node(neighbor[1], currentNode, neighbor[0])
                # Another optimization where we check to see if the node's state is our goal's state before
                # we add to the frontier. This saves time because we don't have to wait till the node's turn
                # before it's checked.
                if neighborsNode.state == goal.state:
                    # Back track our way to the starting point so we know the path. This path is then 
                    # reversed so its in order from start -> goal; not goal -> start.
                    while neighborsNode.state != start.state:
                        shortestPath.append((neighborsNode.action, neighborsNode.state))
                        neighborsNode = neighborsNode.parent
                    return shortestPath[::-1]
                # Lastly, if the frontier doesn't already contain the node, we add it to both the frontier
                # and the explored Nodes.
                elif not frontier.contains_state(neighborsNode.state):
                    frontier.add(neighborsNode)
                    exploredNodes.add(neighborsNode)
    


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids  :
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
