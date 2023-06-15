# Réponse 1: L'intégrité est le plus important, comme expliqué, il ne faut surout pas que l'enprunte change,
# sinon le bloc invalidera tous les blocs suivants. (De toute facon il est très difficile de changer l'enprunte)
# Réponse 2: Le block est défini par son hash et le hash du block précédent ainsi que les données du block 
# ( la liste de transaction)
# Réponse 3: Il n'y a pas la signature et la preuve de travail
# Réponse 5: Il n'y a aucune certitude sur le contenu du bloc, il n'y a pas de signature, 
# donc n'importe qui peut modifier les valeurs
# Réponse 6: En utilisant un pc portable peu puissant maximum 6 zéros, 
# en utilisant un pc puissant 7 zéros



from ecdsa import SigningKey, NIST384p
import hashlib
import secrets #Générateur de nombre aléatoire

private_key = SigningKey.generate() #Génération de la clé privée avec la bibliothèque ecdsa
public_key = private_key.verifying_key # Génération de la clé publique

def signtransaction(transaction_list): #Fonction de signature
    signature = private_key.sign(transaction_list.encode()) #Signature de la transaction
    return signature #Retourne la signature

def verifytransaction(signature,transaction_list): #Fonction de vérification
    verify = public_key.verify(signature, transaction_list[0].encode()) #Vérification de la transaction
    return verify #Retourne la vérification (True ou False)

class Block:
    
    def __init__(self, previous_block_hash, transaction_list,signature=None):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list
        self.signature = signature #Ajout de la signature

        try:
            self.verify = verifytransaction(self.signature, self.transaction_list) #Ajout de la vérification
        except:
            self.verify = False #Si la vérification ne fonctionne pas, la transaction est fausse
            print("Transaction invalide")

        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash } - {self.signature}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        while self.block_hash[:5] != "00000":
            mining_nonce = secrets.randbits(64)
            self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash } - {self.signature} - {mining_nonce}"
            self.block_hash = hashlib.sha256(self.block_hash.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()

    def generate_genesis_block(self):
        self.chain.append(Block("0", ['Genesis Block']))
    
    def create_block_from_transaction(self, transaction_list,signature=None):
        previous_block_hash = self.last_block.block_hash
        self.chain.append(Block(previous_block_hash,transaction_list,signature))

    def display_chain(self):
        for i in range(len(self.chain)):
            #print(f"Data {i + 1}: {self.chain[i].block_data}")
            #print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")
            print(f"Data {i +1}: {self.chain[i].block_data.split(' - ')[0]}\n")
            print(f"Hash {i +1}: {self.chain[i].block_hash}\n")
            print(f"Signature {i +1}: {self.chain[i].block_data.split(' - ')[2]}\n")
            print(f"mining_nonce {i +1}: {self.chain[i].block_data.split(' - ')[3]}\n")

    @property
    def last_block(self):
        return self.chain[-1]

t1 = "L'employeur me verse 2000 €"
t2 = "J'ai dépensé 70 € chez Total"
t3 = "J'ai dépensé 5 € chez amazone"
t4 = "J'ai dépensé 100 € chez Auchan"
t5 = "J'ai dépensé 110 € chez Engi"
t6 = "J'ai dépensé 30 € chez SFR"


myblockchain = Blockchain()
myblockchain.create_block_from_transaction([t1]) #block 1 , appartenant à l'employeur
#les deux premiers blocs seront invalides (Genesis Block et block 1) 
myblockchain.create_block_from_transaction([t2],signature=signtransaction(t2))
myblockchain.create_block_from_transaction([t3],signature=signtransaction(t3))
myblockchain.create_block_from_transaction([t4],signature=signtransaction(t4))
myblockchain.create_block_from_transaction([t5],signature=signtransaction(t5))
myblockchain.create_block_from_transaction([t6],signature=signtransaction(t6))

myblockchain.display_chain()