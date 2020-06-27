# Kripto

Kripto est un chat chiffré peer to peer. Tout les messages sont chiffré avec l'algorithe RSA, ce qui le rend sécurisé. Les message peuvent être
échangé au sein d'un réseau local mais également à travers Internet, à l'aide des redirections NAT.

Ce projet a été réalisé par Calixte Pistolet et Quentin Aniere dans le cadre de l'enseignement de spécialité "Numérique et Sciences Informatiques". Il est sous license MIT. Toute contribution est la bienvenue.

## Fonctionalités

 - Discussion peer to peer chiffrée : Seul les participants de la conversations peuvent voir les messages
 - Options de configuration (Choix des sons d'envoi et de reception de messages)
 - Protection du serveur avec un mot de passe : Seules les personnes qui ont le mot de passe peuvent accéder au serveur
 - Panel de commandes pour les hôtes :
    
    - /stop pour arrêter le serveur
    - /lock pour interdir l'arrivée de nouveaux clients
    - /unlock pour autoriser l'arrivée de nouveaux clients
    - /ban pour bannir un client
    - /kick pour jeter un client hors du serveur

 - Sauvegarde des messages
 - Report de bug (Disponible si le module requests est installé)

## Fonctionnement

Pour nous contacter depuis Kripto, merci d'installer le module requests

## Liste de fonctionnalités à implémenter 

- Faire le /op pour l'hôte

- Afficher nombres d'utilisateurs connectés pour les clients
