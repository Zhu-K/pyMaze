# Generates a customizable random maze and solves it with BFS
# Click on the GUI edges to customize node connection
# Author: Kai Zhu
VERSION = "1.0"

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

def newMaze(*arg):
    global maze_w, maze_h, grid_width, grid_height, mz, swidth, sheight

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

def canvas_click(event):
    x = int(event.x // grid_width)       # get grid coords
    y = int(event.y // grid_height)
    
    local_x = event.x - x * grid_width      # get local coords inside grid
    local_y = event.y - y * grid_height
    dir = -1                    # initialize search direction

    if local_y < grid_height * 0.2:
        dir = 1 # top
    elif local_y > grid_height * 0.8:
        dir = 3 # bottom
    elif local_x < grid_width * 0.2:
        dir = 4 # left
    elif local_x > grid_width * 0.8:
        dir = 2 # right
    else:
        dir = 0 # middle
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
            c.create_oval((x+0.5)*grid_width-NODE_RAD, (y+0.5)*grid_height-NODE_RAD, (x+0.5)*grid_width+NODE_RAD, (y+0.5)*grid_height+NODE_RAD, fill="green", outline="green", tag = "end")  # resetting start


    if dir > 0:
        adj = mz.getAdjNode(x,y,dir)
        if adj:
            connected = not mz.nodes[y][x][dir]
            mz.nodes[y][x][dir] = connected    # flip accessibility
            mz.nodes[adj[1]][adj[0]][(dir+1)%4+1] = connected # flip recriprocal dir in connected square

            drawWall(x,y,dir,connected)

def drawWall(x, y, dir, unblocked):
    # draws maze walls

    x0,y0,x1,y1 = 0,0,0,0
    if dir == 1:        # up
        x0 = x * grid_width + LINESPACE
        y0 = y * grid_height
        x1 = (x+1) * grid_width - LINESPACE
        y1 = y * grid_height
    elif dir == 2:      # right
        x0 = (x+1) * grid_width
        y0 = y * grid_height + LINESPACE
        x1 = (x+1) * grid_width
        y1 = (y+1) * grid_height - LINESPACE
    elif dir == 3:      # bottom
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
    s2 = ",".join([str(adj[0]), str(adj[1]), str((dir+1)%4+1)])

    if unblocked:
        #c.create_line(x0,y0,x1,y1,fill="black", width = 2, tag = ",".join([str(x), str(y), str(dir)]))
        c.delete(s1)
        c.delete(s2)
    else:
        c.create_line(x0,y0,x1,y1,fill="white", width = 1, tag = (s1,"wall"))

def randomize(event):
    # creates random maze

    newMaze()

    timer = time()

    for y in range(maze_h):
        for x in range(maze_w):
            for dir in range(1,5):
                adj = mz.getAdjNode(x,y,dir)
                if adj:
                    ran = (random.getrandbits(1) == 1)
                    mz.nodes[y][x][dir] = ran
                    mz.nodes[adj[1]][adj[0]][(dir+1)%4+1] = ran       # change complement link too
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
            for dir in range(1,5):
                adj = mz.getAdjNode(x,y,dir)  
                if adj:  
                    drawWall(x,y,dir,mz.nodes[y][x][dir])

def drawPath(path):
    # solution path

    c.delete("path")
    x0, y0 = mz.getXY(path[0])
    x0 = (x0 + 0.5) * grid_width
    y0 = (y0 + 0.5) * grid_height

    for i in range(1, len(path)):
        x1, y1 = mz.getXY(path[i])
        x1 = (x1 + 0.5) * grid_width
        y1 = (y1 + 0.5) * grid_height
        c.create_line(x0,y0,x1,y1,fill="yellow", width = 2, tag = "path")
        x0, y0 = x1, y1

def solve(event):
    timer = time()
    # solve the maze via BFS and pass solution to drawPath

    if not mz.start or not mz.end:
        statusbar.configure(text="Missing start or end points. Click on maze grid to set.")
    else:
        drawMaze()
        queue = [[mz.start,[mz.getIndex(mz.start[0],mz.start[1])]]]
        visited = {mz.nodes[mz.start[1]][mz.start[0]][0]}       # remember visited node indices

        while queue:
            node = queue.pop(0)
            x, y = node[0]
            path = node[1]

            if x == mz.end[0] and y == mz.end[1]:
                #print("FOUND PATH!!!!")
                drawPath(path)
                statusbar.configure(text=f"maze solved in{(time()-timer):10.4f} s")
                return
            else:
                for i, unblocked in enumerate(mz.nodes[y][x][1:]):
                    if unblocked:
                        adj = mz.getAdjNode(x,y,i+1)     # dir = i+1
                        if mz.nodes[adj[1]][adj[0]][0] not in visited:
                            #queue.append(adj)
                            adj_ind = mz.getIndex(adj[0], adj[1])
                            queue.append([adj, path + [adj_ind]])
                            visited.add(adj_ind)
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

b_new = Button(master,text="New", fg="white", bg = GRAY,relief=FLAT, width = 10)
b_new.grid(row=2, column=6, sticky=W+E)
b_new.bind("<Button-1>", newMaze)

b_rand = Button(master,text="Randomize", fg="white", bg = GRAY,relief=FLAT, width = 10)
b_rand.grid(row=2, column=7, sticky=W+E)
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

