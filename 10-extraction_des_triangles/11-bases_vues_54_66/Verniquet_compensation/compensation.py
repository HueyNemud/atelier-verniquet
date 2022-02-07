import math
import random
import numpy as np
import matplotlib.pyplot as plt

from triangulation import *



datafile = open('angles_orientes.dat', 'r')
data = datafile.readlines()
datafile.close()

TIDX = []
ALPHA = []

def commonBase(tidx1, tidx2):
	count = 0
	for idx in tidx1:
		if idx in tidx2:
			count += 1
	return count > 1
			
def isConnected(A):
	Nt = A.shape[0]
	return np.min(np.linalg.matrix_power(A + np.eye(Nt), Nt-1)) > 0
	
def diameter(A):
	Nt = A.shape[0]
	A = A + np.eye(Nt); M = A
	for i in range(1,Nt):
		M = M @ A
		if (np.min(M) > 0):
			return i
	return -1
	
def makeAndjacentMatrix(TIDX):
	Nt = len(TIDX)
	A = np.zeros((Nt, Nt))
	for i in range(Nt):
		for j in range(Nt):
			A[i,j] = (commonBase(TIDX[i], TIDX[j]) and (i != j))*1
	return A;
	


data = data[2:]

for i in range(int(len(data)/3)):
	

	line1 = data[3*i+0][0:-1].split(',')
	line2 = data[3*i+1][0:-1].split(',')
	line3 = data[3*i+2][0:-1].split(',')
	
	alpha1 = round(float(line1[4]) + float(line1[5])/60 + float(line1[6])/3600, 6)*math.pi/180;
	alpha2 = round(float(line2[4]) + float(line2[5])/60 + float(line2[6])/3600, 6)*math.pi/180;
	alpha3 = round(float(line3[4]) + float(line3[5])/60 + float(line3[6])/3600, 6)*math.pi/180;
	
	TIDX.append([line1[2].replace('"', ''), line2[2].replace('"', ''), line3[2].replace('"', '')])
	ALPHA.append([alpha1, alpha2, alpha3])

print(TIDX)
print(ALPHA)
exit(1)

t1 = Triangle(TIDX[0]); t1.setAngles(ALPHA[0], unit = ANGLE_UNIT_RAD)
t1.setPosition("Observatoire", Y=0.00541)
t1.setPosition("Piramide", Y = 20)

t2 = Triangle(TIDX[1]); t2.setAngles(ALPHA[1], unit = ANGLE_UNIT_RAD)
t2.setPosition("Observatoire", Y=0.00541)
t2.setPosition("Piramide", Y = 20)

t3 = Triangle(TIDX[2]); t3.setAngles(ALPHA[2], unit = ANGLE_UNIT_RAD)
t3.setPosition("Piramide", Y = 20)
t3.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)

t4 = Triangle(TIDX[3]); t4.setAngles(ALPHA[3], unit = ANGLE_UNIT_RAD)
t4.setPosition("Observatoire", Y=0.00541)
t4.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)

t5 = Triangle(TIDX[4]); t5.setAngles(ALPHA[4], unit = ANGLE_UNIT_RAD)
t5.setPosition("Piramide", Y = 20)
t5.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)

t6 = Triangle(TIDX[5]); t6.setAngles(ALPHA[5], unit = ANGLE_UNIT_RAD)
t6.setPosition("Observatoire", Y=0.00541)
t6.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)

t7 = Triangle(TIDX[6]); t7.setAngles(ALPHA[6], unit = ANGLE_UNIT_RAD)
t7.setPosition("Observatoire", Y=0.00541)
t7.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)

t8 = Triangle(TIDX[7]); t8.setAngles(ALPHA[7], unit = ANGLE_UNIT_RAD)
t8.setPosition("Piramide", Y = 20)
t8.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)

t9 = Triangle(TIDX[8]); t9.setAngles(ALPHA[8], unit = ANGLE_UNIT_RAD)
t9.setPosition("Observatoire", Y=0.00541)
t9.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)

t10 = Triangle(TIDX[9]); t10.setAngles(ALPHA[9], unit = ANGLE_UNIT_RAD)
t10.setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
t10.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)

t11 = Triangle(TIDX[10]); t11.setAngles(ALPHA[10], unit = ANGLE_UNIT_RAD)
t11.setPosition("St Sulpice", X = -0.611685, Y = 5.703124)
t11.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)

