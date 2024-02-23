import numpy as np


class optimize:
	def __init__(self, obj):
		'''obj = 1 for min and 0 for max'''
		self.obj = obj
		self.A = []  # will be converted to ndarray in standerdize
		self.b = []  # will be converted to ndarray in standerdize
		self.c = []  # will be converted to ndarray in standerdize
		self.constr = []  # <= if 1; = if 2; >= if 3
		self.varcount = 0
		self.tableau = np.empty([1, 1])  # will be converted to ndarray in createTableau
		self.status = "unbounded"
		self.B = []
		self.bfs = 0

	def standardize(self):
		if self.obj == 0:  # if maximization
		    for i in range(len(self.c)):
		        self.c[i] = -self.c[i]
		num_constraints = len(self.constr)
		num_vars = len(self.A[0])
		A_slack = np.zeros((num_constraints, num_vars + num_constraints))
		c_slack = np.zeros(num_vars + num_constraints)

		for i in range(num_constraints):
		    if self.constr[i] == 1:
		        A_slack[i, :num_vars] = self.A[i, :]
		        A_slack[i, num_vars + i] = 1
		    elif self.constr[i] == 2:
		        A_slack[i, :num_vars] = self.A[i, :]
		    elif self.constr[i] == 3:
		        A_slack[i, :num_vars] = self.A[i, :]
		        A_slack[i, num_vars + i] = -1
		c_slack[:num_vars] = self.c
		self.A = A_slack
		self.c = c_slack

		for i in range(num_constraints):
			if self.b[i] < 0:
				for j in range(num_vars):
					self.A[i][j] = -self.A[i][j]
				self.b[i] = -self.b[i]

        

	def createTableau(self):
		pass
	def tableau_maker_phase1(c, A, b):
    		m, n = A.shape
    		cost_array=np.full(n,-1)
    		reduced_costs= cost_array @ A
    		# Phase 1: Add artificial variables
    		A_phase1 = np.hstack((A, np.eye(m)))
    		# m more variables
    		array=np.zeros(m+1)
    		a=m+1
    		for i in range(len(array)):
        		if(i!=0):
            			array[i]=a
            			a+=1
    		new_array=np.expand_dims(array, axis=1)
    
    		reduced_cost = np.hstack((reduced_costs, np.zeros(m)))

    		sum=0
    		for i in b:
        		sum+=i
    		cost=-sum
    
    		b_added = np.insert(b, 0, cost)
    		b_reshaped = np.expand_dims(b_added, axis=1)
    		tableau_with_costs=np.vstack((reduced_cost,A_phase1))

    
    		tableau_with_costs=np.hstack((b_reshaped, tableau_with_costs))
    		tableau_with_costs=np.hstack((new_array,tableau_with_costs))
    
		return tableau_with_costs
	def isOptimal(self):
		for i in range(2,self.tableau.shape[1]):
			if(self.tableau[0,i] < 0):
				return False,i
		self.status = "optimal" 
		return True,0
	def tableauSolver(self):
		pass

	def phase2TableauSolver(self):
		#assuming Basis coulmn i.e. 0th in tableau is 0 indexed 
		self.tableau = self.tableau.astype(float)
		self.tableau[0,1] = 0
		m = self.tableau.shape[0]-1

		for i in range(1,m+1):
			self.tableau[0,1] -= self.c[int(self.tableau[i,0])]*self.tableau[i,1]
		A_B = np.zeros((m,m)) #basis matrix
		for i in range(m):
			for j in range(m):
				A_B[j,i] = self.A[j,int(self.tableau[i+1,0])]
		c_B = np.zeros(m)
		for i in range(m):
			c_B[i] = self.c[int(self.tableau[i+1,0])]
		c_B = np.transpose(c_B)
		#get c hat
		c_ = np.transpose(self.c) - np.dot(c_B,np.dot(np.linalg.inv(A_B),self.A))
		#update row 1
		for i in range(2,self.tableau.shape[1]):
			self.tableau[0,i] = c_[i-2]
		#tableau ready
		#solve it
		it = 10000
		while(it):
			#check feasible
			print(self.tableau)
			opt,j = self.isOptimal()
			if(opt):
				return 0
			c_j = self.tableau[0,j]
			l =-1
			ratio = 1e8
			for i in range(1,m+1):
				if(self.tableau[i,j]>0):
					if(ratio > self.tableau[i,1]/self.tableau[i,j]):
						ratio = self.tableau[i,1]/self.tableau[i,j]
						l = i
			if(l < 0):
				self.status = "unbounded"
				return 1
			pivot_ele = self.tableau[l,j]
			#update basis index
			self.tableau[l,0] = j - 2
			# update lth row
			self.tableau[l,1:] = 1/pivot_ele*self.tableau[l,1:]
			#update rows except lth
			for i in range(m+1):
				if i==l: 
					continue
				self.tableau[i,1:] -= self.tableau[l,1:]*self.tableau[i,j]
			it-=1

problem = optimize(1)
c = [-10, -12, -12]
A = np.array([[1, 2,2], [2, 1, 2],[2,2, 1]])
b = [20,20,20]

constr = [1, 1, 1]
problem.A = A
problem.b = b
problem.c = c
problem.constr = constr

problem.standardize()
print(problem.A)
print(problem.b)
print(problem.c)
problem.tableau = np.array([[0,0,-10,-12,-12,0,0,0],[3,20,1,2,2,1,0,0],[4,20,2,1,2,0,1,0],[5,20,2,2,1,0,0,1]])
print(problem.tableau)
problem.phase2TableauSolver()
print(problem.tableau)


