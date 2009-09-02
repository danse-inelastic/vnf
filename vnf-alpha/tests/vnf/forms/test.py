import numpy as np

pos=[[0,0,0],[2,2,2]]

lat=[[4,0,0],[0,4,0],[0,0,4]]

vec=np.array(pos)
print vec
mat=np.linalg.inv(lat)
print mat
fracPos=np.dot(vec,mat)
print fracPos
fracPosList=fracPos.tolist()