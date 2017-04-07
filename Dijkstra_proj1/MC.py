import heapq as hq
import pyavltree as atree
import time
import math

total_node_generated = 0
Max_Boat_Capcity = 0
children_avl = atree.AVLTree()

class State():
    #def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight, g_value = 1 ):
    def __init__(self, cannibalLeft, missionaryLeft, boat, cannibalRight, missionaryRight, g_value = 1 ):
        self.cannibalLeft = cannibalLeft
        self.missionaryLeft = missionaryLeft
        self.boat = boat
        self.cannibalRight = cannibalRight
        self.missionaryRight = missionaryRight
        self.parent = None
        self.g_value = g_value
    def __str__(self):
        return "("+str(self.missionaryLeft)+","+str(self.cannibalLeft)+","+str(self.boat)+","+str(self.missionaryRight)+","+str(self.cannibalRight)+")"
    def get_g_value(self):
        return self.g_value
    def set_g_value(self, new_g):
        self.g_value = new_g
    def is_goal(self):
        if self.cannibalLeft == 0 and self.missionaryLeft == 0:
            return True
        else:
            return False
    def is_valid(self):
        if self.missionaryLeft >= 0 and self.missionaryRight >= 0 \
                   and self.cannibalLeft >= 0 and self.cannibalRight >= 0 \
                   and (self.missionaryLeft == 0 or self.missionaryLeft >= self.cannibalLeft) \
                   and (self.missionaryRight == 0 or self.missionaryRight >= self.cannibalRight):
            return True
        else:
            return False
    def __hash__(self):
        return hash((self.cannibalLeft, self.missionaryLeft, self.boat, self.cannibalRight, self.missionaryRight))




def successors(cur_state):
        global Max_Boat_Capcity
        global total_node_generated
        global children_avl
        children = []
        if cur_state.boat == 'left':
                for m in range(Max_Boat_Capcity +1):
                        for c in range(Max_Boat_Capcity +1):
                                if m+c > 0 and m+c <= Max_Boat_Capcity :
                                        #print 'yes 1'
                                        new_state = State(cur_state.cannibalLeft - c, cur_state.missionaryLeft - m, 'right',cur_state.cannibalRight + c , cur_state.missionaryRight + m)
                                        if new_state.is_valid() and children_avl.find(new_state.__hash__()) == None:
                                                new_state.parent = cur_state
                                                children.append(new_state)
                                                children_avl.insert(new_state.__hash__(), new_state)
        else:
                for m in range(Max_Boat_Capcity +1):
                        for c in range(Max_Boat_Capcity +1):
                                if m+c > 0 and m+c <= Max_Boat_Capcity :
                                        #print 'yes 2'
                                        new_state = State(cur_state.cannibalLeft + c, cur_state.missionaryLeft + m, 'left',cur_state.cannibalRight - c , cur_state.missionaryRight - m)
                                        if new_state.is_valid() and children_avl.find(new_state.__hash__()) == None:
                                                new_state.parent = cur_state
                                                children.append(new_state)
                                                children_avl.insert(new_state.__hash__(), new_state)
        total_node_generated = total_node_generated + len(children)
        return children



###########################

#def dijkstra(c,m):
def dijkstra(n):
    
    initial_state = State(n,n,'left',0,0)
    if initial_state.is_goal():
		return initial_state

    explored = atree.AVLTree() # AVL Tree
    frontier = []

    hq.heappush(frontier,(initial_state.get_g_value(),initial_state))
    
    #debug_arr = []
    while frontier != []:
        
        state = hq.heappop(frontier)[1]

        if state.is_goal():
			return state
        explored.insert(state.__hash__(), state)
        children = successors(state)
        for item in children:
            # 1 --------------------------------
            # Helper place holders so we won't have to do the search more than once
            inExplored = explored.find(item.__hash__()) 
            inFrontier = [[True,item2] for item2 in frontier if item2.__hash__() == state.__hash__()] # inFrontier will hold if node found: [True, item], else: []

            # 2 --------------------------------
            # Calculate new_g_value
            new_g_value =  state.get_g_value() + item.get_g_value()

            # 3 --------------------------------
            # case 1
            if inExplored == None and inFrontier == []:
                hq.heappush(frontier,(item.get_g_value(),item))
            # case 2
            elif inFrontier != []:
                # Edge Relaxation
                # Ex. frontier = [True, (3, <__main__.Node instance at 0x7f6045676d40>)]
                if new_g_value < inFrontier[0][1].get_g_value():
                    inFrontier[0][1].set_g_value(new_g_value)
                    hq.heappush(frontier,(new_g_value,inFrontier[0][1]))
                    
            # case 3: ui in Explored
            elif inExplored != None:
                # Check that this edge is not connecting back to the parent of the current node 
                if state.parent != None:
                    if state.parent.__hash__() != item.__hash__():
                        if new_g_value < inExplored.data.get_g_value():
                            inExplored.data.set_g_value(new_g_value)
                            inExplored.data.parent = state
                            # Add it to Frontier and remove it from Explored
                            hq.heappush(frontier,(new_g_value,inExplored.data))
                            explored.remove(item.__hash__())
    #return debug_arr
    return None

#def main(m, c):
def main(n, m):
    global total_node_generated
    global Max_Boat_Capcity
    global children_avl 

    children_avl = None # Free the memory
    children_avl = atree.AVLTree()
    Max_Boat_Capcity = m
    total_node_generated = 1    # 1 to count for the first node  

    start_time = time.time()

    result = dijkstra(n)

    end_time = (time.time() - start_time)

    if result != None:
        arr_1 = []
        cost = 0
        while result != None:
            arr_1.append(result.__str__())
            cost = cost + result.get_g_value()
            result = result.parent

        print "#"*30+" Missionries And Cannibals Result "+"#"*30
        print '\n'
        print "Path: ",arr_1
        print "Cost: ",cost -1 # The -1 because to get to the first node it costs 0, but the program has cost 1 by default for each edge
        print "Total Nodes: ",total_node_generated
        print("--- %.5f seconds ---" % end_time)
        print '\n'
