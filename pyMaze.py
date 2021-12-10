# Generates a customizable random maze and solves it with BFS
# Click on the GUI edges to customize node connection
# Author: Kai Zhu
VERSION = "1.1"

from time import time
from libs.maze import Maze
from tkinter import *
from tkinter import messagebox
import random

GRAY = "#505050"
DARKGRAY = "#303030"
NODE_RAD = 5    # radii of the start, end nodes
LINESPACE = 2   # gap between line and grid dots
GRID_RAD = 2    # grid dot radius
TOOLRG = 2500   # threshold for large maze

master = Tk()
master.configure(bg=DARKGRAY)
master.title("Python Maze Solver V" + VERSION)
master.resizable(0,0)

canvas_w = 600
canvas_h = 600
maze_w = 20
maze_h = 20
grid_width = canvas_w / maze_w
grid_height = canvas_h / maze_h
mz = Maze(maze_w, maze_h)

showsearch = BooleanVar()

def newMaze(*arg):
    global maze_w, maze_h, grid_width, grid_height, mz

    mz.start = None     # reset maze start/end
    mz.end = None
    c.delete("start")
    c.delete("end")
    
    swidth, sheight = e_width.get(), e_height.get()

    if not swidth.isnumeric() or int(swidth) < 2:
        e_width.delete(0,END)
        e_width.insert(0,str(maze_w))
        swidth = maze_w
    if not sheight.isnumeric() or int(sheight) < 2:
        e_height.delete(0,END)
        e_height.insert(0,str(maze_h))
        sheight = maze_h
    if int(swidth) * int(sheight) > TOOLRG:
        if messagebox.askquestion("Caution", "The entered maze dimensions might be too large, continue regardless?") == "no":
            return

    maze_w = int(swidth)
    maze_h = int(sheight)
    grid_width = canvas_w / maze_w
    grid_height = canvas_h / maze_h    
    mz = Maze(maze_w, maze_h)
    drawGrid()
    drawMaze()
    print(mz.nodes)

