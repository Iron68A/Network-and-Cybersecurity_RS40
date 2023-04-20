# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:44:40 2020

@author: Mr ABBAS-TURKI
"""

#info diverses cours : 
#MD5-> sha 256
# taile message > taille clé -> erreur
# refaire les clefs x1 x2 a et b, utilisé ea =17 et eb = 23
#utiliser Bigprimes.org avec Nofbits = 4 NbDigits =60-100
#e = 65537

#taille limité a 10 car p*q < 2^64 (8 octets) , les trop petites pour SHA256 (pour message > 10 caractères)
#nouvel limite avec sha256, en fonction taille clé, taille message a tester 

import hashlib
import binascii
import random

random.seed()

k= 10

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

def home_deblock(msgblock): #pour débourrer les blocs de 10 caractères

    for msg in msgblock:
        for i in range(len(msg),0,-1):
            if msg[i-1]==chr(0):
                msgblock[msgblock.index(msg)]=msg[i:]
                break
    return ''.join(msgblock)


def home_mod_expnoent(x,y,n): #exponentiation modulaire

    R1 = 1
    R2 = x
    while(y>0):
        if (y%2==1):
            R1 = R1*R2
            R1 = R1%n
            #print("R1 = ", R1)
        R2 = R2*R2
        R2 = R2%n
        #print("R2 = ", R2)
        y = y//2
    return R1

def in_to_bin(x): #transformer un entier en binaire
    if x==0:
        return 0
    else:
        return x%2+10*in_to_bin(x//2)



def home_ext_euclide(a, b): 
    return recursive_home_ext_euclide(a, b)[2]%a #a Refaire 

def recursive_home_ext_euclide(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, u, v = recursive_home_ext_euclide(b, a % b)
        return (d, v, u - (a // b) * v)

def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)

def home_string_to_int(x): # pour transformer un string en int
    z=0
    for i in reversed(range(len(x))):
        z=int(ord(x[i]))*pow(2,(8*i))+z
    return(z)


def home_int_to_string(x): # pour transformer un int en string
    txt=''
    res1=x
    while res1>0:
        res=res1%(pow(2,8))
        res1=(res1-res)//(pow(2,8))
        txt=txt+chr(res)
    return txt


def mot10char(): #entrer le secret
    secret=input("donner un secret de 10 caractères au maximum : ")
    
    #while (len(secret)>11)
     #   secret=input("c'est beaucoup trop long, 10 caractères S.V.P : ")
    return(secret)
    

#voici les éléments de la clé d'Alice
#x1a=2010942103422233250095259520183 #p
#x2a=3503815992030544427564583819137 #q
x1a=1063805098442660534749185384263601416082561751934318929114851809197247605578631913330241394071235709 #p
x2a=1982654118651898562310578873218402649336095562797128997417129319500916716306425513658404434814312487 #q
na=x1a*x2a  #n
phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
ea=17 #exposant public
da=home_ext_euclide(phia,ea) #exposant privé
#voici les éléments de la clé de bob
#x1b=9434659759111223227678316435911 #p
#x2b=8842546075387759637728590482297 #q
x1b=5396702109491801272042044631715247535808482875789666925238961828776776546780520690329977111997820959 #p
x2b=3163816943287154840448938988625767561279146987788414290109785763737929280845468284502267076973439393 #q

nb=x1b*x2b # n
phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
eb=23 # exposants public
db=home_ext_euclide(phib,eb) #exposant privé



print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
print("voici votre clé publique que tout le monde a le droit de consulter")
print("n =",nb)
print("exposant :",eb)
print("voici votre précieux secret")
print("d =",db)
print("*******************************************************************")
print("Voici aussi la clé publique d'Alice que tout le monde peut conslter")
print("n =",na)
print("exposent :",ea)
print("*******************************************************************")
print("il est temps de lui envoyer votre secret ")
print("*******************************************************************")
x=input("appuyer sur entrer")
secret=mot10char()
print("*******************************************************************")
print("voici la version en nombre décimal de ",secret," : ")

block = home_bourrage(home_create_block(secret))

num_sec=[]
for msg in block:
    num_sec.append(home_string_to_int(msg))
print(num_sec)
print("voici le message chiffré avec la publique d'Alice : ")

chif=[]
for a_num_sec in num_sec:
    chif.append(home_mod_expnoent(a_num_sec, ea, na))
print(chif)
print("*******************************************************************")
print("On utilise la fonction de hashage sha256 pour obtenir le hash du message",secret)
#Bhachis0=hashlib.md5(secret.encode(encoding='UTF-8',errors='strict')).digest() #MD5 du message
Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8',errors='strict')).digest() #sha256 du message


print("voici le hash en binaire ")
print("voici le hash en nombre décimal ")
Bhachis1=binascii.b2a_uu(Bhachis0)
Bhachis2=Bhachis1.decode() #en string
Bhachis3=home_string_to_int(Bhachis2)
print(Bhachis3)
print("voici la signature avec la clé privée de Bob du hachis")
signe=home_mod_expnoent(Bhachis3, db, nb)
print(signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n",chif,"\n \t 2-et le hash signé \n",signe)
print("*******************************************************************")
x=input("appuyer sur entrer")
print("*******************************************************************")
print("Alice déchiffre le message chiffré \n",chif,"\nce qui donne ")
dechif=[]
for a_chif in chif:
    dechif.append(home_int_to_string(home_mod_expnoent(a_chif, da, na)))
print(dechif)
print("*******************************************************************")

dechif=home_deblock(dechif)
print("Alice débloque le message \n",dechif)
print("*******************************************************************")

print("Alice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
designe=home_mod_expnoent(signe, eb, nb)
print(designe)
print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)

Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8',errors='strict')).digest() #sha256 du message
#Ahachis0=hashlib.md5(dechif.encode(encoding='UTF-8',errors='strict')).digest()
Ahachis1=binascii.b2a_uu(Ahachis0)
Ahachis2=Ahachis1.decode()
Ahachis3=home_string_to_int(Ahachis2)
print(Ahachis3)
print("La différence =",Ahachis3-designe)
if (Ahachis3-designe==0):
    print("Alice : Bob m'a envoyé : ",dechif)
else:
    print("oups")