import numpy as np
class optimize:
	def __init__(self,obj):
		'''obj = 1 for min and 0 for max'''
		self.obj = obj
		self.A = [] #will be converted to ndarray in standerdize
		self.b = [] #will be converted to ndarray in standerdize
		self.c = [] #will be converted to ndarray in standerdize
		self.varcount = 0
		self.tableau = np.empty([1,1]) #will be converted to ndarray in createTableau
		self.status = "unbounded"
		self.B = []
		self.bfs = 0
	def standardize(self):
		'''
		convert to min if max. 
		add slack var. 
		make all vars ≥ 0
		decide initial bfs and basis(B) by solving auxiliary problem
		convert all to ndarrays 
		'''
		pass
	def createTableau(self):
		pass
	def isOptimal(self):
		for i in range(1,self.tableau.shape[1]):
			if(self.tableau[0,i]<0):
				return False
		self.status = "optimal" # tentative need to check if some component of u>0
		return True
	def tableauSolver(self):
		pass