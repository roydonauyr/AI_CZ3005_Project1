from cmath import sqrt
import json
import math
import heapq
#Setting constants
START = "1"
END = "50"
MAX_ENERGY = 287932

def main():
    #Opening of folders
    G = open("G.json")
    D = open("Dist.json")
    C = open("Coord.json")
    Cost = open("Cost.json")

    graph = json.load(G)
    dist = json.load(D)
    coord = json.load(C)
    cost = json.load(Cost)
    
    

    # UCS
    print("----- UCS -----")
    print(specialAStar(graph, dist, cost, coord, START, END, False,False))

    #UCS with budget
    print("----- UCS with energy budget-----")
    print(specialAStar(graph, dist, cost, coord, START, END, True,False))

    #A* with budget
    print("----- A* with energy budget-----")
    print(specialAStar(graph, dist, cost, coord, START, END, True,True))

def specialAStar(graph, dist, cost, coord, start, end, budget,h):
    path = []
    pq = []
    dist_from_source = {}
    energy_from_source = {}
    parent = {}

    dist_from_source[start] = 0
    energy_from_source[start] = 0
    parent[start] = "-1"    
    heapq.heappush(pq, (0,start))
    num_nodes =0
    while (len(pq) != 0):
        distance, currNode = heapq.heappop(pq)
        num_nodes += 1
        if(currNode == end):
            break

        for neighbour in graph[currNode]:
            temp = currNode + "," + neighbour
            tempDist = dist_from_source[currNode] +  dist[temp]
            tempEnergy = energy_from_source[currNode] + cost[temp]

            if budget and tempEnergy > MAX_ENERGY:
                continue
            
            #Heuristic distance
            if(h):
                hdist = tempDist + calH(coord[neighbour], coord[end])
            
            if(neighbour not in dist_from_source):
                dist_from_source[neighbour] = tempDist
                energy_from_source[neighbour] = tempEnergy
                parent[neighbour] = currNode
                if(h):
                    heapq.heappush(pq, (hdist,neighbour))
                else:
                    heapq.heappush(pq, (tempDist,neighbour))
            elif(neighbour in dist_from_source):
                if(dist_from_source[neighbour] > tempDist):
                    dist_from_source[neighbour] = tempDist
                    energy_from_source[neighbour] = tempEnergy
                    parent[neighbour] = currNode
                    if(h):
                        heapq.heappush(pq, (hdist,neighbour))
                    else:
                        heapq.heappush(pq, (tempDist,neighbour))
                    

 

    # backtrack the final path
    cur_node = end

    while cur_node != "-1":
        path.append(cur_node)
        cur_node = parent[cur_node]
    path.reverse()

    # print path
    print("Shortest Path:", " -> ".join(path))
    # print distance
    print("Shortest Distance:", dist_from_source[end])
    # print number of nodes expanded
    print(f"Nodes expanded: {num_nodes}\n")
    # print energy cost
    if(budget):
        print("Total energy cost:", energy_from_source[end])

def calH(first_coord, second_coord):
    x_dist = (second_coord[0] - first_coord[0]) **2
    y_dist = (second_coord[1] - first_coord[1]) **2

    manhattan = abs(second_coord[0] - first_coord[0]) + abs(second_coord[1] - first_coord[1])

    average = (manhattan + math.sqrt(x_dist + y_dist))/2

    return average

    # Only uses diagonal distance
    # return math.sqrt(x_dist + y_dist)

if __name__ == "__main__":
    main()