t12 = Triangle(TIDX[11]); t12.setAngles(ALPHA[11], unit = ANGLE_UNIT_RAD)
t12.setPosition("Observatoire", Y=0.00541)
t12.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)

t13 = Triangle(TIDX[12]); t13.setAngles(ALPHA[12], unit = ANGLE_UNIT_RAD)
t13.setPosition("Observatoire", Y=0.00541)
t13.setPosition("St Sulpice", X = -0.611685, Y = 5.703124)


t14 = Triangle(TIDX[13]); t14.setAngles(ALPHA[13], unit = ANGLE_UNIT_RAD)
t14.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
t14.setPosition("St Sulpice", X = -0.611685, Y = 5.703124)

t15 = Triangle(TIDX[14]); t15.setAngles(ALPHA[14], unit = ANGLE_UNIT_RAD)
t15.setPosition("Ste Margueritte", X = 11.663692, Y = 6.381898)
t15.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)

t16 = Triangle(TIDX[15]); t16.setAngles(ALPHA[15], unit = ANGLE_UNIT_RAD)
t16.setPosition("Piramide", Y = 20)
t16.setPosition("St Sulpice", X = -0.611685, Y = 5.703124)


t17 = Triangle(TIDX[16]); t17.setAngles(ALPHA[16], unit = ANGLE_UNIT_RAD)
t17.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
t17.setPosition("St Sulpice", X = -0.611685, Y = 5.703124)

t18 = Triangle(TIDX[17]); t18.setAngles(ALPHA[17], unit = ANGLE_UNIT_RAD)
t18.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
t18.setPosition("Piramide", Y = 20)


t19 = Triangle(TIDX[18]); t19.setAngles(ALPHA[18], unit = ANGLE_UNIT_RAD)
t19.setPosition("Notre-Dame", X = 3.266953, Y = 6.471765)
t19.setPosition("Porte St Denis", X = 4.175919, Y = 13.001454)

T = []

t1.solve(); T.append(t1)
t2.solve(); T.append(t2)
t3.solve(); T.append(t3)
t4.solve(); T.append(t4)
t5.solve(); T.append(t5)
t6.solve(); T.append(t6)
t7.solve(); T.append(t7)
t8.solve(); T.append(t8)
t9.solve(); T.append(t9)
t10.solve(); T.append(t10)
t11.solve(); T.append(t11)
t12.solve(); T.append(t12)
t13.solve(); T.append(t13)
t14.solve(); T.append(t14)
t15.solve(); T.append(t15)
t16.solve(); T.append(t16)
t17.solve(); T.append(t17)
t18.solve(); T.append(t18)
t19.solve(); T.append(t19)



print(t1)
print(t2)
print(t3)
print(t4)
print(t5)
print(t6)
print(t7)
print(t8)
print(t9)
print(t10)
print(t11)
print(t12)
print(t13)
print(t14)
print(t15)
print(t16)
print(t17)
print(t18)
print(t19)


t1.plot(point = 'k.')
t2.plot(point = 'k.')
t3.plot(point = 'k.')
t4.plot(point = 'k.')

t5.plot(point = 'k.')
t6.plot(point = 'k.')
t7.plot(point = 'k.')
t8.plot(point = 'k.')

t9.plot(point = 'k.')
t10.plot(point = 'k.')
t11.plot(point = 'k.')
t12.plot(point = 'k.')
t13.plot(point = 'k.')

t14.plot(point = 'k.')
t15.plot(point = 'k.')
t16.plot(point = 'k.')
t17.plot(point = 'k.')
t18.plot(point = 'k.')
t19.plot(point = 'k.')


stations = ["Notre-Dame", "St Sulpice", "Porte St Denis"]

for s in stations:
	X = []; Y = [];
	for t in T:
		if s in t.sommets:
			X.append(t.positions[s][0]*10**(3.46406766)/20.0)
			Y.append(t.positions[s][1]*10**(3.46406766)/20.0)
			
	X = np.array(X)
	Y = np.array(Y)

	factor = math.sqrt(X.shape[0])
	print(s, "  [", np.mean(X), "+/-", np.std(X), "," , np.mean(Y), "+/-", np.std(Y),"]")


plt.show()
