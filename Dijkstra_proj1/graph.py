import heapq as hq
import pyavltree as atree
import time


class Node():
    def __init__(self, key, succ, parent_node, g_value):
        self.key = key
        self.parent_node = parent_node
        self.g_value = g_value;
        self.succ = succ
    def __str__(self):
        return str(self.key) + ", parent: "+self.parent_node+", G Value: "+self.g_value
    
def dijkstra(graph, src, dist):
    total_node_generated = 0
    expolored = atree.AVLTree() # AVL Tree
    frontier = []


    for item in graph:
        if item != src:
            hq.heappush(frontier,(float('inf'), Node(item, graph[item], None, float('inf') )))
            total_node_generated = total_node_generated + 1 
    hq.heappush(frontier,(0, Node(src, graph[src], None, 0 )))
    total_node_generated = total_node_generated + 1 

    while frontier != []:
        u = hq.heappop(frontier)
        expolored.insert(u[1].key, u)

        all_succ = u[1].succ
        for item in all_succ:
            # 1 --------------------------------
            # Helper place holders so we won't have to do the search more than once
            inExplored = expolored.find(item) 
            inFrontier = [[True,item2] for item2 in frontier if item2[1].key == u] # inFrontier will hold if node found: [True, item], else: []

            # 2 --------------------------------
            # Calculate new_g_value
            new_g_value = 0
            if u[1].key == float('inf'):
                      new_g_value =  0 + all_succ[item]
            else:
                      new_g_value =  u[1].g_value + all_succ[item]
            # 3 --------------------------------
            # case 1
            if inExplored == None and inFrontier == []:
                hq.heappush(frontier,(new_g_value, Node(item,graph[item], u, new_g_value )))
                total_node_generated = total_node_generated + 1 
            # case 2
            elif inFrontier != []:
                # Edge Relaxation
                # Ex. frontier = [True, (3, <__main__.Node instance at 0x7f6045676d40>)]
                if new_g_value < inFrontier[0][1][1].g_value:
                    frontier[0][1][1].update_g_value_and_parent(new_g_value, u)
                    inFrontier[0][1][1].g_value = new_g_value
                    inFrontier[0][1][1].parent_node = u
                    hq.heappush(frontier, (new_g_value, inFrontier[0][1][1]))
            # case 3: ui in Explored, Handling minus edges
            elif inExplored != None:
                # Check that this edge is not connecting back to the parent of the current node 
                if u[1].parent_node != None:
                    if u[1].parent_node[1].key != item:
                        if new_g_value < inExplored.data[1].g_value:
                            
                            inExplored.data[1].g_value = new_g_value
                            inExplored.data[1].parent_node = u
                            # Add it to Frontier and remove it from Explored
                            hq.heappush(frontier,(new_g_value,inExplored.data))
                            expolored.remove(item)
        if u[1].key in dist:
            tmp = []
            total_cost =0
            u[1].prent_node = u
            return u, total_node_generated

    return expolored, total_node_generated
 
def main(from_city = 'BWI', to_city = ['SFO','LAX']):
    arr_1 = []
    
    ##########################
    # Book Example 
    graph = {'SFO': {'DFW': 1464, 'LAX': 337, 'ORD': 1846, 'BOS': 2704},
            'LAX': {'SFO': 337, 'DFW': 1235, 'MIA':2342},
            'DFW': {'LAX': 1235, 'SFO': 1464, 'ORD': 802, 'JFK': 1391, 'MIA': 1121},
            'ORD': {'SFO': 1846, 'BOS': 867, 'PVD': 849, 'JFK': 740, 'BWI': 621, 'DFW': 802},
            'MIA': {'LAX': 2342, 'DFW': 1121, 'BWI': 946, 'JFK': 1090, 'BOS': 1258},
            'JFK': {'DFW': 1391, 'ORD': 740, 'BOS': 187, 'PVD': 144, 'MIA': 1090, 'BWI': 184},
            'PVD': {'JFK': 187, 'ORD': 849},
            'BOS': {'ORD': 867, 'SFO': 2704, 'MIA': 1258, 'JFK': 187},
            'BWI': {'ORD': 621, 'JFK': 184, 'MIA': 946}}

    start_time = time.time()

    result, total_node_generated = dijkstra(graph,from_city,to_city)
    cost = result[1].g_value


    while result[1].parent_node != None:
        arr_1.append(result[1].key) 
        result = result[1].parent_node

    arr_1.append(result[1].key)
    print "#"*30+" Graph Result "+"#"*30
    print '\n'
    print "Path: ",arr_1
    print "Cost: ",cost
    print "Total Nodes: ",total_node_generated
    print("--- %.5f seconds ---" % (time.time() - start_time))
    print '\n'

if __name__ == '__main__':
    main()