# Hill_Cipher
Designed a Python-based Hill Cipher to encrypt plain text

## Installation Env
Python 3.6+ 

pip install -r requirements.txt

## 1. Usage - Encryption and Decryption

python src/cipher.py $loc. of input text$ $loc. of key text$

## Sample Input

Enter your input in Plain Text : ACEFTH \
Enter your key in Plain Text : GYBNQKURP 

### Output

String matrix after encryption - \[[ 0 20 16]
 [25 23  8]] \
Encrypted String :  AUQZXI \
\
String matrix after decryption -  [[ 0  2  4]
 [ 5 19  7]] \
Decrypted String :  ACEFTH

## 2. Usage - Cryptanalysis

python src/cryptanalysis.py $loc. of input text$ $loc. of cipher text$

## Sample Output

Key Size : 3 ; Best Index of Coincidence : 0.06983

Best Key - \
 \[[ 2.  4.  5.] \
 [ 9.  2.  1.] \
 [ 3. 17.  7.]] 
