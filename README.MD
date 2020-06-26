# Kripto

Kripto est un chat chiffré peer to peer. Tout les messages sont chiffré avec l'algorithe RSA, ce qui le rend sécurisé. Les message peuvent être
échangé au sein d'un réseau local mais également à travers Internet, à l'aide des redirections NAT.

Ce projet a été réalisé par Calixte Pistolet et Quentin Aniere dans le cadre de l'enseignement de spécialité "Numérique et Sciences Informatiques". Il est sous license MIT. Toute contribution est la bienvenue.

## Fonctionalités

 - Discussion peer to peer chiffrée : Seul les participants de la conversations peuvent voir les messages
 - Protection du serveur avec un mot de passe : Seules les personnes qui ont le mot de passe peuvent accéder au serveur
 - Panel de commandes pour les hôtes :
    
    - /stop pour arrêter le serveur
    - En cours d'ajout

 - Sauvegarde des messages
 - Report de bug

## Fonctionnement

*En cours de rédaction*

## Liste de fonctionnalités à implémenter 

- Nettoyer et refactor le code (En cours)

- Pouvoir annuler la connexion si pas de mot de passe sauvegarde

- Régler le bug de la sauvegarde ! (Encoder en Base64)

- Ajouter des commandes :
  
    - /lock - /unlock : Commande pour empêcher l'arrivé de nouveaux utilisateurs
    - /ban : Commande pour bannir un utilisateur 
    - /kick : Commande pour jeter l'utilisateur dehors 
    - /op : Commande qui permet de changer le rôle (Hôte à client, client à hôte)

- Afficher nombres d'utilisateurs connectés

 - Remettre à jour les lignes de l'index
