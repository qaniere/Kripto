import random, rabinMiller, cryptomath

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


def génération(longueur):

    """Fonction de la création d'une paire de clefs publique/privée de taille variable : Plus la taille des clefs (en bits et gérée par longueur) est grande, plus leur sécurité et la longueur de leur création le sont"""

    ## Choix aléatoire de deux grands nombres premiers qui serviront à créer des clefs plus sécurisées ##

    p = rabinMiller.generateLargePrime(longueur)
    q = rabinMiller.generateLargePrime(longueur)

    ## Génération d'un grand nombre premier complexe à partir des deux grands nombres premiers précédents qui servira de clef publique A ##

    A = random.randrange(2**(longueur - 1), 2**(longueur))
    while cryptomath.pgcd(A, (p - 1) * (q - 1)) != 1:
        A = random.randrange(2**(longueur - 1), 2**(longueur))

    ## Calcul de la clef privée a à partir d'une fonction et de la clef publique A ##

    a = cryptomath.findModInverse(A, (p - 1) * (q - 1))

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

print("Le message dechiffré est :", déchiffré)
