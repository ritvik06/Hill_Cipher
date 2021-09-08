import sys
import os
import numpy as np
import math
from sympy import Matrix
from collections import Counter
from utils import modMatInv

ALPHABET_SIZE = 26

#I/O function
def init_and_preprocess(mode='fileio'):

    if mode=='read':
        str_cipher = str(input("Enter the complete Cipher Text : "))
        str_input = str(input("Enter the substring of Plain Text : "))
    else:
        input_file = sys.argv[1]
        cipher_file = sys.argv[2]

        cwd = os.getcwd() 

        str_input = open(cwd + '/' + input_file, "r").read()
        str_cipher = open(cwd + '/' + cipher_file, "r").read()

    #todo - Remove all characters other than A-Z
    str_input = "".join(str_input.split())
    str_cipher = "".join(str_cipher.split())

    # Convert input & key to vector A - Z -> 0 - 25
    input_plain = [(ord(char_input) - 65) for char_input in str_input]
    input_cipher  = [(ord(char_cipher) - 65) for char_cipher in str_cipher]

    return np.asarray(input_cipher), np.asarray(input_plain)

#find index of coincidence for plain text
def ioc(input_text):

    freq_idx = Counter(np.asarray(input_text))
    N = len(input_text)

    return np.sum([freq_idx[idx]*(freq_idx[idx]-1) for idx in freq_idx.keys()]) / (N*(N-1))


def find_key(input_vec, cipher_vec, k):

    #Choose first k^2 elements of plain text and cipher text

    #Equation is Key * Plain = Cipher mod 26
    #Save all keys of key_size k

    keys = []

    for start_idx in range(0, len(input_vec)- k**2 + 1):
        input_matrix = input_vec[start_idx:start_idx + k**2].reshape((k, k))

        input_matrix = np.transpose(input_matrix)

        cipher_matrix = cipher_vec[start_idx:start_idx + k**2].reshape((k, k))

        cipher_matrix = np.transpose(cipher_matrix)

        try:
            input_inv_matrix = np.asarray(modMatInv(input_matrix, ALPHABET_SIZE))
        except:
            continue

        key = np.matmul(cipher_matrix, input_inv_matrix)

        key = np.remainder(key, ALPHABET_SIZE)

        keys.append(key)

    return keys


def find_plaintext(keys, cipher_vec, k):

    #find plain text from cipher text start_idx + k**2 onwards

    #saves ioc values for plaintext
    ioc_arr, key_arr = [], []

    for idx, key_matrix in enumerate(keys):

        #Calculate plain text as (mod N inv of key) * (cipher text) mod N
        if len(cipher_vec) % k:
            cipher_vec = np.append(cipher_vec, [0]*(k - (len(cipher_vec)%k)))

        cipher_matrix = cipher_vec.reshape((len(cipher_vec) // k, k))

        try:
            key_inv_matrix = np.asarray(modMatInv(key_matrix, ALPHABET_SIZE))
        except:
            continue

        plaintext = np.int_(np.matmul(key_inv_matrix, np.transpose(cipher_matrix)))

        plaintext = np.remainder(plaintext, ALPHABET_SIZE)

        plain_vec = plaintext.reshape((plaintext.shape[0] * plaintext.shape[1]))

        ioc_arr.append(ioc(plain_vec))
        key_arr.append(key_matrix)

    return ioc_arr, key_arr


if __name__  == "__main__":

    cipher_vec, input_vec = init_and_preprocess()

    best_ioc_diff = 1

    for key_size in range(2, 11):
        keys = find_key(input_vec, cipher_vec, key_size)

        ioc_arr, key_arr = find_plaintext(keys, cipher_vec, key_size)

        ioc_diff = np.abs(np.asarray(ioc_arr) - 0.065)

        best_idx = np.argmin(ioc_diff)

        if ioc_diff[best_idx] < best_ioc_diff:
            best_ioc_diff = ioc_diff[best_idx]
            best_ioc = ioc_arr[best_idx]
            best_key = key_arr[best_idx]

        print('Key Size : {} ; Best Index of Coincidence : {:.5f}'.format(key_size, ioc_arr[best_idx]))

        print('Key - \n', key_arr[best_idx])

    print('\nBest Overall Index of Coincidence : {:.5f}, Key Size : {}'.format(best_ioc, best_key.shape[0]))
    print('Best Overall Key - \n', best_key)









