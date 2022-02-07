import sys
import math
import matplotlib.pyplot as plt

ANGLE_UNIT_DEG = 0
ANGLE_UNIT_DMS = 1
ANGLE_UNIT_RAD = 2
ANGLE_UNIT_GON = 3

# -------------------------------------------------------------------------	
# Classe de gestion de la resolution des triangles geodesiques 
# Par defaut, orientation positive des triangles => les sommets sont 
# ordonnes dans le sens trigonometrique sur le pourtour du triangle
# Toutes les valeurs d'angles sont non-signees. 
# Si orientation positive :
#     - angle 1 positif
#     - angle 2 negatif
#     - angle 3 positif
# Si orientation negative :
#     - angle 1 negatif
#     - angle 2 positif
#     - angle 3 negatif
# -------------------------------------------------------------------------	
class Triangle:
	
	def __init__(self, sommets, orientation = +1, name = None):
		if not (len(sommets) == 3):
			print("Error: number of triangles vertices not equal to 3")
			sys.exit(1)
		self.bases = {}
		self.angles = {}
		self.positions = {}
		self.sommets = sommets
		self.orientation = orientation
		
		if name is None:
			s1 = str(self.sommets[0]).upper() 
			s2 = str(self.sommets[1]).upper() 
			s3 = str(self.sommets[2]).upper()
			self.name = "Triangle between " + s1 + ", " + s2 + " and " + s3
		else:
			self.name = name
			
		self.__check()
		
	def __check(self):
		two_pts = (self.sommets[0] == self.sommets[1])
		two_pts = two_pts or (self.sommets[1] == self.sommets[2])
		two_pts = two_pts or (self.sommets[0] == self.sommets[2])
		if two_pts:
			print("Error: " + str(self.name) + " must contain three different points")
			sys.exit(1)
			 
		
		
	def __str__(self):

		chaine  = "---------------------------------------------------------------------------------\n"
		chaine += self.name + "\n"
		chaine += "---------------------------------------------------------------------------------\n"
		chaine += " "*26 + "ALPHA" + " "*14 + "X" + " "*11 + "Y" + " "*13 + "BASE\n"
		for i in range(3):
			chaine += str(self.sommets[i]).upper() + " "*(21-len(self.sommets[i]))
			if self.sommets[i] in self.angles:
				chaine +=  '{:10.6f}'.format(self.angles[self.sommets[i]]) + " deg    "
			else:
				chaine += "    "
			if self.sommets[i] in self.positions:
				chaine +=  '{:10.6f}'.format(self.positions[self.sommets[i]][0]) + " "*2
				chaine +=  '{:10.6f}'.format(self.positions[self.sommets[i]][1]) + " "*6
			else:
				chaine += " "*28
			if self.sommets[i] in self.bases:
				chaine +=  '{:10.6f}'.format(self.bases[self.sommets[i]]) + "  "
			chaine += "\n"
		
		if len(self.angles) == 3:		
			somme = self.__sumAngles()
			chaine += "                    ----------------- \n"
			chaine += "SUM:                 " + '{:10.6f}'.format(somme) + " deg     "
			chaine += "(CLOSING: " + '{:6.6f}'.format(somme-180.0) + " deg)\n"
		chaine += "---------------------------------------------------------------------------------\n"
		if self.isSolved():
			chaine += "SOLVED TRIANGLE\n"
		else:
			if self.isSolvable():
				chaine += "SOLVABLE TRIANGLE\n"
			else:
				chaine += "NON-SOLVABLE TRIANGLE\n"
		chaine += "---------------------------------------------------------------------------------\n"
		return chaine
		
			
	def plot(self, line = 'k-', point = 'ko', text = False, hold = True):
		if not self.isSolved():
			print("Error: cannot plot unsolved triangle")
			sys.exit(1)
		x1 = self.positions[self.sommets[0]][0]; y1 = self.positions[self.sommets[0]][1];
		x2 = self.positions[self.sommets[1]][0]; y2 = self.positions[self.sommets[1]][1];
		x3 = self.positions[self.sommets[2]][0]; y3 = self.positions[self.sommets[2]][1];
		if not point is None:
			plt.plot([x1,x2,x3], [y1, y2, y3], point)
		if not line is None:
			plt.plot([x1,x2,x3,x1], [y1, y2, y3,y1], line)
		if text:
				plt.text(x1, y1, self.sommets[0])
				plt.text(x2, y2, self.sommets[1])
				plt.text(x3, y3, self.sommets[2])
		if not hold:
			plt.show()

		
	def __sumAngles(self):
		return self.angles[self.sommets[0]] + self.angles[self.sommets[1]]+ self.angles[self.sommets[2]] 
		
		
	def __closing(self):
		return self.__sumAngles() - 180.0	
		
		
	def angleStd(self):
		return abs(self.__closing())/math.sqrt(3)
		
		
	def getPointName(self, idx):
		return self.sommets[idx]
	def getPointPosition(self, idx):
		return self.positions[self.getPointName(idx)]
	def getPointAngle(self, idx):
		return self.angles[self.getPointName(idx)]
	def getPointBase(self, idx):
		return self.bases[self.getPointName(idx)]
	def whichBaseIsAvailable(self):
		for i in range(len(self.sommets)):
			if self.sommets[i] in self.bases:
				return i
		return -1
			
	def __complementAngles(self):
		if len(self.angles) < 2:
			print("Error: cannot complement angles: " + str(2-len(self.angles)) + " angle(s) missing")
			sys.exit(1)
		if len(self.angles) == 2:
			if (self.sommets[0] in self.angles) and (self.sommets[1] in self.angles):
				self.angles[self.sommets[2]] = 180.0 - self.angles[self.sommets[0]] - self.angles[self.sommets[1]]
			if (self.sommets[0] in self.angles) and (self.sommets[2] in self.angles):
				self.angles[self.sommets[1]] = 180.0 - self.angles[self.sommets[0]] - self.angles[self.sommets[2]]
			if (self.sommets[1] in self.angles) and (self.sommets[2] in self.angles):
				self.angles[self.sommets[0]] = 180.0 - self.angles[self.sommets[1]] - self.angles[self.sommets[2]]
	
	def __adjustAngles(self):
		if len(self.angles) < 3:
			print("Error: cannot adjust angles: " + str(3-len(self.angles)) + " angle(s) missing")
			sys.exit(1)
		somme = (self.__sumAngles() - 180)
		self.angles[self.sommets[0]] -= somme/3.0
		self.angles[self.sommets[1]] -= somme/3.0
		self.angles[self.sommets[2]] -= somme/3.0
			

	def setName(self, name):
		self.name = name

	def setAngle(self, name, value, unit = ANGLE_UNIT_DEG):
		if unit == ANGLE_UNIT_DMS:
			value = (value[0] + value[1]/60.0 + value[2]/3600.0)
		if unit == ANGLE_UNIT_GON:
			value = value*360.0/400.0
		if unit == ANGLE_UNIT_RAD:
			value = value*180.0/math.pi
		self.angles[name] = value
		
	def setAngles(self, values, unit = ANGLE_UNIT_DEG):
		for i in range(3):
			self.setAngle(self.sommets[i], values[i], unit = unit)

		
	def __computeBases(self):
		if (self.sommets[0] in self.positions) and (self.sommets[1] in self.positions):
			x1 = self.positions[self.sommets[0]][0]; x2 = self.positions[self.sommets[1]][0]
			y1 = self.positions[self.sommets[0]][1]; y2 = self.positions[self.sommets[1]][1]
			self.bases[self.sommets[2]] = math.sqrt((x2-x1)**2 + (y2-y1)**2)
		if (self.sommets[1] in self.positions) and (self.sommets[2] in self.positions):
			x1 = self.positions[self.sommets[1]][0]; x2 = self.positions[self.sommets[2]][0]
			y1 = self.positions[self.sommets[1]][1]; y2 = self.positions[self.sommets[2]][1]
			self.bases[self.sommets[0]] = math.sqrt((x2-x1)**2 + (y2-y1)**2)
		if (self.sommets[2] in self.positions) and (self.sommets[0] in self.positions):
			x1 = self.positions[self.sommets[2]][0]; x2 = self.positions[self.sommets[0]][0]
			y1 = self.positions[self.sommets[2]][1]; y2 = self.positions[self.sommets[0]][1]
			self.bases[self.sommets[1]] = math.sqrt((x2-x1)**2 + (y2-y1)**2)


	def setPosition(self, name, X = 0.0, Y = 0.0):
		self.positions[name] = [X,Y]
			
		
	def isSolvable(self):
		return (len(self.angles) >= 2) and (len(self.positions) >=  2)
		
		
	def isSolved(self):
		return (len(self.angles) == 3) and (len(self.positions) == 3)
		
		
	def solve(self):
		
		# Feasibility test
		if not self.isSolvable():
			s1 = str(self.sommets[0]).upper() 
			s2 = str(self.sommets[1]).upper() 
			s3 = str(self.sommets[2]).upper()
			print("Error: triangle " + s1 +" - " + s2 + " - " + s3 + " not solvable")
			sys.exit(1)
			
		# Trivial calculations
		self.__computeBases()
		self.__complementAngles()
		
		# Solving triangle
		b = self.sommets[self.whichBaseIsAvailable()]
		factor = self.bases[b]/math.sin(self.angles[b]*math.pi/180)
		
		X = []; Y = []; I = []
		for i in range(3):
			if self.sommets[i] == b:
				continue
			I.append(i)
			alpha = self.angles[self.sommets[i]]*math.pi/180
			self.bases[self.sommets[i]] = factor*math.sin(alpha)
			X.append(self.positions[self.sommets[i]][0]); 
			Y.append(self.positions[self.sommets[i]][1]);
			

		A0 = math.atan2(Y[1]-Y[0], X[1]-X[0])
			
		sign = (1 - 2*((3-I[0]-I[1]) % 2)) * (I[1] - I[0])/abs(I[1] - I[0])
		alpha1 = + A0 + sign*self.angles[self.sommets[I[0]]]*math.pi/180
		alpha2 = + A0 - sign*self.angles[self.sommets[I[1]]]*math.pi/180 + math.pi
		
		x = X[0] + self.bases[self.sommets[I[1]]]*math.cos(alpha1)
		y = Y[0] + self.bases[self.sommets[I[1]]]*math.sin(alpha1)
		
		xx = X[1] + self.bases[self.sommets[I[0]]]*math.cos(alpha2)
		yy = Y[1] + self.bases[self.sommets[I[0]]]*math.sin(alpha2)
		
		verif = math.sqrt((xx-x)**2 + (yy-y)**2)
		
		if verif > 1e-2*self.bases[b]:
			print("Error: " + self.name + " -> cross-check = " + '{:6.5f}'.format(verif) + " !")
			sys.exit(1)
		if verif > 1e-4*self.bases[b]:
			pass
			#print("Warning: " + self.name + " -> cross-check = " + '{:6.5f}'.format(verif) + " !")

		self.positions[b] = [0,0]
		self.positions[b][0] = (x + xx)/2.0
		self.positions[b][1] = (y + yy)/2.0
		
		
	
	def solveIfPossible(self):
		if not self.isSolvable():
			return False 
		else:
			self.solve()
			return True
