import heapq as hq
#import pyavltree as atree
import time
import math
import random
#import hashmap

total_node_generated = 0
children_avl = None
children_dict = {}
frontier_avl = None
current_level_g_value = 0
goal = ''
n_value =0
frontier_dict = {} # Dictionary

class State():
    def __init__(self, arrangment, g_value, h_value, f_value, parent):
        self.g_value = g_value
        self.arrangment = arrangment
        self.f_value = f_value  # f = h(n) + g(n) .. h(n) is the huristic value, g(n) is the cost value
        self.parent = parent
        self.h_value = h_value
    
    def empty_space_location(self):
        return self.arrangment.index('E')
    def __str__(self):
        return self.arrangment
    def get_g_value(self):
        return self.g_value
    def set_g_value(self, new_g):
        self.g_value = new_g
    def __hash__(self):
        #return hash((self.arrangment, self.g_value, self.f_value))
        return hash((self.arrangment))
    def __str__(self):
        return "Arrangment:",self.arrangment,"f: ",self.f_value,", g: ",self.g_value,", h: ",self.h_value

# Helper Methods
# Goal Check
def is_goal(arrangment):
        global goal
        return arrangment == goal
def switch(arr, i1, i2):
    return arr[i2], arr[i1]

def move_allowed(arrangment,  empty_char_location, direction, steps):  # direction: left, right. Steps: 1,2,3,4 (i.e. 0, 1, 2, 3)
    if direction == 'left':
        return empty_char_location - steps >= 0
    else:
        return empty_char_location + steps < len(arrangment)

def huristic_helper(arrangment, h):
    huristic = 0
    if h == 0:
        pass    # Keep its value to 0
    elif h == 1:
        
        huristic = huristic_miss_placed_tiles(arrangment)
    elif h == 2:
        huristic = huristic_manhattan_distance(arrangment) # Do manhattan_distance
    return huristic 
# Huristic Method (Based on miss placed tiles)
def huristic_miss_placed_tiles(arrangment):
        # e_add = 0
        # if arrangment.index('E') != len(arrangment) -1:
        #     e_add = 1   
        arrangment = arrangment.replace('E','')
        return  len([1 for i in range((len(arrangment )/2 )) if arrangment[i] == 'B']) * 2 #+ e_add     # Since if 2 B's on left means that 2 wrong A's on the right since they are both of size n
def huristic_manhattan_distance(arrangment):
        arrangment = arrangment.replace('E','')
        total_size = len(arrangment)
        half_size = total_size/2
        half_arr = arrangment[:total_size/2]
        tmp_arr = []
        man_dis = 0
        for i in range(half_size):
            if arrangment[i] == 'B':
                for j in range(half_size):
                    if arrangment[half_size+j] == 'A' and half_size+j not in tmp_arr:
                        tmp_arr.append(half_size+j)
                        man_dis = man_dis + (half_size+j - i)
                        break

        return man_dis *2
