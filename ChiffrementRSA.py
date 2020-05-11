# coding: utf8
from random import *


"""Dans ce programme on simulera la création d'une paire de clef publique/privée, l'envoi d'un message ainsi que son chiffrement, cryptage, décryptage puis finalement déchiffrement."""


''''''''''''''''''''''' Message au lecteur ''''''''''''''''''''
Dans ce script, certains paramètres se trouveront toujours
sous formes de variables au nom court.
- Le module de chiffrement sera appelé par la variable "moduleDeChiffrement"
- La clef publique sera appelée par la variable "clefPublique"
- La clef privée sera appelée par la variable "clefPrivée"
- Le message clair sera appelé mar la variable "messageClair"
- Le message chiffré sera appelé par la variable "messageChiffré"
- Le message chiffré et crypté sera appelé par la variable "messageCrypté"
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


### Définition de la fonction de chiffrement ###


def transformationChiffres(messageClair):

    """Fonction de chiffrement : transforme le message clair en message chiffré"""

    messageChiffré = list(messageClair)
    for i in range(len(messageChiffré)):
        messageChiffré[i] = ord(messageChiffré[i])
        # ord(x) est la fonction qui pour tout charactère Unicode (sous type str) x renvoie sa valeur Unicode
    return messageChiffré


### Définition de la fonction de cryptage ###


def cryptage(messageChiffré, clefPublique, moduleDeChiffrement):

    """Fonction de cryptage : transforme le message chiffré en message indéchiffrable"""

    messageCrypté = messageChiffré
    for x in range(len(messageCrypté)):
        messageCrypté[x] = pow(messageCrypté[x], clefPublique, moduleDeChiffrement)
        # pow(a, b, c) est la fonction qui renvoie a puissance b modulo c
    return messageCrypté


### Définition de la fonction de décryptage ###


def décryptage(messageCrypté, clefPrivée, moduleDeChiffrement):

    """Fonction de décryptage : transforme le message indéchiffrable en message chiffré"""

    messageChiffré = messageCrypté
    for y in range(len(messageChiffré)):
        messageChiffré[y] = pow(messageChiffré[y], clefPrivée, moduleDeChiffrement)
        # pow(a, b, c) est la fonction qui renvoie a puissance b modulo c
    return messageChiffré


### Définition de la fonction de déchiffrement ###


def transformationCaratères(messageChiffré):

    """Fonction de déchiffrement : transforme le message chiffré en message clair"""

    messageClair = messageChiffré
    for j in range(len(messageClair)):
        messageClair[j] = chr(messageClair[j])
        # chr(x) est la fonction qui pour toute valeur Unicode x nous renvoie son charactère Unicode (sous type str)
    messageClair = "".join(messageClair)
    return messageClair


### Définition de la fonction de génération des clefs ###


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


### Définition de la fonction de Miller-Rabin ###


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


def pgcd(clefPublique, phiDuModuleDeChiffrement):

    "Fonction de calcul du PGCD (Plus Grand Commun Diviseur) de clefPublique et phi de moduleDeChiffrement : Ce PGCD servira de clef publique"

    while clefPublique != 0:
        clefPublique, phiDuModuleDeChiffrement = phiDuModuleDeChiffrement % clefPublique, clefPublique
    return phiDuModuleDeChiffrement


### Définition de la fonction de calcul de la clef privée  ###


def inverse(clefPublique, phiDuModuleDeChiffrement):

    """Fonction inverse : Cacule l'inverse de clefPublique modulo phiDuModuleDeChiffrement avec l'algorithme d'euclide étendu"""

    if pgcd(clefPublique, phiDuModuleDeChiffrement) != 1:
        return None  # Si clefPublique et phiDuModuleDeChiffrement ne sont pas premier

    ## Calcul de l'algorithme d'euclide étendu ##

    u1, u2, u3, v1, v2, v3 = 0, 1, phiDuModuleDeChiffrement, 1, 0, clefPublique
    while v3 != 0:
        q = u3 // v3  # // division euclidienne
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % phiDuModuleDeChiffrement
