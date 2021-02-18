# Maze class
# Author: Kai Zhu

class Maze:
    def __init__(self, width = 2, height = 2):
        # maze constructor

        self.width = width
        self.height = height
        self.nodes = []
        self.start = None
        self.end = None

        for i in range(height):
            self.nodes.append([])
            for j in range(width):
                node = [i*width + j, False, False, False, False]
                if j > 0:
                    node[4] = True
                    self.nodes[i][j-1][2] = True
                if i > 0:
                    node[1] = True
                    self.nodes[i-1][j][3] = True
                self.nodes[i].append(node)
        self.root = self.nodes[0][0]
        #print(self.nodes)

    def getAdjNode(self, x, y, dir):
        # returns the coordinates of the adjacent node in the direction (dir)

        if dir == 1 and y > 0:
            return (x, y-1)
        elif dir == 2 and x < self.width-1:
            return (x+1, y)
        elif dir == 3 and y < self.height-1:
            return (x, y+1)
        elif dir == 4 and x > 0:
            return (x-1, y)
        else:
            return None

    def getIndex(self, x, y):
        # returns the index of a node given the coordinates

        return y * self.width + x

    def getXY(self, index):
        # returns the coords of a node given the index

        y = index // self.width
        x = index - y * self.width
        return (x, y)


if __name__ == "__main__":
    testMaze = Maze(3,3)
    print(testMaze.nodes)