import numpy as np
import time
import random

def printa_lista(lista,who):
    print "\n\t\t#####\t",who,"\t####"
    
    for l in lista:
        #printa_node(l)
        print l.get_node()
    

def printa_node(n):
    node = n.get_node()
    print "Coord: ",node[0],"  G: ",node[1],"  H: ",node[2],"  Cost: ",node[3],"  Wall: ",node[4]



class Node:
    def __init__(self,Cord,Obj):
        self.Cord = Cord 
        a = self.Cord[0] - Obj[0]
        b = self.Cord[1] - Obj[1]
        c = self.Cord[2] - Obj[2]
        self.G = random.randint(0,9)
        self.H = int(round(np.sqrt( np.square(a) + np.square(b) + np.square(c) )))
        self.Cost = self.G + self.H
        self.wall = False 
 
    def get_cost(self):
        return self.Cost
    def set_wall(self):
        self.wall = True
    def get_wall(self):
        return self.wall
    def get_node(self):
        return (self.Cord,self.G,self.H,self.Cost,self.wall)

class Cube:
    def __init__(self,dim,obstacles):
        self.End = (random.randint(0,dim-1),random.randint(0,dim-1),random.randint(0,dim-1))
        self.Start = (random.randint(0,dim -1 ),random.randint(0,dim -1),random.randint(0,dim-1))
        self.Cube = []
        print "foi ",self.End
        for x in range(dim):
            for y in range(dim):
                for z in range(dim):
                    node = Node((x,y,z),self.End)
                    if random.random() < obstacles :
                        if (x,y,z) != self.Start and (x,y,z) != self.End:
                            node.set_wall()
                    self.Cube.append(node) 

        self.Cube = np.array(self.Cube)               
        self.Cube = self.Cube.reshape(dim,dim,dim)
    def get_cube(self):
        return self.Cube
    def get_start(self):
        return self.Start
    def get_end(self):
        return self.End
    def get_neighborhood(self,cord):

        neighbor = []
        for a in (-1,0,1):
            x = a + cord[0]
            for b in (-1,0,1):
                y = b + cord[1]
                for c in (-1,0,1):
                    z = c + cord[2]
                    if (x==y and y==z):
                        pass
                    else:
                        if((x >= 0 and x < len(self.Cube)) and 
                           (y >= 0 and y < len(self.Cube)) and
                           ((z >= 0) and z < len(self.Cube))):
                             neighbor.append(self.Cube[x][y][z])
        return neighbor
class A_Estrela:
    def __init__(self):
        self.open = []
        self.closed = []
    def solve(self,dim,obstacles):
        c = Cube(dim,obstacles)
        cube = c.get_cube()
        start = c.get_start()
        start = cube[start[0]][start[1]][start[2]]
        self.open.append(start)


        end = c.get_end()
        end = cube[end[0]][end[1]][end[2]]
        print "###########SELF OPEN###",self.open

        print "Start === ",start.get_node()  
        print "END  === ",end.get_node()    
        current = start 
        while(1):
            if not self.open: 
                print "\n\n\t\tNO SOLUTION\n\n"
                break
            current = self.open.pop(0)
            print "\nCurrent===",current.get_node()
            if current == end:
                print "\n\nEXIT DO WHILE"
                break
            if current in self.closed:
                index = self.closed.index(current)
                print "ja no closed", current.get_node, index
            # move o primeiro da lista de abertos pra lista de fechados
            self.closed.append(current)
            #printa_lista(self.open,"Open Inicio While")

            neighbors = c.get_neighborhood(current.get_node()[0])
            #print "\n\t====Vizinhanca===="
            for n in neighbors:
                #print n.get_node()
                if n.get_wall() == False:
                    #print "Open Path at", n.get_node()
                    if n not in self.closed:
                        self.open.append(n) 
            #remove repetitions
            self.open = list(set(self.open))
            # sort by cost
            sorted_open = sorted(self.open, key = Node.get_cost) 
            #print "\n\t====End While===="

            self.open = sorted_open
            printa_lista(self.open,"Open")
            self.closed = list(set(self.closed))
            printa_lista(self.closed,"Closed")
            #time.sleep(1)
        
        print "Start === ",start.get_node()  
        print "END  === ",end.get_node()    

if  __name__ == "__main__":
    dim = 10
    obstacles = 0.6
    IA = A_Estrela()
    IA.solve(dim,obstacles)