# End of Helper Methods
def successors(cur_state, h):
        global total_node_generated
        global children_avl
        children = []
        global n_value
        global last_hash 
        global children_dict

        empty_char_location = cur_state.empty_space_location()
        # -------------------------------------
         # # Check the right
        step = 1
        while(move_allowed(cur_state.arrangment, empty_char_location, 'right',step) and step <= 4):
            tmp_arr = list(cur_state.arrangment)
            tmp_arr[empty_char_location], tmp_arr[empty_char_location + step] = switch(tmp_arr, empty_char_location, empty_char_location + step )
            arrangment = ''.join(tmp_arr)
            cost =  0
            if step == 1 or step == 2:
                cost = 1
            else:
                cost = step -1
            cost = cost + cur_state.get_g_value()
            huristic = huristic_helper(arrangment, h)
            new_state = State(arrangment, cost,  huristic,  cost +  huristic, cur_state)
            if dict_key_found(children_dict,new_state.__hash__()) == None:
                children.append(new_state)
                children_dict[new_state.__hash__()] = new_state
            # if children_avl.find(new_state.__hash__()) == None:
            #     children.append(new_state)
            #     children_avl.insert(new_state.__hash__(), new_state)
                    
            step = step +1
        # Check left    
        step = 1
        while(move_allowed(cur_state.arrangment, empty_char_location, 'left',step) and step <= 4):
            tmp_arr = list(cur_state.arrangment)
            tmp_arr[empty_char_location], tmp_arr[empty_char_location - step] = switch(tmp_arr, empty_char_location, empty_char_location - step )
            arrangment = ''.join(tmp_arr)
            cost =  0
            if step == 1 or step == 2:
                cost = 1
            else:
                cost = step -1
            cost = cost + cur_state.get_g_value()
            huristic = huristic_helper(arrangment, h)
            new_state = State(arrangment, cost, huristic,  cost +  huristic, cur_state)
            if dict_key_found(children_dict,new_state.__hash__()) == None:
                children.append(new_state)
                children_dict[new_state.__hash__()] = new_state

            step = step +1
        total_node_generated = total_node_generated + len(children)
        return children


def re_order_states(arr_1):
    # 1- find the lowest f value (might be 1,2 or more)
    return sorted(arr_1, key = lambda x: (x.f_value, x.h_value))

def dict_key_found(dict_arr, key):
    try:
        return dict_arr[key]
    except:
        return None

def dijkstra_a_star(initial_state, h):
    global frontier_avl
    global frontier_dict


    #frontier_avl = None
    #frontier_avl = atree.AVLTree()


    if is_goal(initial_state):
        return initial_state

   # explored = atree.AVLTree() # AVL Tree
    explored_dict = {}
    
    frontier = []

    hq.heappush(frontier,(initial_state.f_value, initial_state))
    #frontier_avl.insert(initial_state.__hash__(), initial_state)
    frontier_dict[initial_state.__hash__()] = initial_state
    while frontier != []:
    #while frontier_avl.is_Empty() == False:
   # while frontier_dict != {}:
        
        state = hq.heappop(frontier)[1]
       
        #print state.__hash__()
        #print frontier_dict
        frontier_dict.pop(state.__hash__())
       # print dict(state_dict)
        #state = frontier_avl.pop_min_value_key().data
        #state = frontier_dict.pop
        #frontier_avl.remove(state.__hash__())

        if is_goal(state.arrangment):
            return state

        #explored.insert(state.__hash__(), state)
        explored_dict[state.__hash__()] = state
        children = successors(state, h)
        #children = re_order_states(children)
        for item in children:
            # 1 --------------------------------
            # Helper place holders so we won't have to do the search more than once
           # inExplored = explored.find(item.__hash__()) 
           # inFrontier = frontier_avl.find(item.__hash__())

            inExplored = dict_key_found(explored_dict, item.__hash__())
            inFrontier = dict_key_found(frontier_dict, item.__hash__())

            
            # 2 --------------------------------
            # Calculate new_g_value
            new_g_value =  state.get_g_value() + item.get_g_value()

            # 3 --------------------------------
            # case 1
            if inExplored == None and inFrontier == None:

                hq.heappush(frontier,(item.f_value,item))
                frontier_dict[item.__hash__()] = item
               # frontier_avl.insert(item.__hash__(), item)

            # case 2
            elif inFrontier != None:
                # Edge Relaxation
                # Ex. frontier = [True, (3, <__main__.Node instance at 0x7f6045676d40>)]
                if new_g_value < inFrontier.get_g_value():
                    inFrontier.set_g_value(new_g_value)
                    hq.heappush(frontier,(inFrontier.f_value,inFrontier))
                    frontier_dict[item.__hash__()] = item

                # if new_g_value < inFrontier.date.get_g_value():
                #     inFrontier.data.set_g_value(new_g_value)

                #     hq.heappush(frontier,(inFrontier.data.f_value,inFrontier.data))
                #     frontier_dict[initial_state.__hash__()] = initial_state
                #    #frontier_avl.insert(item.__hash__(), item)


    return None

