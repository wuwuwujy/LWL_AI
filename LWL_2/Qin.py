import os
import math
import numpy as np
import queue
import sys
import copy

class flowfree:
	#We use a stracture to record the basic information of graph which include the color position, width, height
	def __init__(self, graph=[], height=0, width=0, color=[], colorpos=dict()):
		self.graph=[] 
		self.height=0
		self.width=0
		self.color=[]
		self.colorpos=dict()

		return

	#Input : graph, txt file containing maze
	#Description: In this function, we read the txt file of graph line by line, 
	# and store the maze structure in a 2D list. The height and width of maze
	# are recorded too.
	def readgraph(self,filename):
		self.graph= []
		with open(filename,"r") as fp:
			for line in fp:
				self.graph.append(list(line[0:len(line)-1]))
		fp.close()
		self.height = len(self.graph)
		self.width = len(self.graph[0])
		return

	#Input : graph
	#Output: None
	#Description: In this function, we travel all point of the graph and find colors and its corresponding position
	
	def findcolors(self):
		for i in range(self.width):
			for j in range(self.height):
				if self.graph[j][i]!= '_':
					if self.graph[j][i] not in self.color:
						self.color.append(self.graph[j][i])
						self.colorpos[self.graph[j][i]]=[(j,i)]
					else:
						self.colorpos[self.graph[j][i]].append((j,i))

		return

	#Input : graph
	#Output: none
	#Description: print the graph on the terminal
	def printgraph(self):
		for line in self.graph:
			print(''.join(line))

	def var_constrain(self,pos):
		x,y=pos[0],pos[1]
		barricade=[]
		if x-1>=0:
			if self.graph[x-1][y]=='_':
				barricade.append((x - 1,y))
		if x + 1<self.height:
			if self.graph[x+1][y]=='_':
				barricade.append((x + 1, y))
		if y - 1 >= 0:
			if self.graph[x][y-1]=='_':
				barricade.append((x, y - 1))
		if y + 1 < self.width:
			if self.graph[x][y+1]=='_':
				barricade.append((x, y + 1))
		return barricade
	def backtracking():
		graph = self.graph
		boundary = self.boundary
		colors = self.colors
		if backtracking_h(graph,boundary,colors):
			for line in graph:
				print(''.join(line))

	def change_boundary(graph,boundary,path):
		for i in path:
			x=i[0]
			y=i[1]
			if graph[x][y] != '_' :
				boundary[x,y] = 0 # not a boundary if a path is applied 

			if x - 1 >= 0 and y - 1 >= 0: # set surrounding area to be boundary
				if graph[x-1][y-1] = '_' :
					boundary[x-1,y] = 1
			if x - 1 >= 0:
				if graph[x-1][y] = '_' :
					boundary[x-1,y] = 1
			if x + 1 < self.height:
				if graph[x+1][y] = '_' :
					boundary[x+1,y] = 1
			if x + 1 < self.height and y - 1 >= 0:
				if graph[x+1][y-1] = '_' :
					boundary[x-1,y-1] = 1
			if y - 1 >= 0:
				if graph[x][y-1] = '_' :
					boundary[x,y-1] = 1
			if y + 1 < self.width:
				if graph[x][y+1] = '_' :
					boundary[x,y+1] = 1
			if x + 1 < self.height and y + 1 <self.width:
				if graph[x+1][y+1] = '_' :
					boundary[x+1,y+1] = 1
			if x - 1 >= 0 and y + 1 < self.width:
				if graph[x-1][y+1] = '_' :
					boundary[x-1,y+1] = 1



	def change_graph(graph,path,color):
		for i in path:
			graph[i[0]][i[1]] = color

	def backtracking_h(graph,boundary,colors):
		if assignment complete: # find all of the paths
			return True
		color = assign_variable(graph,boundary,colors) # choose which variable to assign
		Search_result=Search(var, boundary)# search for the paths return a list according to priority
		for path in Search_result:
			if path is consistant:
				#change graph,boundary,colors
				tempg=graph.copy()
				tempb=boundary.copy()
				tempc=colors.copy()
				change_boundary(boundary,path)
				change_graph(graph,path,color)
				colors=[colors[i] for i in range(len(colors)) if colors[i] != color ] 
				result = backtracking_h(graph,boundary,colors)
				if result != False:
					return result
				graph=tempg #restore graph,boundary,colors
				boundary=tempb
				colors=tempc

		return False









a=flowfree()
a.readgraph('input77.txt')
a.findcolors()
print(a.color)
print(a.colorpos)
a.printgraph()
#print(a.colorpos['O'][0][0])
print(a.var_constrain(a.colorpos['O'][0]))



		
