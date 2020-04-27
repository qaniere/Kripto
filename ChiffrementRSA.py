from random import *


"""Dans ce programme on simulera la création d'une paire de clef publique/privée, l'envoi d'un message ainsi que son chiffrement, cryptage, décryptage puis finalement déchiffrement."""


''''''''''''''''''''''' Message au lecteur ''''''''''''''''''''

Dans ce script, certains paramètres se trouveront toujours
sous formes de variables au nom court.

- Le module de chiffrement sera appelé par la variable "g"
- La clef publique sera appelée par la variable "A"
- La clef privée sera appelée par la variable "a"

- Le message clair sera appelé mar la variable "m"
- Le message chiffré sera appelé par la variable "n"
- Le message chiffré et crypté sera appelé par la variable "c"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


### Définition de la fonction de chiffrement ###


def chiffrement(m):

    """Fonction de chiffrement : transforme le message clair en message chiffré"""

    n = list(m)
    for i in range(len(n)):
        n[i] = ord(n[i])
    return n


### Définition de la fonction de cryptage ###


def cryptage(n, A, g):

    """Fonction de cryptage : transforme le message chiffré en message indéchiffrable"""

    c = n
    for x in range(len(c)):
        c[x] = pow(c[x], A, g)
    return c


### Définition de la fonction de décryptage ###


def décryptage(c, a, g):

    """Fonction de décryptage : transforme le message indéchiffrable en message chiffré"""

    n = c
    for y in range(len(n)):
        n[y] = pow(n[y], a, g)
    return n


### Définition de la fonction de déchiffrement ###


def déchiffrement(n):

    """Fonction de déchiffrement : transforme le message chiffré en message clair"""

    m = n
    for j in range(len(m)):
        m[j] = chr(m[j])
    m = "".join(m)
    return m


### Définition de la fonction de génération des clefs ###


def génération(longueur):

    """Fonction de la création d'une paire de clefs publique/privée de taille variable : Plus la taille des clefs (en bits et gérée par longueur) est grande, plus leur sécurité et la longueur de leur création le sont"""

    ## Choix aléatoire de deux grands nombres premiers qui serviront à créer des clefs plus sécurisées ##

    p = mersenne(longueur)
    q = mersenne(longueur)

    ## Génération d'un grand nombre premier complexe à partir des deux grands nombres premiers précédents qui servira de clef publique A ##

    A = randrange(2**(longueur - 1), 2**(longueur))
    while pgcd(A, (p - 1) * (q - 1)) != 1:
        A = randrange(2**(longueur - 1), 2**(longueur))

    ## Calcul de la clef privée a à partir d'une fonction et de la clef publique A ##

    a = inverse(A, (p - 1) * (q - 1))

    ## Calcul du module de chiffrement (g) ##

    g = p * q

    return (g, A, a)


### Définition de la fonction de Miller-Rabin ###


def Miller_Rabin(premier):

    """Fonction Miller-Rabin : retourne True si premier est nombre premier selon l'algorithme Miller-Rabin"""

    s = premier - 1
    t = 0
    while s % 2:
        s = s // 2
        t += 1
    for trials in range(5):
        a = randrange(2, premier - 1)
        v = pow(a, s, premier)
        if v != 1:
            i = 0
            while v != (premier - 1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (pow(v, 2)) % premier
    return True


### Définition de la fonction de primalité ###


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


### Définition de la fonction de génération d'un grand nombre premier ###


def mersenne(longueur):

    """Renvoie un nombre premier aléatoire de taille correspondant à la variable longueur en bits"""
    
    while True:
        premier = randrange(2**(longueur - 1), 2**(longueur))
        if primalité(premier):
            return premier


### Définition de la fonction de calcul de la clef publique ###


def pgcd(A, phi_de_g):

    "Fonction de calcul du PGCD (Plus Grand Commun Diviseur) de A et phi de g : Ce PGCD servira de clef publique"

    while A != 0:
        A, phi_de_g = phi_de_g % A, A
    return phi_de_g


### Définition de la fonction de calcul de la clef privée  ###


def inverse(A, phi_de_g):
    
    """Fonction inverse : Cacule l'inverse de A modulo phi_de_g avec l'algorithme d'euclide étendu"""

    if pgcd(A, phi_de_g) != 1:
        return None  # Si A et phi_de_g ne sont pas premier

    ## Calcul de l'algorithme d'euclide étendu ##

    u1, u2, u3, v1, v2, v3 = 0, 1, phi_de_g, 1, 0, A
    while v3 != 0:
        q = u3 // v3  # // division euclidienne
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % phi_de_g


### Génération des clefs et du module de chiffrement ###


g, A, a = génération(16)


### Impression des clefs et du module de chiffrement ###


print("Module de chiffrement (g) : " + str(g) + "\n        Clef publique (A) : (" + str(g) + ", " + str(A) + ")\n          Clef privée (a) : (" + str(g) + ", " + str(a) + ")\n")


### Entrée du message à envoyer ###


m = input("Tapez votre message :\n\n    ")

## Vérification de la longueur du message ##

while len(m) >= 255:
    m = input("\nVotre message doit faire moins de 255 caractères.\n\nTapez votre message :\n\n    ")


### Chiffrement du message ###


n = chiffrement(m)


### Cryptage du message ###


c = cryptage(n, A, g)


###  Affichage du message chiffré et crypté (donc indéchiffrable) grâce à la clef publique, qui sert à la simulation de l'envoi du message ###


print("\nLe message chiffré par grâce à la clef publique est :", c, "\n")


### Entrée manuelle de la clef privée nécessaire au décryptage du message pour simuler le travail de l'ordinateur ###


clefTapée = int(
    input("Tapez votre clef privée pour lire votre message :\n\n>>> "))


### Décryptage du message ###


n = décryptage(c, clefTapée, g)


### Déchiffrement du message ###


m = déchiffrement(n)


### Affichage du message déchiffré ###


print("\nLe message dechiffré est :\n\n", m)

input("\n\nVous êtes arrivés à la fin du programme\n\n")