def canvas_click(event):
    x = int(event.x // grid_width)       # get grid coords
    y = int(event.y // grid_height)
    
    local_x = event.x - x * grid_width      # get local coords inside grid
    local_y = event.y - y * grid_height
    dir = -2                    # initialize search direction

    if local_y < grid_height * 0.2:
        dir = 0 # top
    elif local_y > grid_height * 0.8:
        dir = 2 # bottom
    elif local_x < grid_width * 0.2:
        dir = 1 # left
    elif local_x > grid_width * 0.8:
        dir = 3 # right
    else:
        dir = -1 # middle
        statusbar.configure(text="")
        if (x, y) == mz.start:
            c.delete("start")  # resetting start
            mz.start = None
        elif (x, y) == mz.end:
            c.delete("end")  # resetting start
            mz.end = None
        elif not mz.start:      # set start point 
            mz.start = (x, y)
            c.create_oval((x+0.5)*grid_width-NODE_RAD, (y+0.5)*grid_height- NODE_RAD, (x+0.5)*grid_width+NODE_RAD, (y+0.5)*grid_height+NODE_RAD, fill="yellow", outline="yellow", tag = "start")  # resetting start
        else:                   # set or move end point
            if mz.end:
                c.delete("end")  # resetting start
            mz.end = (x, y)
            c.create_oval((x+0.5)*grid_width-NODE_RAD, (y+0.5)*grid_height-NODE_RAD, (x+0.5)*grid_width+NODE_RAD, (y+0.5)*grid_height+NODE_RAD, fill="cyan", outline="green", tag = "end")  # resetting start


    if dir > -1:
        adj = mz.getAdjNode(x,y,dir)
        if adj:
            connected = not mz.nodes[y][x][dir]
            mz.nodes[y][x][dir] = connected    # flip accessibility
            mz.nodes[adj[1]][adj[0]][(dir+2)%4] = connected # flip recriprocal dir in connected square

            drawWall(x,y,dir,connected)

def drawWall(x, y, dir, unblocked):
    # draws maze walls

    x0,y0,x1,y1 = 0,0,0,0
    if dir == 0:        # up
        x0 = x * grid_width + LINESPACE
        y0 = y * grid_height
        x1 = (x+1) * grid_width - LINESPACE
        y1 = y * grid_height
    elif dir == 3:      # right
        x0 = (x+1) * grid_width
        y0 = y * grid_height + LINESPACE
        x1 = (x+1) * grid_width
        y1 = (y+1) * grid_height - LINESPACE
    elif dir == 2:      # bottom
        x0 = x * grid_width + LINESPACE
        y0 = (y+1) * grid_height
        x1 = (x+1) * grid_width - LINESPACE
        y1 = (y+1) * grid_height
    else:               # left
        x0 = x * grid_width
        y0 = y * grid_height + LINESPACE
        x1 = x * grid_width
        y1 = (y+1) * grid_height - LINESPACE

    adj = mz.getAdjNode(x,y,dir)
    s1 = ",".join([str(x), str(y), str(dir)])
    s2 = ",".join([str(adj[0]), str(adj[1]), str((dir+2)%4)])

    if unblocked:
        c.delete(s1)
        c.delete(s2)
    else:
        c.create_line(x0,y0,x1,y1,fill="white", width = 1, tag = (s1,"wall"))

def randomize(event):
    # creates random maze
    path = []
    #newMaze()

    timer = time()
    if mz.start and mz.end:
        path = randPath()
        print(path)


    for y in range(maze_h):
        for x in range(maze_w):
            dirs = [0,1,2,3]
            random.shuffle(dirs)
            for dir in range(4):
                adj = mz.getAdjNode(x,y,dir)
                if adj:
                    if path == []:                                   # no destination, dont worry about pathing
                        ran = (random.random() > 0.5)                # all these params are fine tuning for making a nice looking maze
                    else:
                        if adj not in path or (x, y) not in path:
                            #ran = (random.random() > 0.5)     
                            ran = (random.random() > 0.3 + sum(mz.nodes[adj[1]][adj[0]]) * 0.15)       # tune the shape of the maze walls
                        else:
                            ran = True                                  # do not obstruct guaranteed path
                    mz.nodes[y][x][dir] = ran
                    mz.nodes[adj[1]][adj[0]][(dir+2)%4] = ran       # change complement link too
                    #drawWall(x,y,dir,ran)
    drawMaze()
    statusbar.configure(text=f"new maze generated in{(time()-timer):10.4f} s")
    #print(mz.nodes)

def drawGrid():
    # draw the grid (corner circles)
    c.delete("grid")
    for x in range(maze_w + 1):
        for y in range(maze_h + 1 ): 
            c.create_oval(grid_width*x-GRID_RAD, grid_height*y-GRID_RAD,grid_width*x+GRID_RAD, grid_height*y+GRID_RAD, fill="green", outline="green", tag = "grid")

def drawMaze():
    # refresh maze visuals

    c.delete("wall")
    c.delete("path")
    for y in range(maze_h):
        for x in range(maze_w):
            for dir in range(0,4):
                adj = mz.getAdjNode(x,y,dir)  
                if adj:  
                    drawWall(x,y,dir,mz.nodes[y][x][dir])

def drawPath(path, colour):
    # solution path

    #c.delete("path")
    x0, y0 = path[0]
    x0 = (x0 + 0.5) * grid_width
    y0 = (y0 + 0.5) * grid_height

    for i in range(1, len(path)):
        x1, y1 = path[i]
        x1 = (x1 + 0.5) * grid_width
        y1 = (y1 + 0.5) * grid_height
        c.create_line(x0,y0,x1,y1,fill=colour, width = 2, tag = "path")
        x0, y0 = x1, y1

def randPath():
    # using DFS to generate a random path from start to dest

    if not mz.start or not mz.end:
        statusbar.configure(text="Missing start or end points. Click on maze grid to set.")
    else:
        #drawMaze()
        stack = [mz.start]
        predecessors = {mz.start: None}       # remember visited node indices

        while stack:
            x, y = stack.pop(-1)

            if (x, y) == mz.end:
                #print("FOUND PATH!!!!")
                path = [(x, y)]
                pred = predecessors[(x, y)]
                while pred:
                    path.append(pred)
                    pred = predecessors[path[-1]]
                return path[::-1]
            else:
                dirs = [0,1,2,3]
                random.shuffle(dirs)
                for dir in dirs:
                    adj = mz.getAdjNode(x,y,dir)     # dir = i+1
                    if not adj: continue
                    if adj not in predecessors:
                        stack.append(adj)
                        predecessors[adj] = (x, y)
        statusbar.configure(text="NO VALID PATH FOUND!")

def solveBFS(maze):
    queue = [maze.start]
    predecessors = {maze.start: None}       # remember visited node indices

    while queue:
        x, y = queue.pop(0)

        if (x, y) == maze.end:
            path = [(x, y)]
            pred = predecessors[(x, y)]
            while pred:
                path.append(pred)
                pred = predecessors[path[-1]]
            return path[::-1]
        else:
            for i, unblocked in enumerate(maze.nodes[y][x]):
                if unblocked:
                    adj = maze.getAdjNode(x,y,i)     # dir = i+1
                    if adj not in predecessors:
                        queue.append(adj)
                        predecessors[adj] = (x, y)

def solve(event):
    timer = time()
    c.delete("path")
    # solve the maze via BFS and pass solution to drawPath

    if not mz.start or not mz.end:
        statusbar.configure(text="Missing start or end points. Click on maze grid to set.")
    else:
        drawMaze()
        path = solveBFS(mz)
        if path: 
            drawPath(path, "yellow")
            statusbar.configure(text=f"maze solved in{(time()-timer):10.4f} s")
        else:
            statusbar.configure(text="NO VALID PATH FOUND!")


def endProg(*arg):
    # exit program
    master.destroy()


# GUI creation

c = Canvas(master, width = canvas_w, height = canvas_h, bg="black", highlightthickness=0)
c.grid(row=1, columnspan=10)

l1 = Label(master,text="Width: ",bg = DARKGRAY, fg="white")
l1.grid(row=2, column=0, sticky = E)

e_width = Entry(master, bg=DARKGRAY, fg="yellow", width = 3, justify="right", relief = FLAT)
e_width.grid(row=2, column=1, sticky = W)
e_width.insert(0, str(maze_w))

l2 = Label(master,text="Height: ",bg = DARKGRAY, fg="white")
l2.grid(row=2,column=2, sticky = E)

e_height = Entry(master, bg=DARKGRAY, fg="yellow", width = 3, justify="right", relief = FLAT)
e_height.grid(row=2, column=3, sticky = W)
e_height.insert(0, str(maze_h))

c_pattern = Checkbutton(master, text="Show search", bg=DARKGRAY, fg ="white", activebackground = DARKGRAY, activeforeground = "white", selectcolor=DARKGRAY, variable=showsearch)
c_pattern.grid(row=2, column=4, sticky = W)
#c_pattern.insert(0, str(maze_h))

b_new = Button(master,text="New", fg="white", bg = GRAY,relief=FLAT, width = 10)
b_new.grid(row=2, column=6, sticky=W+E)
b_new.bind("<Button-1>", newMaze)

b_rand = Button(master,text="Randomize", fg="white", bg = GRAY,relief=FLAT, width = 10)
b_rand.grid(row=2, column=7, sticky=W+E)
#b_rand.bind("<Button-1>", randomize)
b_rand.bind("<Button-1>", randomize)

b_solve = Button(master,text="Solve", fg="white", bg = GRAY,relief=FLAT, width = 10)
b_solve.grid(row=2, column=8, sticky=W+E)
b_solve.bind("<Button-1>", solve)

b_exit = Button(master,text="Exit", fg="white", bg = GRAY,relief=FLAT, width = 10)
b_exit.grid(row=2, column=9, sticky=W+E)
b_exit.bind("<Button-1>", endProg)

statusbar = Label(master, text="", bd=1, bg = DARKGRAY, fg = "yellow", pady=5, padx=5)
statusbar.grid(row=3, columnspan = 10, sticky=W+E)

drawGrid()

c.bind("<Button-1>", canvas_click)


master.mainloop()

