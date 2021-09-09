# Code for finding inverse modulo sourced and modified from https://github.com/ctfs/write-ups-2015/blob/master/ghost-in-the-shellcode-2015/crypto/nikoli/hilly.py
import numpy as np

# Return matrix A with the ith row and jth column deleted
def minor(A,i,j):
    return A[np.array(list(range(i))+list(range(i+1,A.shape[0])))[:,np.newaxis],
               np.array(list(range(j))+list(range(j+1,A.shape[1])))]

# Finds the inverse of a mod p, if it exists
def modInv(a,p):          
    try:
        return pow(a, -1, p)
    except:
	    raise ValueError(str(a)+" has no inverse mod "+str(p))

# Finds the inverse of matrix A mod p
def modMatInv(A,p):       
	n=len(A)
	adj=np.zeros(shape=(n,n))
	for i in range(0,n):
		for j in range(0,n):
			adj[i][j]=((-1)**(i+j)*int(round(np.linalg.det(minor(A,j,i)))))%p
	return (modInv(int(round(np.linalg.det(A))),p)*adj)%p



