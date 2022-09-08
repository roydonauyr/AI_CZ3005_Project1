import json
import math
import heapq

MAX_ENERGY = 287932

def main():
    #Opening of folders
    G = open("G.json")
    D = open("Dist.json")
    C = open("Coord.json")
    Cost = open("Cost.json")

    graph = json.load(G)
    dist = json.load(D)
    Coord = json.load(C)
    cost = json.load(Cost)
    
    # Calculating distance of dict
    # heuristicDict = {}
    # targetCoord = Coord['50']
    # for key, item in Coord.items():
    #     heuristicDict[key] = calcH(targetCoord, item)

    # # Greedy algorithm
    # print(greedySearch(graph, heuristicDict, "1", "50"))

    # UCS
    print("----- UCS -----")
    ucs(graph, dist, cost, "1", "50")
     
def calcH(goal, cur):
    new_x = (goal[0] - cur[0]) 
    new_y = (goal[1] - cur[1])
    
    heuristicDistance = math.sqrt((new_x **2 + new_y ** 2))
    return heuristicDistance

def greedySearch(graph, heuristicDict, start, end):
    #Initialise
    shortestPathList = []
    pq = []

    # Starting the greedy algo
    for element in graph[start]:
        heapq.heappush(pq, (heuristicDict[element], element))
    
    for i in range(5):
        visited = heapq.heappop(pq)
        shortestPathList.append(visited)

        #Checking if its terminal
        if(visited[1] == end):
            return shortestPathList
        
        for element in graph[visited[1]]:
            heapq.heappush(pq, (heuristicDict[element], element))  

    return -1

# A* Search
def a_star(graph, dist, cost, start, end, with_energy=False, heuristic=lambda u: 0):
    # Min priority queue -> (priority, cur_node)
    pq = []
    path = []
    prev = {}
    dist_from_source = {}
    energy_from_source = {}

    dist_from_source[start] = 0
    energy_from_source[start] = 0
    prev[start] = "-1"
    heapq.heappush(pq, (0, start)) 

    # Number of nodes expanded
    num_nodes = 0

    while len(pq) != 0:
        distance, cur_node = heapq.heappop(pq)
        num_nodes += 1

        # Reaches goal state
        if cur_node == end:
            break

        # Push neighbours that are not done yet
        for adjacent in graph[cur_node]:
            temp = cur_node + "," + adjacent
            new_distance_taken = dist_from_source[cur_node] + dist[temp]
            new_energy_taken = energy_from_source[cur_node] + cost[temp]

            # f = g + h
            new_priority = new_distance_taken + heuristic(adjacent)

            # skip if energy is more than budget (if applicable)
            if with_energy and new_energy_taken > MAX_ENERGY:
                continue
            
            # update if not in visited and new distance is shorter
            if adjacent not in dist_from_source or new_distance_taken < dist_from_source[adjacent]:
                dist_from_source[adjacent] = new_distance_taken
                energy_from_source[adjacent] = new_energy_taken
                prev[adjacent] = cur_node
                heapq.heappush(pq, (new_priority, adjacent))

    # backtrack the final path
    cur_node = end

    while cur_node != "-1":
        path.append(cur_node)
        cur_node = prev[cur_node]
    
    # reverse path, as it was in backwards direction
    path.reverse()

    # print path
    print("Shortest Path:", " -> ".join(path))

    # print distance
    print("Shortest Distance:", dist_from_source[end])

    # print energy
    if with_energy:
        print("Total Energy Cost:", energy_from_source[end])

    # print number of nodes expanded
    print(f"Nodes expanded: {num_nodes}\n")


# Uniform Cost Search
def ucs(graph, dist, cost, start, end):
    # UCS = A* Search with no heuristic function
    a_star(graph, dist, cost, start, end, with_energy=False, heuristic=lambda u: 0)
    
if __name__ == "__main__":
    main()


