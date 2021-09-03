import numpy as np
import math
from sympy import Matrix

#I/O function
def init_and_preprocess():

    str_input = str(input("Enter your input in Plain Text : "))
    str_key = str(input("Enter your key in Plain Text : "))

    #todo - Remove all characters other than A-Z
    str_input = "".join(str_input.split())
    str_key = "".join(str_key.split())

    # Convert input & key to vector A - Z -> 0 - 25
    input_vec = [(ord(char_input) - 65) for char_input in str_input]
    input_key  = [(ord(char_key) - 65) for char_key in str_key]

    return np.asarray(input_key), np.asarray(input_vec)


#Creates matrix from input string key
def create_key_matrix(input_key):

    #string key length must be dim * dim
    assert np.sqrt(len(input_key)) == int(np.sqrt(len(input_key)))

    dim = int(np.sqrt(len(input_key)))

    #Construct key from vector->matrix
    key_matrix = np.zeros((dim, dim), dtype=np.int32)
    for i in range(dim):
        for j in range(dim):
            key_matrix[i][j] = input_key[(i*dim) + j]
            
    return key_matrix


# Construct (len(input_vec) / dim_key) vectors for the input
def create_input_vec(input_vec, dim_key):

    #Pad 0 to make input_vec multiple of dim_key
    if len(input_vec)%dim_key:
        input_vec = np.append(input_vec, [0]*(dim_key - (len(input_vec)%dim_key)))

    input_matrix = input_vec.reshape((len(input_vec) // dim_key, dim_key))

    return input_matrix, input_vec


#This function encrypts the input message
def encrypt(input_matrix, key_matrix):

    encrypt_matrix = np.zeros((len(input_matrix), len(input_matrix[0])), dtype=np.int32)

    for i in range(len(input_matrix)):
        encrypt_matrix[i] = np.squeeze(np.matmul(key_matrix, np.expand_dims(input_matrix[i], axis=1)))
    
    #Take modulo to create final encryption
    encrypt_matrix = np.remainder(encrypt_matrix, 26)

    #Convert encryption to string
    encrypt_string = ''

    for encrypt_sub_matrix in encrypt_matrix:
        encrypt_string += ''.join([chr(x+65) for x in encrypt_sub_matrix])

    return encrypt_matrix, encrypt_string



#This function decrypts the input message
def decrypt(encrypt_matrix, key_matrix):
    
    #Takes inverse modulo of key matrix
    key_inv_matrix = np.matrix(Matrix(key_matrix).inv_mod(26))

    decrypt_matrix = np.zeros(encrypt_matrix.shape, dtype=np.int32)

    for i in range(len(encrypt_matrix)):
        decrypt_matrix[i] = np.squeeze(np.matmul(key_inv_matrix, np.expand_dims(encrypt_matrix[i], axis=1)))

    #Take modulo to create final encryption
    decrypt_matrix = np.remainder(decrypt_matrix, 26)

    #Convert encryption to string
    decrypt_string = ''

    for decrypt_sub_matrix in decrypt_matrix:
        decrypt_string += ''.join([chr(x+65) for x in decrypt_sub_matrix])

    return decrypt_matrix, decrypt_string


if __name__  == "__main__":

    input_key, input_vec = init_and_preprocess()

    key_matrix = create_key_matrix(input_key)

    input_matrix, input_vec = create_input_vec(input_vec, key_matrix.shape[0])

    encrypt_matrix, encrypt_string = encrypt(input_matrix, key_matrix)

    print('String matrix after encryption : ', encrypt_matrix)

    print('Encrypted String : ', encrypt_string)

    decrypt_matrix, decrypt_string = decrypt(encrypt_matrix, key_matrix)

    print('String matrix after decryption : ', decrypt_matrix)

    print('Decrypted String : ', decrypt_string)
