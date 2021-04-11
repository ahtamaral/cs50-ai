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
    with open(f"../data/{directory}/people.csv", encoding="utf-8") as f:
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
    with open(f"../data/{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"../data/{directory}/stars.csv", encoding="utf-8") as f:
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
    # O diretório acessado para obter os dados depende do argumento dado na CLI
    # No caso de omissão, ele acessa diretamento o diretório large/. Caso queiramos
    # Acessar os dados de small/ devemos especificar através do argv.
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")


    # Entrada do ator inicial (Estado inicial).
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    # Entrada do ator final (Estado final).
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Função que vou implementar com o algoritmo BFS.
    # Ela tem que receber uma lista de nós
    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")

    #-------------------------------------------------
    # CUIDADO: Minha implementação para a identificação
    # de igualdade entre ator inicial e final se baseia na
    # avaliação do comprimento da lista path (Se for igual a 1
    # ele considera que houve essa repetição). Pode ser que,
    # uma vez implementado o BFS, essa condição ocorra mesmo
    # para estados inicial e final distintos. Ficar atento a isso.
    # Implementei dessa forma pois a main() implementada apresentava
    # um SegFault quando encontrava essa ocasião. A implementação
    # da main precisa sempre acessar a posição i+1 de path.
    # Poderia ter sido uma opção implementar uma variável chamada
    # "extremosCoincidem", de valor 0 ou 1, e adicioná-la a i, 
    # dessa forma inalterando a implementação e saída de dados
    # original.
    #-------------------------------------------------

    elif len(path) == 1:
        degrees = 0
        print("Initial actor and target actor are the same.")
        print(f"{degrees} degrees of separation.")
        person = people[path[0].state]["name"]
        print(f"{person} starred all his movies with himself.")

    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


# Chamar por frontier retorna um objeto da classe QueueFrontier.
# Chamar por frontier.frontier retorna uma lista contendo os nós na fronteira.


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    startNode = Node(state = source, parent = None, action = None)
    frontier = QueueFrontier()
    frontier.add(startNode)
    if startNode.state == source: # Comparação válida: Ambas são ID
        return frontier.frontier

    # Dentro do Loop
    # while...
    # Expandir o nó (Encontrar seus vizinhos)
    neighbors = neighbors_for_person(startNode.state)
    print(neighbors)

    # TODO
    #raise NotImplementedError


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
            if person_id in person_ids:
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
