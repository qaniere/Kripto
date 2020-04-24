from random import *

"""Dans ce programme on simulera la création d'une paire de clef publique/privée, l'envoi d'un message ainsi que son chiffrement, cryptage, décryptage puis finalement déchiffrement."""

def chiffrement(message):

    """Fonction de chiffrement : transforme le message clair en message chiffré"""

    message = list(message)
    for i in range(len(message)):
        message[i] = ord(message[i])
    return message


def cryptage(m, A, g):

    """Fonction de cryptage : transforme le message chiffré en message indéchiffrable"""

    for x in range(len(m)):
        m[x] = pow(m[x], A, g)
    return m


def décryptage(c, a, g):

    """Fonction de décryptage : transforme le message indéchiffrable en message chiffré"""

    for y in range(len(c)):
        c[y] = pow(c[y], a, g)
    return c


def déchiffrement(chiffré):

    """Fonction de déchiffrement : transforme le message chiffré en message clair"""

    for j in range(len(chiffré)):
        chiffré[j] = chr(chiffré[j])
    chiffré = "".join(chiffré)
    return chiffré


def Miller_Rabin(num):

    """Returne True si num est nombre premier"""

    s = num - 1
    t = 0
    while s % 2:
        s = s // 2
        t += 1
    for i in range(5):
        a = randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (pow(v, 2)) % num
    return True


def primalité(num):

    """Retourne True si num est le nombre premier ..."""

    if (num < 2):
        return False

    lowPrimes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
        307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
        389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
        467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569,
        571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
        653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
        751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
        853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
        947, 953, 967, 971, 977, 983, 991, 997
    ]

    if num in lowPrimes:
        return True

    for prime in lowPrimes:
        if (num % prime == 0):
            return False

    return rabinMiller(num)


def generateLargePrime(longueur):

    """Renvoie un nombre premier aléatoire de longueur équivalente à la variable longueur en terme de bits"""

    while True:
        num = randrange(2**(longueur - 1), 2**(longueur))
        if primalité(num):
            return num


def pgcd(a, b):

    """Fonction de calcul du plus grand commun diviseur de a et b : Il s'agit du produit de tous les nombres premiers (doublets compris) que ces deux nombres ont en commun"""

    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):

    """Cacul l'invers de a mod m avec l'algorithme d'euclide étendu"""

    if pgcd(a, m) != 1:
        return None  # Si a et m ne sont pas premier
    # Calcul l'algorithme d'euclide étendu
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # // dividion entiere
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (
            u3 - q * v3), v1, v2, v3
    return u1 % m


def génération(longueur):

    """Fonction de la création d'une paire de clefs publique/privée de taille variable : Plus la taille des clefs (en bits et gérée par longueur) est grande, plus leur sécurité et la longueur de leur création le sont"""

    ## Choix aléatoire de deux grands nombres premiers qui serviront à créer des clefs plus sécurisées ##

    p = generateLargePrime(longueur)
    q = generateLargePrime(longueur)

    ## Génération d'un grand nombre premier complexe à partir des deux grands nombres premiers précédents qui servira de clef publique A ##

    A = randrange(2**(longueur - 1), 2**(longueur))
    while pgcd(A, (p - 1) * (q - 1)) != 1:
        A = randrange(2**(longueur - 1), 2**(longueur))

    ## Calcul de la clef privée a à partir d'une fonction et de la clef publique A ##

    a = findModInverse(A, (p - 1) * (q - 1))

    ## Calcul du module de chiffrement (g) ##

    g = p * q

    return (g, A, a)


### Génération des clefs et du module de chiffrement ###

g, A, a = génération(16)

print("Module de chiffrement (g) : " + str(g) +
      "\n        Clef publique (A) : (" + str(g) + ", " + str(A) +
      ")\n          Clef privée (a) : (" + str(g) + ", " + str(a) + ")\n")

## Entrée du message à envoyer ##

message = input("Tapez votre message :\n\n    ")

while len(message) >= 255:
    message = input(
        "\nVotre message doit faire moins de 255 caractères.\n\nTapez votre message :\n\n    "
    )

## Chiffrement du message ##

m = chiffrement(message)

## Cryptage du message ##

c = cryptage(m, A, g)

##  Affichage du message chiffré et crypté (donc indéchiffrable) grâce à la clef publique, qui sert à la simulation de l'envoi du message ##

print("\nLe message chiffré par grâce à la clef publique est :", c, "\n")

## Entrée manuelle de la clef pour simuler le taf du PC
clefTapée = int(
    input("Tapez votre clef privée pour lire votre message :\n\n>>> "))

d = décryptage(c, clefTapée, g)

déchiffré = déchiffrement(d)

print("Le message dechiffré est :\n\n", déchiffré)

input("\n\nFin du programme\n\n")
