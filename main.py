import json
import math
import heapq

def main():
    #Opening of folders
    G = open("G.json")
    D = open("Dist.json")
    C = open("Coord.json")

    graph = json.load(G)
    dist = json.load(D)
    Coord = json.load(C)

    # Calculating distance of dict
    heuristicDict = {}
    targetCoord = Coord['50']
    for key, item in Coord.items():
        heuristicDict[key] = calcH(targetCoord, item)

    # Greedy algorithm
    print(greedySearch(graph, heuristicDict, "1", "50"))
     
def calcH(goal, cur):
    new_x = (goal[0] - cur[0]) 
    new_y = (goal[1] - cur[1])
    
    heuristicDistance = math.sqrt((new_x **2 + new_y ** 2))
    return heuristicDistance

def greedySearch(graph, heuristicDict, start, end):
    #Initialise
    shortestPathList = []
    path = []

    # Starting the greedy algo
    for element in graph[start]:
        heapq.heappush(path, (heuristicDict[element], element))
    
    while(len(path)!=0):
        visited = heapq.heappop(path)
        shortestPathList.append(visited)

        #Checking if its terminal
        if(visited[1] == end):
            return shortestPathList
        
        for element in graph[visited[1]]:
            heapq.heappush(path, (heuristicDict[element], element))  

    return -1
    
if __name__ == "__main__":
    main()


