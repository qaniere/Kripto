# coding: utf8
from random import *



def chiffrement(message, clefPublique, moduleDeChiffrement):

    """ Fonction qui chiffre le message selon l'algorithme RSA et le formate en une seule chaine de caractère.
    Cette fonction doit prendre comme argument :
        - Le message à chiffre
        - La Clé publique de l'expéditeur
        - Le module de chiffrement de l'expéditeur """

    messageFinal = []
    #On intialise la liste qui stockera le résultat au fur et à mesure

    for indexCaractère in range (len(message)):

        numeroCaractère = ord(message[indexCaractère])
        #On récupere le numéro du caractère de chaque message dans la table ASCII avec ord()

        messageFinal.append(pow(numeroCaractère, clefPublique, moduleDeChiffrement))
        #la fonction pow(a, b, c) est la fonction qui renvoie a puissance b modulo c

    messageFinal = "/".join(map(str, messageFinal))
    #On formate le message chiffré pour l'envoyer plus facilement
    
    #Le message est désormais chiffré et formaté et ne peut être déchiffré uniquement avec la clé privée
    return messageFinal


def déchiffrement(message, clefPrivée, moduleDeChiffrement):

    """Fonction de décryptage : transforme le message indéchiffrable en message chiffré"""

    messageDéchiffré = ""

    message = message.split("/")
    message = list(map(int, message))
    #On transforme la chaine d'entrée en liste d'entiers

    for indexEntier in range(len(message)):
    #Pour chaque index de la liste messages
    
        numeroCaractère = pow(message[indexEntier], clefPrivée, moduleDeChiffrement)
        #On déchiffre le message, en récupérant a puissance b modulo c
        #C'est effectuant cette puissance sur chaque membre de la liste composant le message crypté que l'on décrypte chaque caractère du message
        messageDéchiffré += chr(numeroCaractère)
        #On transforme le numéro ascii en caractère

    #Le message est alors déchiffré
    return messageDéchiffré



def génération(longueur):

    """Fonction de la création d'une paire de clefs publique/privée de taille variable : Plus la taille des clefs (en bits et gérée par longueur) est grande, plus leur sécurité et la longueur de leur création le sont"""

    ## Choix aléatoire de deux grands nombres premiers qui serviront à créer des clefs plus sécurisées ##

    p = mersenne(longueur)
    q = mersenne(longueur)

    ## Génération d'un grand nombre premier complexe à partir des deux grands nombres premiers précédents qui servira de clef publique clefPublique ##

    clefPublique = randrange(2**(longueur - 1), 2**(longueur))
    while pgcd(clefPublique, (p - 1) * (q - 1)) != 1:
        clefPublique = randrange(2**(longueur - 1), 2**(longueur))

    ## Calcul de la clef privée clefPrivée à partir d'une fonction et de la clef publique clefPublique ##

    clefPrivée = inverse(clefPublique, (p - 1) * (q - 1))

    ## Calcul du module de chiffrement (moduleDeChiffrement) ##

    moduleDeChiffrement = p * q

    return (moduleDeChiffrement, clefPublique, clefPrivée)



def Miller_Rabin(premier):

    """Fonction Miller-Rabin : retourne True si premier est nombre premier selon l'algorithme Miller-Rabin"""

    s = premier - 1
    t = 0
    while s % 2:
        s = s // 2
        t += 1
    for trials in range(5):
        u = randrange(2, premier - 1)
        v = pow(u, s, premier)
        if v != 1:
            i = 0
            while v != (premier - 1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (pow(v, 2)) % premier
    return True


def primalité(premier):

    """Fonction de primalité : retourne True si premier est le nombre premier selon plusieurs algorithmes"""

    if (premier < 2):
        return False

    petits_nombres_premiers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if premier in petits_nombres_premiers:
        return True

    for prime in petits_nombres_premiers:
        if (premier % prime == 0):
            return False
    return Miller_Rabin(premier)


def mersenne(longueur):

    """Renvoie un nombre premier aléatoire de taille correspondant à la variable longueur en bits"""

    while True:
        premier = randrange(2**(longueur - 1), 2**(longueur))
        if primalité(premier):
            return premier


def pgcd(clefPublique, phiDuModuleDeChiffrement):

    "Fonction de calcul du PGCD (Plus Grand Commun Diviseur) de clefPublique et phi de moduleDeChiffrement : Ce PGCD servira de clef publique"

    while clefPublique != 0:
        clefPublique, phiDuModuleDeChiffrement = phiDuModuleDeChiffrement % clefPublique, clefPublique # % reste de la division euclidienne
    return phiDuModuleDeChiffrement


def inverse(clefPublique, phiDuModuleDeChiffrement):

    """Fonction inverse : Cacule l'inverse de clefPublique modulo phiDuModuleDeChiffrement avec l'algorithme d'euclide étendu"""

    if pgcd(clefPublique, phiDuModuleDeChiffrement) != 1:
        return None  # Si clefPublique et phiDuModuleDeChiffrement ne sont pas premier

    ## Calcul de l'algorithme d'euclide étendu ##

    u1, u2, u3, v1, v2, v3 = 0, 1, phiDuModuleDeChiffrement, 1, 0, clefPublique
    while v3 != 0:
        q = u3 // v3  # // quotient de la division euclidienne
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % phiDuModuleDeChiffrement



if __name__ == "__main__":
#Si on execute le fichier en lui même, ces lignes ne seront pas lues en cas d'import

    """ Démonstration du module de chiffrement"""

    module, CléPublique, CléPrivée = génération(16)

    print(f"Votre Clé Publique => {CléPublique}\nVotre Clé Privée => {CléPrivée}\nVotre module de chiffrement => {module}\n")
    
    MessageClair = input("Quel message désirez vous chiffrer ?\n>>> ")
    MessageChiffré = chiffrement(MessageClair, CléPublique, module)

    print(f"\n{MessageClair} chiffré avec l'algorithme RSA donne {MessageChiffré}")

    #Inutile de faire la démonstration du déchiffrement