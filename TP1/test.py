

import binascii
import random

random.seed()

def in_to_bin(x): #transformer un entier en binaire
    if x==0:
        return 0
    else:
        return x%2+10*in_to_bin(x//2)


def home_mod_expnoent(x,y,n): #exponentiation modulaire
    R1 = 1
    R2 = x
    i=0
    while(y!=0):
        if (y%2==1):
            R1 = R1*R2
            R1 = R1%n
            #print("R1 = ", R1)
        R2 = R2*R2
        R2 = R2%n
        #print("R2 = ", R2)
        i = i+1
        y = y//2
    return R1

def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)

def euclide_etendu(a, b):
    return recursive_euclide_etendu(a, b)[2]

def recursive_euclide_etendu(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, u, v = recursive_euclide_etendu(b, a % b)
        return (d, v, u - (a // b) * v)


k=10
def home_create_block(msg): #pour créer les blocs de 10 caractères
    j= k//2
    i=0
    msgblock=[]
    while (i<len(msg)):
        msgblock.append(msg[i:i+j])
        i=i+j
    return msgblock

def home_bourrage(msgblock): #pour bourrer les blocs de 10 caractères
    for msg in msgblock:

        alea=''
        for i in range(k-len(msg)-3):
            alea=alea+chr(random.randint(0,255))

        n_msg= chr(0)+chr(2)+alea+chr(0)+msg
        msgblock[msgblock.index(msg)]=n_msg
    return msgblock

print(home_bourrage(home_create_block("Bonjour je suis une patate")))