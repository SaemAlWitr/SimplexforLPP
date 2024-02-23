def isOptimal(self):
		for i in range(2,self.tableau.shape[1]):
			if(self.tableau[0,i] < 0):
				return False,i
		self.status = "optimal" 
		return True,0
	def tableauSolver(self):
		pass

	def phase2TableauSolver(self,tableau,c,A,b):
		#assuming Basis coulmn i.e. 0th in tableau is 0 indexed 
		self.tableau[0,1] = 0
		m = self.tableau.shape[0]-1
		for i in range(1,m+1):
			self.tableau[0,1] -= c[self.tableau[i,0]]*self.tableau[i,1]
		A_B = np.zeros((m,m)) #basis matrix
		for i in range(m):
			for j in range(m):
				A_B[j,i] = self.A[j,self.tableau[i,0]]
		c_B = np.zeros(m)
		for i in range(m):
			c_B[i] = self.c[self.tableau[i+1,0]]
		c_B = np.transpose(c_B)
		#get c hat
		c_ = np.transpose(self.c) - c_B*np.dot(np.linalg.inv(A_B),self.A)
		#update row 1
		for i in range(2,self.tableau.shape[1]):
			self.tableau[0,i] = c_[i-2]
		#tableau ready
		#solve it
		it = 10000
		while(it):
			#check feasible
			opt,j = self.isOptimal()
			if(opt):
				return 0
			c_j = tableau[0,j]
			l =-1
			ratio = 1e8
			for i in range(1,m+1):
				if(tableau[i,j]>0):
					if(ratio > self.tableau[i,1]/self.tableau[i,j]):
						ratio = self.tableau[i,1]/self.tableau[i,j]
						l = i
			if(l < 0):
				self.status = "unbounded"
				return 1
			pivot_ele = self.tableau[l,j]
			#update basis index
			self.tableau[l,0] = j
			# update lth row
			self.tableau[l,1:] = 1/pivot_ele*self.tableau[l,1:]
			#update rows except lth
			for i in range(m+1):
				if i==l: 
					continue
				self.tableau[i,1:] -= self.tableau[l,1:]*self.tableau[i,j]
			it-=1