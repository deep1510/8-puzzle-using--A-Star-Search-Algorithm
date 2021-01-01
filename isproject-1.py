''' node configration with its data 
    ( matrix "grid puzzel" , g(n) = 0  , f(n)= 0 , parent position (x,y) , Parent Matrix )'''
class Node: 
    
    def __init__(self,mat,gn,fn,parent_x,parent_y,matParent):
         self.mat = mat
         self.gn = gn 
         self.fn = fn 
         self.parent_x =parent_x
         self.parent_y = parent_y
         self.matParent = matParent
    ''' This function is responsible for generating the successors of the current node'''
    def successor(self):
        successors=[]
        x,y = self.blank_tile(self.mat,0) #get the loction of the blank tile (x,y) ,'0' means blank of current node

        new_loc= [[x-1,y],[x+1,y],[x,y-1],[x,y+1]] #generate 4 new locations for the blank tiles and stored then in new_loc[] array
        for i in new_loc:
           new_succsessor= self.swapping(self.mat,i[0],i[1],x,y)
           if new_succsessor != 0:
               new_node = Node(new_succsessor,self.gn+1,0,x,y,self.mat)
               successors.append(new_node)
        return successors
        

    '''  This function is responsible of getting a copy of current node to swapping it with new blank tile location'''
    def swapping(self,current_mat,x1,y1,x,y):
        child_m =[]
        if x1 >= 0 and x1 < len(self.mat) and y1 >= 0 and y1 < len(self.mat):
            # copy the current matrix 
            for i in current_mat:
                t =[]
                for j in i:
                    t.append(j)
                child_m.append(t)
            # end of copying process
            # swaping process   
            temp= child_m[x1][y1]
            child_m[x1][y1] =child_m[x][y]
            child_m[x][y] = temp
            return child_m
        else:
            return 0
    ''' This function is responsible of finding the blank tile location'''
    def blank_tile(self,m,a):
        for i in range(0,len(self.mat)):
            for j in range(0,len(self.mat)):
                if self.mat[i][j] == a:
                    return i,j
                    
''' Stores the Search Configuration (List of expanded nodes, List of generated nodes, Number of nodes generated)'''
class Grid:
    explored_list = []
    frontier = []
    no_of_nodes_generated = 0

    ''' This function is responisible for taking the input from the user '''
    def read_input(self):
        print("(Use 0 for blank tile, Insert spaces after each number & press enter after each row)")
        matrix = [[int(y) for y in input().strip().split(" ")] for x in range(3)] # stores the data in a 2d matrix
        return matrix

    ''' This function is responsible of checking whether or not the parent node is generated again and prevent that if it happens '''
    def matchWithParent(self,current_mat,parent_mat):
        count=0
        for x in range(3):
            for y in range(3):
                if current_mat[x][y] != parent_mat[x][y]:
                    count = count + 1
        if count == 0:
            return False
        else:
            return True
        
    ''' This function is responsible for computing the f(n) value '''
    def evaluation_fn(self,current,goal,heuristic):

        if heuristic == 1:
            return self.manhattan_distance_heuristic(current.mat,goal) + current.gn 
        else:
            return self.misplaced_tiles_heuristic(current.mat,goal) + current.gn

    ''' This function is responsible for computing h(n) based on misplaced tiles heuristic '''    
    def misplaced_tiles_heuristic(self,current,goal):

        count=0
        for x in range(3):
            for y in range(3):
                if current[x][y] == 0: continue

                if current[x][y] != goal[x][y]: #count the misplaced tiles
                    count = count + 1

        return count

    ''' This function is responsible for computing h(n) based on manhattan distance heuristic '''
    def manhattan_distance_heuristic(self,current,goal):

        current_tile_positions = self.find_tile_positions(current)
        goal_tile_positions = self.find_tile_positions(goal)

        # calculates the right angle distance from the goal position for each tile
        sum =0
        for x in range(8):
            x = x + 1
            sum = sum + abs(goal_tile_positions[x][0] - current_tile_positions[x][0]) + abs(goal_tile_positions[x][1] - current_tile_positions[x][1])

        return sum
    
    ''' This function is responsible for finding the location of tiles'''
    def find_tile_positions(self,state):

        tile_positions ={}
        for i in range(3):
            for j in range(3):
                tile_positions.update({state[i][j]:[i,j]})
        
        return tile_positions

    ''' This function is responsible for searching the solution '''
    def search(self):
        print("Enter the start state")
        start_state = self.read_input()
        print("Enter the goal state")
        goal_state = self.read_input()

        print("Select the type of Heuristic. Enter 1 for Manhattan-Distance-Heuristic 2 for Misplaced-Tiles-Heuristic")
        heuristic = int(input())

        if heuristic not in [1, 2]:
            print("Invalid Input")
            return

        print("Processing....")

        start_state = Node(start_state,0,0,-1,-1,start_state)
        start_state.fn = self.evaluation_fn(start_state,goal_state, heuristic)
        self.frontier.append(start_state)
        while len(self.frontier)!=0:
            current = self.frontier[0]

            # this condition to check if the goal is found or not
            if current.mat == goal_state:
                print("Goal found")
                self.printSolutionPath(current,self.explored_list)
                print("No of Nodes Generated", self.no_of_nodes_generated +len(self.frontier))
                print("No of Nodes Expanded", len(self.explored_list))
                break
                    
            # this condition to check if the problem is not solvable the search will stop at genertaed nodes greater than 3000
            if self.no_of_nodes_generated+len(self.frontier) > 3000 :
                print ("Number of nodes generated exceeded 3000. The puzzle doesnt have a solution")
                break
            # if the goal is not found and the number of nodes generated not exceding the limit (solvable)
            # the following code will generate the children and remove the current node from the frontier
            self.no_of_nodes_generated +=1
            for child in current.successor():
                if self.matchWithParent(child.mat,current.matParent):
                    child.fn = self.evaluation_fn(child,goal_state,heuristic)
                    self.frontier.append(child)
                else:
                    pass
            self.explored_list.append(current)
            self.frontier.remove(current)
            # reordring the nodes based on the f(n) values.
            self.frontier.sort(key=lambda  x:x.fn,reverse=False)
        if(len(self.frontier) == 0): print("No Solution")

    ''' This function is responsible for printing the path ''' 
    def printSolutionPath(self,node,explored_list):
        goal_node = node
        path = []
        # Backtracks till the initial state is found
        while node.parent_x != -1 and node.parent_y != -1:
            for item in explored_list:
                tile_positions = self.find_tile_positions(item.mat)
                # finds the parent node from explored list based on x,y position of blank tile and the depth 
                if tile_positions[0] == [node.parent_x, node.parent_y] and item.gn == (node.gn)-1: 
                    path.append(item)
                    break
            node = item

        path.reverse()
        path.append(goal_node)
        for path_node in path:
            print('\n'.join([' '.join([str(cell) for cell in row]) for row in path_node.mat]))
            print("--------")
        return


if __name__ == "__main__":

    grid = Grid()
    grid.search()