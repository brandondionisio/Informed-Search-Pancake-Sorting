import heapq
import copy
import timeit
import random
           
def main():
    # Randomized 10-long pancake stack
    stack = list(range(1, 10))
    random.shuffle(stack)
    stack.append(10)

    # prompt the user for input
    print("Enter pancake stack with sizes consecutively (i.g., 3124).")
    print("Enter \"r\" for a randomized 10-pancake stack.")
    user = input()

    # input query loop
    valid_input = False
    # accept input only if it is a valid stack or "d" (default stack)
    while not valid_input:
        if not user.isdigit() and user != "r":
            print("Invalid input. Please try again: ")
            user = input()
        elif user != "r" and not valid_stack([int(digit) for digit in str(int(user))]):
            user = input()
        else:
            valid_input = True

    # convert input into an array
    if user.isdigit():
        user = int(user)
        stack = [int(digit) for digit in str(user)]

    # make astar object
    AStar = astar(stack)

    # start the timer
    timer_start = timeit.default_timer()

    print("Running search...")
    # run the search algorithm
    AStar.run()

    # stop the timer
    timer_stop = timeit.default_timer()

    # print the solution with the time taken
    AStar.print_result()
    print("A* search time:", round(timer_stop - timer_start, 2), "seconds")

class astar():
    def __init__(self, initial_state):

        # length of the pancake array
        self.length = len(initial_state)

        # the step number of which we add the node
        self.steps = 0
        
        # array of seen states
        self.seen = []

        # The forward cost function is modeled with a priority queue
        self.forward = PriorityQueue()

        # create the initial pancake state node
        self.root = Stack_State(initial_state, None, self.steps)

        # put the node on the priority queue
        self.forward.put(self.root)

        # increase the number of steps / flips
        self.steps += 1

    # runs the A* search
    def run(self):
        while True:
            # if the priority queue is empty, then there is no solution
            if self.forward.empty():
                self.solution = False
                return
            
            # gets the highest priority flip
            curr = self.forward.get()

            # adds the flip to list of seen flips
            self.seen.append(curr.state)

            # If the heuristic function returns 0, then we are at the goal
            if curr.heuristic() == 0:
                self.solution = curr
                return
            
            # adds all of the possible pancake stacks made from flipping
            # pancakes with the current stack to the priority queue.
            for i in range(2, self.length):
                # creates a copy of the current stack with a new reference
                temp = copy.deepcopy(curr)
                temp.flip(i)
                temp.prev = curr
                temp.steps = self.steps
                
                # adds the temp states to the priority queue if not in there
                # already and if not already seen
                if (not self.forward.contains_state(temp.state)) and (temp.state not in self.seen):
                    self.forward.put(temp)
                
                # if the priority queue already has the state, will try to
                # replace the state if it has a better total cost
                elif self.forward.contains_state(temp.state):
                    self.forward.better_cost(temp)
                
                self.steps += 1

    # prints the end result of the A* search
    def print_result(self):
        if self.solution == False:
            print("Problem has no solution")
        else:
            path = []
            curr = self.solution
            while curr != None:
                path.append(curr)
                curr = curr.prev
            
            # if the length of path is 1, then the pancakes were already sorted
            if len(path) == 1:
                print("Pancake stack is already sorted!")
                return
            
            path.reverse()
            
            print("The pancake stack", path[0].state, "is solved by the following flip sequence:")
            for step in range(1, len(path) - 1):
                print("F", path[step].depth, ", ", end = "", sep = "")
            print("F", path[len(path) - 1].depth, sep = "")

# Verifies that the stack is valid. Checks that the end number is largest,
# (plate on the bottom), and that the stack contains only consecutive integers.
def valid_stack(stack):
    for i in stack:
        if i > stack[len(stack) - 1]:
            print("Largest plate needs to be on the bottom. Please try again.")
            return False
    if sorted(stack) != list(range(min(stack), max(stack) + 1)):
        print("Pancake stack should consist only of consecutive numbers. Please try again.")
        return False
    return True

# Stack_State class
# represents each stack of pancakes during the search
#
# state: an array of integers representing the pancake stack sizes
# prev: the previous state of pancakes before flipping to current
# steps: number of flips it took to reach the current state
class Stack_State:
    def __init__(self, state, prev, steps):
        self.state = state
        self.prev = prev
        self.backward_cost = 0
        self.steps = steps
    
    # comparator for the heap
    def __lt__(self, other):
        if self.get_total() != other.get_total():
            return self.get_total() < other.get_total()
        else:
            return self.steps < other.steps

    # gets the total cost of the forward cost + backward cost of the
    # curr node
    def get_total(self):
        return self.heuristic() + self.backward_cost

    # flips the stack of pancakes with the given depth
    def flip(self, depth):
        self.depth = depth

        # We swap the first and the last pancake in the range of the flip
        # depth. In the case where there is an odd number of pancakes, the
        # middle pancake would just be swapped with itself
        for i in range(int(depth / 2)):
            temp = self.state[i]
            self.state[i] = self.state[depth - i - 1]
            self.state[depth - i - 1] = temp
        
        # The backward cost is how many pancakes have been flipped (i.e.
        # flip_depth)
        self.backward_cost += depth
        
    # heuristic function which is the number of stack positions for
    # which the pancake at that position is not of adjacent size to
    # the pancake below
    # returns the corresponding heuristic nteger for the current stack
    def heuristic(self):
        hgap = 0
        for i in range(1, len(self.state)):
            if abs(self.state[i] - self.state[i-1]) != 1:
                hgap += 1
        return hgap


# Priority Queue
# implementation of a priority queue for the A* search algorithm
# 
class PriorityQueue():
    # default constructor; initializes the heap, represented by a list
    def __init__(self):
        self.heap = []

    # returns whether priority queue is empty
    def empty(self):
        return len(self.heap) == 0
    
    # puts the given nodes on the priority queue
    def put(self, node):
        heapq.heappush(self.heap, node)
    
    # gets the node with the least cost
    # pops the node from the heap
    def get(self):
        top = heapq.heappop(self.heap)
        return top
    
    # checks to see if the given state is already in the priority queue
    # returns true if so; false if not
    # state argument is an array of pancake stack
    def contains_state(self, state):
        for node in self.heap:
            if node.state == state:
                return True
        return False
    
    # if a node's state is already in the priority queue, will try
    # to see if it has a better total cost, and if it does, will replace
    # it in the priority queue. 
    def better_cost(self, new_node):
        for node in self.heap:
            if node.state == new_node.state:
                if node.get_total() > new_node.get_total():
                    self.heap[self.heap.index(node)] = new_node

if __name__ == '__main__':
    main()