def random_state_generate(n):
    a_num = 0
    total = n *2
    i = 0
    arr_1 = []
    arr_1.append([random.randint(0,total),'E'])
    while a_num < total /2:
        if random.random() < 0.5:
            index = i%total
            if [True for item in arr_1 if item[0] == index] == []:
                arr_1.append([index,'A'])
                a_num = a_num +1
        i = i+1  
    [arr_1.append([i,'B']) for i in range(total+1) if [ True for item in arr_1 if item[0] == i] == []]
    arr_1 = sorted(arr_1, key = lambda x:x[0])
    return  "".join([item[1] for item in arr_1 ])

def main(n, h):
    global goal
    global n_value

    n_value = n
    goal = 'A'*n_value+'B'*n_value+'E'

    print "n value: ", n_value
    print "goal ",goal


    random_states_arr = []
    # 1- Generate worst case
    worst_configuration = 'E'+'B'*n_value+'A'*n_value
    random_states_arr.append(worst_configuration)
    # 2- Generate 10 random unique generated element
    
    found_ten_unique_states = False
    i = 0
    while found_ten_unique_states != True:
        state = random_state_generate(n_value)
        if state not in random_states_arr and state != worst_configuration and state != goal :
            random_states_arr.append(state)
            if i > 9:
                found_ten_unique_states = True
            i = i+1
    # 3- use a A* then Dijkstra (h, h0) for each state (Total 11 with the worst case)
    print "Random Generated Configurations"
    print random_states_arr
    start_time = time.time()
    do_operations(random_states_arr[2], h)
   # do_operations('BABBABBAAAABBBAAE', h)
    # for item in random_states_arr:
    #     print '='* 40
    #     print "State to Test: ",item
    #     print "#"*30+" Dijkstra... h0  \t  "+"#"*30
    #     do_operations(item, 0)
    #     print "#"*30+" A*... h1  \t  "+"#"*30
    #     do_operations(item, h)
    end_time = (time.time() - start_time)
    print "~0~"*10
    print "Total Time:"
    print("--- %.5f seconds ---" % end_time)
     



def do_operations(init_arrangment, h = 1):
    """ h0 = dijkstra, h1 = A*, h2 = manhattan distance """
    global total_node_generated
    global children_avl 
    global frontier_avl
    global frontier_dict
    global children_dict

    #children_avl = None # Free the memory
    #children_avl = atree.AVLTree()

    children_dict = None # Free the memory
    children_dict = {}

    #frontier_avl = None # Free the memory
    #frontier_avl = atree.AVLTree()


    frontier_dict = None # Free the memory
    frontier_dict = {}

    huristic = huristic_helper(init_arrangment, h)
    total_node_generated = 0    

    start_time = time.time()
    result = dijkstra_a_star(State(init_arrangment,0,huristic,  0 + huristic, None), h) 
    end_time = (time.time() - start_time)

    if result != None:
        arr_1 = []
        cost = 0
        while result != None:
            arr_1.append(result.arrangment)
            cost =  cost + result.get_g_value()
            result = result.parent

        print "#"*30+" Misplaced 1D tiles "+"#"*30
        print '\n'
        print "Path: ",arr_1
        print "Cost: ",cost  
        print "Total Nodes: ",total_node_generated
        print "Effective Branching Factor: ", math.pow(float(total_node_generated), 1.0/float(len(arr_1) -1 )) # Formula: b=x^1/d, where x: total number of nodes searched, d: depth (-1: to remove the root node from the count since we are looking at the depth)
        print("--- %.5f seconds ---" % end_time)
        print '\n'

if __name__ == '__main__':
    main(4,1)