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
        for i in range(1, self.tableau.shape[1]):
            if (self.tableau[0, i] < 0):
                return False
        self.status = "optimal"  # tentative need to check if some component of u>0
        return True

    def tableauSolver(self):
        pass

problem = optimize(0)
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
